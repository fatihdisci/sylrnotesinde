"""Loopback-only blind listening server, no third-party assets or network clients."""
import argparse, hashlib, json, os, secrets, time
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
DIMS=['pronunciation','naturalness','intonation','overall']

def atomic_json(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix('.tmp')
    temp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    temp.replace(path)

def valid_rating(value,allow_partial=False):
    if not isinstance(value,dict) or not set(value).issubset(DIMS) or (not allow_partial and set(value)!=set(DIMS)): raise ValueError('Invalid rating dimensions')
    if any(type(v) is not int or v not in range(1,6) for v in value.values()): raise ValueError('Scores must be integers 1–5')
    return value

class Session:
    def __init__(self,state_dir=None):
        self.directory=Path(state_dir) if state_dir else ROOT/'comparison'
        self.path=self.directory/'private-session.json'
        self.models=json.loads((ROOT/'config/models.json').read_text())
        self.tests=json.loads((ROOT/'test-texts/tests.json').read_text())
        catalog=json.loads((ROOT/'config/catalog.json').read_text())
        self.records=catalog['records']
        fingerprint=hashlib.sha256(json.dumps([(r['model'],r['voice'],r['test'],r['variant'],r['sha256']) for r in self.records],sort_keys=True).encode()).hexdigest()
        if self.path.exists():
            self.data=json.loads(self.path.read_text())
            if self.data['fingerprint']!=fingerprint: raise RuntimeError('Corpus changed. Preserve the current session and use --state-dir for a new session.')
        else:
            order=list(self.models); secrets.SystemRandom().shuffle(order)
            self.data=dict(id=secrets.token_hex(12),fingerprint=fingerprint,order=order,ids={self.key(r):secrets.token_hex(12) for r in self.records},ratings={},revealed=False)
            atomic_json(self.path,self.data)
        self.by_id={self.data['ids'][self.key(r)]:r for r in self.records}
        self.required=[self.data['ids'][self.key(r)] for r in self.records if r['variant']=='original' and r['voice']==self.models[r['model']]['voices'][0]]
    @staticmethod
    def key(r): return '|'.join(r[k] for k in ['model','voice','test','variant'])
    def is_rated(self,i): return i in self.data['ratings'] and set(self.data['ratings'][i]['scores'])==set(DIMS)
    def complete(self): return all(self.is_rated(i) for i in self.required)
    def public(self):
        groups=[]
        for index,key in enumerate(self.data['order']):
            spec=self.models[key]; revealed=self.data['revealed']
            groups.append(dict(alias=f'Model {chr(65+index)}',name=spec['name'] if revealed else None,voices=[dict(id=str(i),label=v if revealed else f'Ses {i+1}') for i,v in enumerate(spec['voices'])],clips=[dict(id=self.data['ids'][self.key(r)],voice=str(spec['voices'].index(r['voice'])),test=r['test'],variant=r['variant'],duration=r['durationSeconds'],speed=r['speed']) for r in self.records if r['model']==key]))
        return dict(session=self.data['id'],groups=groups,tests=self.tests,ratings=self.data['ratings'],revealed=self.data['revealed'],complete=self.complete(),required=len(self.required),rated=sum(self.is_rated(i) for i in self.required))
    def save(self,body):
        if not isinstance(body,dict): raise ValueError('JSON object required')
        if body.get('reveal'):
            if not self.complete(): raise ValueError('Rate the first voice for all four tests and all three models before revealing')
            self.data['revealed']=True
        elif 'id' in body:
            if body['id'] not in self.by_id: raise ValueError('Unknown audio')
            ratings=valid_rating(body['ratings'],allow_partial=True)
            comment=body.get('comment','')
            if not isinstance(comment,str) or len(comment)>5000: raise ValueError('Comment too long')
            self.data['ratings'][body['id']]=dict(scores=ratings,comment=comment,updated=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))
        else: raise ValueError('Invalid request')
        atomic_json(self.path,self.data)
        exported=self.export()
        atomic_json(self.directory/'results'/f'{self.data["id"]}.json',exported)
        return self.public()
    def export(self):
        result=dict(schemaVersion=1,session=self.data['id'],revealed=self.data['revealed'],ratings=self.data['ratings'],protocol='Native speeds; -20 LUFS, -2 dBTP listening copies; no automatic winner.')
        if self.data['revealed']: result['identities']={i:{k:r[k] for k in ['model','voice','test','variant','speed','sha256']} for i,r in self.by_id.items()}
        return result

def handler(session):
    class Handler(BaseHTTPRequestHandler):
        def safe_host(self): return self.headers.get('Host') in (f'127.0.0.1:{self.server.server_port}',f'localhost:{self.server.server_port}')
        def send(self,status,data,ctype='application/json; charset=utf-8',extra=None):
            if not isinstance(data,bytes): data=json.dumps(data,ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header('Content-Type',ctype);self.send_header('Content-Length',str(len(data)))
            self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; font-src 'self'; media-src 'self'; connect-src 'self'; frame-ancestors 'none'")
            for k,v in (extra or {}).items(): self.send_header(k,v)
            self.end_headers();self.wfile.write(data)
        def do_GET(self):
            if not self.safe_host(): return self.send(403,{'error':'Loopback host required'})
            path=urlparse(self.path).path
            if path=='/api/session': return self.send(200,session.public())
            if path=='/api/export': return self.send(200,session.export(),extra={'Content-Disposition':'attachment; filename="ses-karsilastirma.json"'})
            if path.startswith('/audio/'):
                record=session.by_id.get(path.removeprefix('/audio/'))
                if not record: return self.send(404,{'error':'Unknown audio'})
                file=(ROOT/record['listeningPath']).resolve()
                if not file.is_relative_to((ROOT/'outputs').resolve()): return self.send(403,{'error':'Invalid path'})
                audio=file.read_bytes();size=len(audio)
                extra={'Accept-Ranges':'bytes'}
                if self.headers.get('Range'):
                    try:
                        value=self.headers['Range'].removeprefix('bytes=');start,end=value.split('-')
                        start=int(start);end=min(int(end) if end else size-1,size-1)
                        if not 0<=start<=end<size: raise ValueError()
                    except ValueError: return self.send(416,b'',extra={'Content-Range':f'bytes */{size}'})
                    extra['Content-Range']=f'bytes {start}-{end}/{size}'
                    return self.send(206,audio[start:end+1],'audio/wav',extra)
                return self.send(200,audio,'audio/wav',extra)
            files={'/':('index.html','text/html; charset=utf-8'),'/app.js':('app.js','text/javascript; charset=utf-8'),'/style.css':('style.css','text/css; charset=utf-8')}
            if path in files:
                file,ctype=files[path];return self.send(200,(ROOT/'comparison'/file).read_bytes(),ctype)
            if path.startswith('/fonts/'):
                file=(ROOT.parent/'public'/path.lstrip('/')).resolve()
                if file.is_relative_to((ROOT.parent/'public/fonts').resolve()) and file.is_file(): return self.send(200,file.read_bytes(),'font/woff2')
            return self.send(404,{'error':'Not found'})
        def do_POST(self):
            if not self.safe_host() or self.headers.get('Origin') not in (f'http://127.0.0.1:{self.server.server_port}',f'http://localhost:{self.server.server_port}'):
                return self.send(403,{'error':'Same-origin request required'})
            if self.path!='/api/save': return self.send(404,{'error':'Not found'})
            try:
                size=int(self.headers.get('Content-Length','0'))
                if not 0<size<32768: raise ValueError('Invalid request size')
                body=json.loads(self.rfile.read(size));data=session.save(body)
            except (ValueError,KeyError,TypeError) as error: return self.send(400,{'error':str(error)})
            return self.send(200,data)
        def log_message(self,*args): pass
    return Handler

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=3030);p.add_argument('--state-dir');a=p.parse_args()
    session=Session(a.state_dir)
    server=ThreadingHTTPServer(('127.0.0.1',a.port),handler(session))
    # Requests share mutable state; serialize saves by using the lock in process_request_thread.
    import threading
    session_lock=threading.RLock()
    original=session.save
    def locked(body):
        with session_lock: return original(body)
    session.save=locked
    print(f'Local blind comparison: http://127.0.0.1:{a.port}',flush=True)
    print(f'JSON results: {session.directory / "results"}',flush=True)
    server.serve_forever()
