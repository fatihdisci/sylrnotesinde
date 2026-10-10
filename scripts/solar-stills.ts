import {bundle} from '@remotion/bundler';
import {renderStill,selectComposition} from '@remotion/renderer';
import {mkdirSync} from 'node:fs';
const serveUrl=await bundle({entryPoint:'src/index.ts'});
const composition=await selectComposition({serveUrl,id:'Episode-solar-basketball',chromiumOptions:{gl:'angle'}});
mkdirSync('renders/episodes/solar-basketball/lookdev',{recursive:true});
for(const frame of (process.argv.length>2?process.argv.slice(2).map(Number):[0,75,220,360,590,730,980,1060,1160,1320,1410,1540,1690,1820])){
 await renderStill({serveUrl,composition:{...composition,props:{...composition.props,debug:true}},frame,output:`renders/episodes/solar-basketball/lookdev/${frame}.png`,chromiumOptions:{gl:'angle'},inputProps:{debug:true},onBrowserLog:log=>{if(log.text.includes('LAYOUT_AUDIT:'))console.log(frame,log.text);}});
 console.log('Frame',frame);
}
