import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';
import {typography} from './tokens';
export const fontFiles = [
  {family: typography.sans, weight: '400', file: 'IBMPlexSans-Regular.woff2'},
  {family: typography.sans, weight: '500', file: 'IBMPlexSans-Medium.woff2'},
  {family: typography.sans, weight: '600', file: 'IBMPlexSans-SemiBold.woff2'},
  {family: typography.mono, weight: '400', file: 'IBMPlexMono-Regular.woff2'},
  {family: typography.mono, weight: '500', file: 'IBMPlexMono-Medium.woff2'},
] as const;
// loadFont blocks rendering; failed assets reject instead of silently substituting.
export const fontsReady = Promise.all(fontFiles.map(({family, weight, file}) =>
  loadFont({family, weight, url: staticFile(`fonts/${file}`)}),
));
