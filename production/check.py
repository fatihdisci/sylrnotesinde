import argparse,json
from core import verify_current
p=argparse.ArgumentParser();p.add_argument('--id',required=True);p.add_argument('--release',action='store_true');a=p.parse_args()
data,manifest=verify_current(a.id,a.release)
print(json.dumps({'valid':True,'mode':'publication' if a.release else 'draft','reviewStatus':data['review']['status'],'frames':manifest['durationInFrames']}))
