import type {CSSProperties, ReactNode} from 'react';
import {safeArea, video} from '../brand/tokens';
/** Optional screen-space stage. Camera transforms belong inside the geometry child. */
export const SceneSpace = ({children, mode = 'object', style}: {children: ReactNode; mode?: 'object' | 'comparison' | 'journey'; style?: CSSProperties}) => <div data-scene-layout={mode} style={{position: 'absolute', left: safeArea.left, top: 620, width: video.width - safeArea.left - safeArea.right, height: 700, ...style}}>{children}</div>;
