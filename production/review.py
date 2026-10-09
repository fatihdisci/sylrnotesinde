"""Minimal loopback audio/word editor. Saving never fabricates a human listening approval."""
import argparse,datetime,json,mimetypes,threading
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from core import ROOT,paths,read,write,word_errors,export,bindings,sha
SAVE_LOCK=threading.Lock()
def editable_current(id):
    spec,dest=paths(id);data=read(dest/'word-timings.json')
    if data['bindings']!=bindings(spec,dest/'narration.wav'):raise ValueError('STALE sources; regenerate before editing')
    if data['alignerHash']!=sha((ROOT/'alignment/model.json').read_bytes()):raise ValueError('STALE alignment model')
    return data

HTML='''<!doctype html><html lang="tr"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Altyazı inceleme · Sayıların Ötesinde</title><style>
@font-face{font-family:Plex;src:url(/font)}body{background:#111615;color:#F2F0E9;font-family:Plex,sans-serif;max-width:1000px;margin:32px auto;padding:20px}header{position:sticky;top:0;background:#111615;padding:14px 0;border-bottom:1px solid #35413E;z-index:2}button,input{font:inherit;background:#202926;color:#F2F0E9;border:1px solid #909B97;padding:7px;margin:3px}input[type=number]{width:105px}#caption{white-space:pre-line;height:78px;font-size:26px;color:#F2F0E9}table{width:100%;border-collapse:collapse}td{border-bottom:1px solid #35413E;padding:6px}.active{color:#F07857}.suspect{border-left:3px solid #F07857}#status{color:#9DBFCA}small{color:#909B97}audio{width:100%}@media(max-width:700px){body{margin:0;padding:16px 12px 120px}header{position:static}h2{font-size:22px}#caption{position:fixed;bottom:0;left:0;right:0;height:auto;min-height:64px;padding:12px;background:#111615;border-top:1px solid #35413E;font-size:22px;z-index:3}thead{display:none}tr{display:grid;grid-template-columns:1fr 1fr}td:first-child,td:last-child{grid-column:1/-1}td{min-width:0}input[type=number]{width:80px}button{padding:6px}#mapping{font-size:15px}table{table-layout:fixed}}
</style>
<header><h2>Altyazı / gerçek ses incelemesi</h2><audio id="audio" controls src="/audio"></audio><div id="caption"></div><div id="status"></div><input id="reviewer" placeholder="İnceleyen kişi"><label><input type="checkbox" id="listened">Sesin tamamını dinledim ve zamanları kontrol ettim.</label><br><button id="save">Düzeltmeleri kaydet</button><button id="approve">İncelemeyi onayla</button><small>1 kare =33,333 ms. Taslağı kaydetmek onay sayılmaz.</small></header><p>Kelimeye tıklayarak dinle. Sayıların yazıyla okunuşu ↔ ekrandaki metin eşlemesi aşağıda.</p><details><summary>Konuşma / ekran metni eşlemeleri</summary><div id="mapping"></div></details><table><thead><tr><th>Kelime</th><th>Başlangıç ms</th><th>Bitiş ms</th><th>Güven / durum</th></tr></thead><tbody id="words"></tbody></table><script>
let data,cues;const audio=document.querySelector('#audio'),status=document.querySelector('#status');
async function load(){let r=await fetch('/state');data=await r.json();if(!r.ok)throw Error(data.error);cues=data.cues;document.querySelector('#mapping').textContent=data.displayMap.map(m=>m.spokenWordIds.map(i=>data.words[i].word).join(' ')+' → '+m.display.join(' / ')).join(' | ');render();}
function render(){const body=document.querySelector('#words');body.replaceChildren();data.words.forEach(w=>{const tr=document.createElement('tr');tr.id='word-'+w.id;if(w.issues.length)tr.className='suspect';const td=document.createElement('td'),play=document.createElement('button');play.textContent=w.word;play.onclick=()=>{audio.currentTime=Math.max(0,w.startMs/1000-.18);audio.play();};td.append(play);tr.append(td);for(const key of ['startMs','endMs']){const cell=document.createElement('td'),input=document.createElement('input');input.type='number';input.step='0.001';input.value=w[key];input.onchange=()=>w[key]=Number(input.value);for(const direction of [-1,1]){const button=document.createElement('button');button.textContent=direction<0?'−1f':'+1f';button.onclick=()=>{w[key]=Math.round((Number(input.value)+direction*1000/30)*1000)/1000;input.value=w[key];};cell.append(button);}cell.append(input);tr.append(cell);}const info=document.createElement('td');info.textContent=w.confidence.toFixed(2)+' / '+w.reviewStatus+' '+w.issues.join(', ');tr.append(info);body.append(tr);});status.textContent='Durum: '+data.review.status+' '+(data.integrityErrors||[]).join('; ');}
function tick(){const ms=audio.currentTime*1000;document.querySelectorAll('tr.active').forEach(e=>e.classList.remove('active'));let w=data?.words.find(w=>w.startMs<=ms&&ms<w.endMs);if(w)document.querySelector('#word-'+w.id).classList.add('active');let m=data?.displayMap.find(m=>{let a=data.words[m.spokenWordIds[0]],b=data.words[m.spokenWordIds.at(-1)];return a.startMs<=ms&&ms<b.endMs;});document.querySelector('#caption').textContent=m?m.display.join('\\n'):'';requestAnimationFrame(tick);}tick();
async function save(approve){try{const r=await fetch('/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({words:data.words.map(w=>({id:w.id,startMs:w.startMs,endMs:w.endMs})),reviewer:document.querySelector('#reviewer').value,listened:document.querySelector('#listened').checked,approve,expectedAlignmentHash:data.alignmentHash})});const result=await r.json();if(!r.ok)throw Error(result.error);await load();status.textContent='Kaydedildi · '+result.status;}catch(e){status.textContent=e.message;}}
document.querySelector('#save').onclick=()=>save(false);document.querySelector('#approve').onclick=()=>save(true);load().catch(e=>status.textContent=e.message);
</script></html>'''

def apply_review(id,payload):
    from core import sha
    data=editable_current(id);_,dest=paths(id)
    if payload.get('expectedAlignmentHash')!=sha((dest/'word-timings.json').read_bytes()):raise ValueError('Stale editor tab; reload before saving')
    if [w['id'] for w in payload['words']]!=[w['id'] for w in data['words']]:raise ValueError('Missing/reordered words')
    reviewer=payload.get('reviewer','').strip()
    if not reviewer:raise ValueError('Reviewer name required for a correction record')
    for old,new in zip(data['words'],payload['words']):
        for field in ['startMs','endMs']:
            if old[field]!=new[field]:old['corrections'].append({'field':field,'before':old[field],'after':new[field],'reviewer':reviewer,'at':datetime.datetime.now(datetime.timezone.utc).isoformat()});old[field]=new[field]
    errors=word_errors(data)
    if errors:raise ValueError('; '.join(errors))
    approve=payload.get('approve') is True
    if approve and payload.get('listened') is not True:raise ValueError('Listening confirmation is required; JSON validity is not approval')
    data['review']={'status':'approved' if approve else 'needs_review','reviewer':reviewer,'listened':approve,'at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    if approve:
        for word in data['words']:word['reviewStatus']='approved'
    else:
        for word in data['words']:word['reviewStatus']='needs_review'
    # Retain the original detector findings; explicit full listening/timing approval
    # resolves their review state only after the current energy/timing checks pass.
    for gap in data.get('unexplainedSpeechGaps',[]):
        gap['reviewed']=approve
        gap['reviewer']=reviewer if approve else None
        gap['reviewedAt']=data['review']['at'] if approve else None
    targets=[dest/n for n in ['word-timings.json','captions.json','captions.srt','narration-manifest.json']]
    backup={p:p.read_bytes() if p.exists() else None for p in targets}
    try:
        write(dest/'word-timings.json',data);export(id)
    except Exception:
        for p,content in backup.items():
            if content is not None:p.write_bytes(content)
            elif p.exists():p.unlink()
        raise
    return data['review']

def main():
    p=argparse.ArgumentParser();p.add_argument('--id',required=True);p.add_argument('--port',type=int,default=3033);args=p.parse_args();_,dest=paths(args.id)
    class Handler(BaseHTTPRequestHandler):
        def reply(self,status,body,mime='application/json'):
            self.send_response(status);self.send_header('Content-Type',mime);self.send_header('Content-Length',str(len(body)));self.send_header('Cache-Control','no-store');self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; media-src 'self'; font-src 'self'; connect-src 'self'");self.end_headers()
            try:self.wfile.write(body)
            except (BrokenPipeError,ConnectionResetError):pass
        def safe(self):return self.headers.get('Host') in [f'127.0.0.1:{args.port}',f'localhost:{args.port}'] and self.headers.get('Origin',f'http://127.0.0.1:{args.port}') in [f'http://127.0.0.1:{args.port}',f'http://localhost:{args.port}']
        def do_GET(self):
            if not self.safe():return self.reply(403,b'{}')
            try:
                if self.path=='/':return self.reply(200,HTML.encode(),'text/html; charset=utf-8')
                if self.path=='/font':return self.reply(200,(ROOT/'public/fonts/IBMPlexSans-Regular.woff2').read_bytes(),'font/woff2')
                if self.path=='/audio':
                    import re
                    audio=(dest/'narration.wav').read_bytes();size=len(audio);request=self.headers.get('Range')
                    if not request:return self.reply(200,audio,'audio/wav')
                    match=re.fullmatch(r'bytes=(\d+)-(\d*)',request)
                    if not match:return self.reply(416,b'')
                    start=int(match[1]);end=min(size-1,int(match[2]) if match[2] else size-1)
                    if start>end:return self.reply(416,b'')
                    self.send_response(206);self.send_header('Content-Type','audio/wav');self.send_header('Accept-Ranges','bytes');self.send_header('Content-Range',f'bytes {start}-{end}/{size}');self.send_header('Content-Length',str(end-start+1));self.end_headers()
                    try:self.wfile.write(audio[start:end+1])
                    except (BrokenPipeError,ConnectionResetError):pass
                    return
                if self.path=='/state':
                    from core import sha
                    data=editable_current(args.id);data={**data,'cues':read(dest/'captions.json') if (dest/'captions.json').exists() else [],'integrityErrors':word_errors(data),'alignmentHash':sha((dest/'word-timings.json').read_bytes())};return self.reply(200,json.dumps(data,ensure_ascii=False).encode())
                self.reply(404,b'{}')
            except Exception as e:self.reply(400,json.dumps({'error':str(e)}).encode())
        def do_POST(self):
            if not self.safe():return self.reply(403,b'{}')
            if self.path!='/save':return self.reply(404,b'{}')
            try:
                length=int(self.headers.get('Content-Length',0))
                if not 0<length<200000:raise ValueError('Invalid payload size')
                payload=json.loads(self.rfile.read(length))
                with SAVE_LOCK:result=apply_review(args.id,payload)
                self.reply(200,json.dumps(result).encode())
            except Exception as e:self.reply(400,json.dumps({'error':str(e)}).encode())
    print(f'http://127.0.0.1:{args.port} · {args.id}',flush=True);ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
if __name__=='__main__':main()
