/** All geometry and distances share metres. NASA diameters / mean orbital distances. */
export const SUN_DIAMETER_KM = 1_391_400;
export const MODEL_SUN_DIAMETER_M = .24;
export const metres = (kilometres: number) => kilometres * MODEL_SUN_DIAMETER_M / SUN_DIAMETER_KM;
export const scaleModel = Object.freeze({
 sun: {diameter: .24, distance: 0},
 earth: {diameter: metres(12_756), distance: metres(149_600_000)},
 moon: {diameter: metres(3_474.8), distance: metres(384_400)},
 jupiter: {diameter: metres(142_984), distance: metres(778_500_000)},
 neptune: {diameter: metres(49_528), distance: metres(4_515_000_000)},
});
export type V3 = [number,number,number];
export const centre = (distance: number): V3 => [0,1.3,-distance];
export const positions = {
 sun: centre(0), earth: centre(scaleModel.earth.distance),
 moon: [scaleModel.moon.distance,1.3,-scaleModel.earth.distance] as V3,
 jupiter: centre(scaleModel.jupiter.distance), neptune: centre(scaleModel.neptune.distance),
};
export const SCALE_NOTE = '24 cm Güneş • tek doğrusal ölçek';
export const PLACEMENT_NOTE = 'Ortalama uzaklıklar • doğrusal yerleşim';
