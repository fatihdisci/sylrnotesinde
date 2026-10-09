import {Html5Audio, Sequence, staticFile} from 'remotion';
export type SoundEvent = {id: string; frame: number; path: string; durationInFrames: number; gain: number};
/** Pre-generated local assets, scheduled on the same authored frames as geometry. */
export const EventSoundTrack = ({events}: {events: readonly SoundEvent[]}) => <>{events.map(e =>
  <Sequence key={e.id} from={e.frame} durationInFrames={e.durationInFrames} layout="none">
    <Html5Audio src={staticFile(e.path)} volume={f => e.gain*Math.min(1,f/2,(e.durationInFrames-f)/5)} />
  </Sequence>)}</>;
