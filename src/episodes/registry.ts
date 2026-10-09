import type {Episode} from './types';
import prepared from '../../public/episodes/production-check/narration-manifest.json';
import {ProductionCheck} from './production-check/Scenes';
import motion from '../../public/episodes/motion-study/narration-manifest.json';
import {MotionStudy} from './motion-study/Scenes';
import film from '../../public/episodes/seconds-film/narration-manifest.json';
import {SecondsFilm} from './seconds-film/Scenes';
import study15 from '../../public/episodes/motion-study-15/narration-manifest.json';
import {MotionStudy15} from './motion-study-15/Scenes';
import minimax from '../../public/episodes/seconds-film-minimax/narration-manifest.json';
import {SecondsFilmMinimax} from './seconds-film-minimax/Scenes';
/** Add a new authored TSX scene here; render/QA scripts stay unchanged. */
export const episodes = [{episode: prepared as Episode, component: ProductionCheck}, {episode: motion as Episode, component: MotionStudy}, {episode: film as Episode, component: SecondsFilm}, {episode: study15 as Episode, component: MotionStudy15}, {episode: minimax as Episode, component: SecondsFilmMinimax}];
