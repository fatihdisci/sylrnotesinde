export type DirectedEvent = {id:string;from:number;to:number;information:string;visual:string;camera:string;animation:string;effects:readonly {sound:string;frame:number;durationFrames:number;gain:number}[]};
export type AudioDirection = {storyboardHash:string;idea:string;events:readonly DirectedEvent[];speech:{onsetMs:number;offsetMs:number;audioDurationMs:number;listeningVerified:boolean}};
/** Authored meaning is resolved to measured word frames during import/export. */
export const eventFrames = (direction:AudioDirection) => Object.fromEntries(direction.events.map(e=>[e.id,e.from])) as Record<string,number>;
