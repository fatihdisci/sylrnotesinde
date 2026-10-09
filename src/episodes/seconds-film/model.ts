import type {Episode} from '../types';
/** Events are cue starts measured from each real M1 WAV, not guessed seconds. */
export const filmEvents = (episode: Episode) => {
  const study=episode.kind==='motion-study';
  const at=(i:number) => episode.captions[i].from;
  const offset=episode.id==='motion-study-15'?1:0;
  const shortAt=(i:number)=>at(i+offset);
  return study ? {clock:0,days:shortAt(1),pack:shortAt(2)-10,zoom:shortAt(2),field:shortAt(3),group:shortAt(4),years:shortAt(3),ribbon:null,result:shortAt(4)+18} :
    {clock:at(3),days:at(5),pack:at(8),zoom:at(9),field:at(10),group:at(12),years:at(14),ribbon:at(15),result:at(17)};
};
export const unitSeconds=1_000_000;
export const blockCount=1000;
export const days=unitSeconds/86400;
export const years=unitSeconds*blockCount/(86400*365.25);
