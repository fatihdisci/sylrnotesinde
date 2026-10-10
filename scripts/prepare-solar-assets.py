"""Fetch attributed planet maps once; create an original seeded basketball surface."""
from pathlib import Path
import hashlib,json,subprocess,concurrent.futures,math,random
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'public/episodes/solar-basketball/textures'
FILES={'earth':'earth_daymap','clouds':'earth_clouds','jupiter':'jupiter','neptune':'neptune','sun':'sun','moon':'moon'}
def fetch(pair):
 name,remote=pair;out=DEST/f'{name}.jpg';url=f'https://www.solarsystemscope.com/textures/download/2k_{remote}.jpg'
 if not out.exists():subprocess.run(['curl','--fail','--silent','--show-error','--location','--user-agent','Mozilla/5.0',url,'--output',str(out)],check=True)
 assert out.read_bytes()[:2]==b'\xff\xd8','Invalid image '+str(out)
 return {'file':str(out.relative_to(ROOT/'public')),'url':url,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'license':'CC-BY-4.0','attribution':'Solar System Scope / INOVE; maps based on NASA imagery; https://www.solarsystemscope.com/textures/'}
def main():
 DEST.mkdir(parents=True,exist_ok=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:records=list(pool.map(fetch,FILES.items()))
 from PIL import Image
 rng=random.Random(42);h,w=1024,2048;rgb=bytearray();bump=bytearray()
 for y in range(h):
  for x in range(w):
   pebble=(math.cos(x*.83+math.sin(y*.4))+math.sin(y*1.14+math.cos(x*.37)))*.25
   tone=min(1,max(0,.5+.3*pebble+rng.gauss(0,.04)))
   rgb.extend((int(150+tone*65),int(55+tone*45),int(16+tone*22)));bump.append(int(tone*255))
 Image.frombytes('RGB',(w,h),bytes(rgb)).save(DEST/'basketball.png')
 Image.frombytes('L',(w,h),bytes(bump)).save(DEST/'basketball-bump.png')
 for name in ['basketball.png','basketball-bump.png']:
  p=DEST/name;records.append({'file':str(p.relative_to(ROOT/'public')),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'license':'original project procedural texture','seed':42})
 (DEST.parent/'asset-manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
 print('Prepared',len(records),'local textures; no runtime network.')
if __name__=='__main__':main()
