import type {Episode} from './types';
import prepared from '../../public/episodes/production-check/narration-manifest.json';
import {ProductionCheck} from './production-check/Scenes';
/** Add a new authored TSX scene here; render/QA scripts stay unchanged. */
export const episodes = [{episode: prepared as Episode, component: ProductionCheck}];
