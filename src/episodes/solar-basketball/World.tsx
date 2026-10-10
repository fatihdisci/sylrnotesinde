import {useEffect,useLayoutEffect,useMemo,useRef,useState} from 'react';
import {ThreeCanvas} from '@remotion/three';
import {useThree} from '@react-three/fiber';
import {staticFile,delayRender,continueRender,cancelRender} from 'remotion';
import * as THREE from 'three';
import type {Episode} from '../types';
import {anchor,cameraPose,phase} from './camera';
import {positions,scaleModel,type V3} from './model';
const path=(name:string)=>staticFile(`episodes/solar-basketball/textures/${name}`);
const Camera=({f,episode}:{f:number;episode:Episode})=>{
 const {camera}=useThree(),p=cameraPose(f,episode);
 useLayoutEffect(()=>{camera.position.set(...p.eye);camera.lookAt(...p.target);(camera as THREE.PerspectiveCamera).fov=p.fov;camera.updateProjectionMatrix();},[camera,p.eye,p.target,p.fov]);return null;
};
const Maps=({f,episode,maps}:{f:number;episode:Episode;maps:THREE.Texture[]})=>{
 const a=(id:string)=>anchor(episode,id),morph=phase(f,a('ball-size')+32,a('earth-size')-10);
 const seams=useMemo(()=>[0,Math.PI/2,Math.PI/4,-Math.PI/4].map((angle,i)=>{
  const points=Array.from({length:129},(_,j)=>{const t=j/128*Math.PI*2;return new THREE.Vector3(.12015*Math.cos(t),.12015*Math.sin(t),0).applyAxisAngle(new THREE.Vector3(0,1,0),angle+(i>1?.32:0));});
  return new THREE.TubeGeometry(new THREE.CatmullRomCurve3(points),128,.00065,5,true);
 }),[]);
 return <>
  <group position={positions.sun} rotation={[.14,f*.0018,.12]}>
   <mesh><sphereGeometry args={[.12,96,64]}/><meshStandardMaterial map={maps[0]} bumpMap={maps[1]} bumpScale={.00055} roughness={.84}/></mesh>
   {morph<1&&seams.map((g,i)=><mesh key={i} geometry={g}><meshStandardMaterial color="#24140e" roughness={.87} transparent opacity={1-morph} depthWrite={false}/></mesh>)}
   {morph>0&&<mesh><sphereGeometry args={[.12003,96,64]}/><meshBasicMaterial map={maps[2]} color="#ffd08a" transparent opacity={morph} depthWrite={false}/></mesh>}
  </group>
  <Planet position={positions.earth} diameter={scaleModel.earth.diameter} map={maps[3]} f={f} rotation={.5}/>
  <mesh position={positions.earth} rotation={[0,f*.0005+.5,0]}><sphereGeometry args={[scaleModel.earth.diameter*.502,64,48]}/><meshStandardMaterial color="#f2f2f2" alphaMap={maps[4]} transparent opacity={.55} depthWrite={false} roughness={1}/></mesh>
  <Planet position={positions.moon} diameter={scaleModel.moon.diameter} map={maps[5]} f={f} rotation={1}/>
  <Planet position={positions.jupiter} diameter={scaleModel.jupiter.diameter} map={maps[6]} f={f} rotation={-1.4}/>
  <Planet position={positions.neptune} diameter={scaleModel.neptune.diameter} map={maps[7]} f={f} rotation={.4}/>
  {(['earth','moon','jupiter','neptune'] as const).map(name=><group key={name} position={positions[name]}>
   <mesh position={[0,-.013,0]}><cylinderGeometry args={[.00004,.000045,.026,8]}/><meshStandardMaterial color="#7b8791" metalness={.9} roughness={.25}/></mesh>
  </group>)}
 </>;
};
const Planet=({position,diameter,map,f,rotation}:{position:V3;diameter:number;map:THREE.Texture;f:number;rotation:number})=><mesh position={position} rotation={[.08,rotation+f*.00065,.03]}><sphereGeometry args={[diameter/2,80,56]}/><meshStandardMaterial map={map} roughness={.78} metalness={.02}/></mesh>;
/** Original architecture. Buildings are environment, never quantity marks. */
const City=()=>{
 const ref=useRef<THREE.InstancedMesh>(null),windows=useRef<THREE.InstancedMesh>(null),roofs=useRef<THREE.InstancedMesh>(null);
 const buildings=useMemo(()=>Array.from({length:1584},(_,i)=>{
  const side=i%2?1:-1,row=Math.floor(i/18),lane=Math.floor(i%18/2),rand=(n:number)=>{const x=Math.sin(n*127.1+42)*43758.5453;return x-Math.floor(x);};
  const h=3.5+rand(i+9)*10,w=5+rand(i+16)*7,d=5+rand(i+31)*5;
  return {x:side*(10+w/2+lane*28+rand(i+70)*6),z:-row*9.7+12,h,w,d,color:['#23323b','#2e3439','#344143','#303d45'][i%4]};
 }),[]);
 useLayoutEffect(()=>{
  if(!ref.current||!windows.current||!roofs.current)return;
  const obj=new THREE.Object3D();let wi=0;
  buildings.forEach((b,i)=>{
   obj.position.set(b.x,b.h/2,b.z);obj.scale.set(b.w,b.h,b.d);obj.updateMatrix();ref.current!.setMatrixAt(i,obj.matrix);ref.current!.setColorAt(i,new THREE.Color(b.color));
   obj.position.set(b.x,b.h+.07,b.z);obj.scale.set(b.w+.3,.14,b.d+.3);obj.updateMatrix();roofs.current!.setMatrixAt(i,obj.matrix);
   for(let level=0;level<3;level++)for(let col=0;col<3;col++){
    obj.position.set(b.x+(col-1)*b.w*.23,1.25+level*(b.h-2)/3,b.z+b.d/2+.012);obj.scale.set(b.w*.12,.6,1);obj.updateMatrix();windows.current!.setMatrixAt(wi++,obj.matrix);
   }
  });ref.current.instanceMatrix.needsUpdate=true;if(ref.current.instanceColor)ref.current.instanceColor.needsUpdate=true;windows.current.instanceMatrix.needsUpdate=true;roofs.current.instanceMatrix.needsUpdate=true;
 },[buildings]);
 return <group>
  <mesh rotation={[-Math.PI/2,0,0]} position={[0,-.03,-410]}><planeGeometry args={[620,920]}/><meshStandardMaterial color="#19272d" roughness={.95}/></mesh>
  <mesh rotation={[-Math.PI/2,0,0]} position={[0,0,-405]}><planeGeometry args={[12,890]}/><meshStandardMaterial color="#101b22" roughness={.82} metalness={.08}/></mesh>
  {[-197,-141,-85,-29,29,85,141,197].map(s=><mesh key={`parallel-${s}`} rotation={[-Math.PI/2,0,0]} position={[s,.002,-405]}><planeGeometry args={[7,890]}/><meshStandardMaterial color="#101b22" roughness={.9}/></mesh>)}
  {Array.from({length:11},(_,i)=><mesh key={`cross-${i}`} rotation={[-Math.PI/2,0,0]} position={[0,.004,8-i*80]}><planeGeometry args={[614,5]}/><meshStandardMaterial color="#101b22" roughness={.9}/></mesh>)}
  {[-1,1].map(side=><mesh key={side} position={[side*7,.1,-405]}><boxGeometry args={[1.9,.2,890]}/><meshStandardMaterial color="#34434a" roughness={.9}/></mesh>)}
  <instancedMesh ref={ref} args={[undefined,undefined,1584]} frustumCulled={false}><boxGeometry/><meshStandardMaterial roughness={.88}/></instancedMesh>
  <instancedMesh ref={roofs} args={[undefined,undefined,1584]} frustumCulled={false}><boxGeometry/><meshStandardMaterial color="#455158" metalness={.25} roughness={.65}/></instancedMesh>
  <instancedMesh ref={windows} args={[undefined,undefined,1584*9]} frustumCulled={false}><planeGeometry/><meshBasicMaterial color="#d7aa72" transparent opacity={.58}/></instancedMesh>
  <mesh rotation={[-Math.PI/2,0,0]} position={[.38,.012,-scaleModel.neptune.distance/2]}><planeGeometry args={[.14,scaleModel.neptune.distance]}/><meshBasicMaterial color="#F07857" transparent opacity={.72}/></mesh>
  {Array.from({length:86},(_,i)=><mesh key={i} rotation={[-Math.PI/2,0,0]} position={[0,.006,-i*10+8]}><planeGeometry args={[.1,2.8]}/><meshBasicMaterial color="#829394" transparent opacity={.45}/></mesh>)}
  {Array.from({length:36},(_,i)=>{const z=12-i*24;return <group key={i}>
   {[-1,1].map(s=><group key={s} position={[s*6.1,0,z]}>
    <mesh position={[0,2.1,0]}><cylinderGeometry args={[.035,.05,4.2,6]}/><meshStandardMaterial color="#53616b" metalness={.6} roughness={.65}/></mesh>
    <mesh position={[-s*.35,4.2,0]}><boxGeometry args={[.8,.07,.2]}/><meshBasicMaterial color="#ffe3ac"/></mesh>
    <mesh rotation={[-Math.PI/2,0,0]} position={[-s*.7,.008,0]}><circleGeometry args={[2.2,24]}/><meshBasicMaterial color="#d0a45f" transparent opacity={.055} depthWrite={false}/></mesh>
   </group>)}
  </group>;})}
  {(['sun','earth','jupiter','neptune'] as const).map(name=><group key={name} position={[0,0,positions[name][2]]}>
   <mesh position={[0,.575,0]}><cylinderGeometry args={[name==='sun'?.19:.14,.23,1.15,32]}/><meshStandardMaterial color="#25353e" metalness={.4} roughness={.38}/></mesh>
   <mesh rotation={[-Math.PI/2,0,0]} position={[0,.014,0]}><ringGeometry args={[.55,.57,64]}/><meshBasicMaterial color={name==='sun'?'#F07857':'#9DBFCA'}/></mesh>
  </group>)}
 </group>;
};
const Stars=()=>{
 const positions=useMemo(()=>{const a=new Float32Array(360*3);for(let i=0;i<360;i++){const az=i*2.399963,el=.08+((i*37)%359)/359*.9,r=1600;a[i*3]=Math.cos(az)*Math.cos(el)*r;a[i*3+1]=Math.sin(el)*r;a[i*3+2]=Math.sin(az)*Math.cos(el)*r-380;}return a;},[]);
 return <points><bufferGeometry><bufferAttribute attach="attributes-position" args={[positions,3]}/></bufferGeometry><pointsMaterial color="#9DBFCA" size={1.2} sizeAttenuation={false} transparent opacity={.45} fog={false}/></points>;
};
const TextureCommit=({maps,handle}:{maps:THREE.Texture[];handle:number})=>{
 const {advance}=useThree();
 useLayoutEffect(()=>{if(maps.length){advance(0);continueRender(handle);}},[maps,handle,advance]);return null;
};
const World=({f,episode,maps,handle}:{f:number;episode:Episode;maps:THREE.Texture[];handle:number})=>{
 const pose=cameraPose(f,episode),distance=new THREE.Vector3(...pose.eye).distanceTo(new THREE.Vector3(...pose.target));
 return <>
 <color attach="background" args={['#0c151c']}/>
 <fog attach="fog" args={['#0c151c',distance*1.5,distance*18]}/>
 <Camera f={f} episode={episode}/>
 <ambientLight intensity={.16}/><hemisphereLight args={['#d6edff','#202c2a',.55]}/>
 <directionalLight position={[-4,6,8]} color="#ffe3bc" intensity={3.5}/>
 <directionalLight position={[5,2,-10]} color="#93c5e2" intensity={1.6}/>
 <City/><Stars/>{maps.length>0&&<Maps f={f} episode={episode} maps={maps}/>}<TextureCommit maps={maps} handle={handle}/>
</>;};
export const SolarWorld=({f,episode}:{f:number;episode:Episode})=>{
 const [maps,setMaps]=useState<THREE.Texture[]>([]);
 const [handle]=useState(()=>delayRender('Prepare local solar textures'));
 useEffect(()=>{
  let alive=true;
  const loader=new THREE.TextureLoader();
  void Promise.all(['basketball.png','basketball-bump.png','sun.jpg','earth.jpg','clouds.jpg','moon.jpg','jupiter.jpg','neptune.jpg'].map(n=>loader.loadAsync(path(n)))).then(textures=>{
   textures.forEach((t,i)=>{t.colorSpace=i===1||i===4?THREE.NoColorSpace:THREE.SRGBColorSpace;t.anisotropy=8;});
   if(alive)setMaps(textures);
  }).catch(cancelRender);
  return ()=>{alive=false;};
 },[]);
 return <ThreeCanvas width={1080} height={1920} dpr={1} gl={{antialias:true,alpha:false,powerPreference:'high-performance',logarithmicDepthBuffer:true}} camera={{near:.00001,far:4000,fov:44}}><World f={f} episode={episode} maps={maps} handle={handle}/></ThreeCanvas>;
};
