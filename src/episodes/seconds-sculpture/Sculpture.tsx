import {useLayoutEffect,useMemo,useRef} from 'react';
import {ThreeCanvas} from '@remotion/three';
import {useThree} from '@react-three/fiber';
import * as THREE from 'three';
import {RoundedBoxGeometry} from 'three/addons/geometries/RoundedBoxGeometry.js';
import type {Episode} from '../types';
import {anchor,blockPose,cameraPose,lerp3,mix,phase,type V3} from './choreography';
const ivory='#F2F0E9',coral='#F07857',ice='#9DBFCA';
const Cube=({position=[0,0,0],rotation=[0,0,0],scale=1,color=coral}:{position?:V3;rotation?:V3;scale?:number|V3;color?:string})=>{
 const geometry=useMemo(()=>new RoundedBoxGeometry(1,1,1,2,.045),[]);
 return <mesh geometry={geometry} position={position} rotation={rotation} scale={scale} castShadow receiveShadow><meshStandardMaterial color={color} metalness={.32} roughness={.29}/></mesh>;
};
const Camera=({f,episode}:{f:number;episode:Episode})=>{
 const {camera}=useThree();const p=cameraPose(f,episode);
 useLayoutEffect(()=>{camera.position.set(...p.eye);camera.lookAt(...p.target);(camera as THREE.PerspectiveCamera).fov=p.fov;camera.updateProjectionMatrix();},[camera,p.eye,p.target,p.fov]);return null;
};
const Thousand=({f,episode,teaser=false}:{f:number;episode:Episode;teaser?:boolean})=>{
 const ref=useRef<THREE.InstancedMesh>(null);
 const geometry=useMemo(()=>new RoundedBoxGeometry(1,1,1,2,.035),[]);
 const dummy=useMemo(()=>new THREE.Object3D(),[]);
 useLayoutEffect(()=>{
  if(!ref.current)return;
  for(let i=0;i<1000;i++){
   const p=teaser?{position:[(i%10-4.5)*1.06,(Math.floor(i/10)%10-4.5)*1.06,(Math.floor(i/100)-4.5)*1.06-12] as V3,rotation:[0,0,0] as V3,scale:phase(f,anchor(episode,'shock'),anchor(episode,'shock')+30)}:blockPose(i,f,episode);
   dummy.position.set(...p.position);dummy.rotation.set(...p.rotation);dummy.scale.setScalar(!teaser&&i===999&&f<anchor(episode,'launch')?.00001:Math.max(.00001,p.scale));dummy.updateMatrix();ref.current.setMatrixAt(i,dummy.matrix);
   ref.current.setColorAt(i,new THREE.Color(i===999?coral:(i%100===0?ivory:ice)));
  }
  ref.current.instanceMatrix.needsUpdate=true;if(ref.current.instanceColor)ref.current.instanceColor.needsUpdate=true;
 },[f,episode,teaser,dummy]);
 return <instancedMesh ref={ref} args={[geometry,undefined,1000]} frustumCulled={false} castShadow receiveShadow><meshStandardMaterial metalness={.38} roughness={.32}/></instancedMesh>;
};
const Clock=({f,episode}:{f:number;episode:Episode})=>{
 const a=(id:string)=>anchor(episode,id);const open=phase(f,a('dive'),a('clock'));
 const unwind=phase(f,a('unwind'),a('calendar')+20);
 const angle=(f-a('clock'))/30*Math.PI*2; // One sped-up revolution =60 represented seconds.
 const rotation:V3=[.05,0,Math.PI*.06];
 return <group rotation={rotation} scale={Math.max(.00001,open)}>
  <mesh position={[0,0,-.14]} rotation={[Math.PI/2,0,0]}><cylinderGeometry args={[2.22,2.22,.12,96]}/><meshStandardMaterial color="#1a2424" metalness={.65} roughness={.25}/></mesh>
  {[2.2,2.05,.27].map((r,i)=><mesh key={r} position={[0,0,i===2?.18:0]}><torusGeometry args={[r,i===2?.07:.035,8,96]}/><meshStandardMaterial color={i===2?coral:ivory} metalness={.75} roughness={.19}/></mesh>)}
  {Array.from({length:60},(_,i)=>{const rad=i/60*Math.PI*2;return <mesh key={i} position={[Math.sin(rad)*1.9,Math.cos(rad)*1.9,.03]} rotation={[0,0,-rad]} scale={[i%5===0?.036:.014,i%5===0?.23:.1,.025]}><boxGeometry/><meshStandardMaterial color={i%5===0?ivory:ice}/></mesh>;})}
  <group rotation={[0,0,-angle]} scale={1-unwind}><mesh position={[0,.85,.15]} scale={[.035,1.8,.04]}><boxGeometry/><meshStandardMaterial color={coral}/></mesh><mesh position={[0,0,.18]}><sphereGeometry args={[.12,16,12]}/><meshStandardMaterial color={coral} metalness={.6} roughness={.2}/></mesh></group>
  <group rotation={[0,0,-angle/60]} scale={1-unwind}><mesh position={[0,.52,.12]} scale={[.085,1.1,.04]}><boxGeometry/><meshStandardMaterial color={ivory}/></mesh></group>
 </group>;
};
const Days=({f,episode}:{f:number;episode:Episode})=>{
 const a=(id:string)=>anchor(episode,id);const bloom=phase(f,a('unwind'),a('calendar')+30),fold=phase(f,a('collect'),a('block')+24);
 return <group>
 {Array.from({length:12},(_,i)=>{
  const turn=i/12*Math.PI*2,ring:V3=[Math.sin(turn)*1.7,Math.cos(turn)*1.7,.12];
  const fan:V3=[(i%4-1.5)*1.6, (1-Math.floor(i/4))*2.2,.8*Math.sin(i*.6)];
  const fanP=lerp3(ring,fan,bloom);const collect=phase(f,a('collect')+i*2,a('block')+i*1.5);
  const pos=lerp3(fanP,[0,0,(i-5.5)*.045],collect);
  const size=mix(.19,1,bloom)*(1-fold*.6);
  const fill=Math.max(0,Math.min(1,1000000/86400-i));
  const painted=phase(f,a('million')+i*2.4,a('fraction')+24+i*1.2)*fill;
  return <group key={i} position={pos} rotation={[mix(-.35,.04,bloom)*(1-collect),mix(turn*.15,Math.sin(i)*.12,bloom)*(1-collect),mix(-turn,(i%4-1.5)*-.04,bloom)*(1-collect)]} scale={Math.max(.00001,size)}>
   <Cube scale={[1.28,1.8,.08]} color={ivory}/>
   <mesh position={[0,.69,.052]} scale={[1.23,.28,.025]}><boxGeometry/><meshStandardMaterial color={coral}/></mesh>
   <mesh position={[0,-.68+painted*.63,.06]} scale={[1.13,Math.max(.001,painted*1.26),.018]}><boxGeometry/><meshStandardMaterial color={coral}/></mesh>
   {Array.from({length:7},(_,j)=><mesh key={j} position={[-.43+j*.143,.35,.065]} scale={[.07,.035,.015]}><boxGeometry/><meshStandardMaterial color="#304142"/></mesh>)}
   {[0,1,2].map(j=><mesh key={j} position={[-.43,.05-j*.19,.068]} scale={[.53,.025,.008]}><boxGeometry/><meshStandardMaterial color={ice}/></mesh>)}
  </group>;
 })}
 </group>;
};
const World=({f,episode}:{f:number;episode:Episode})=>{
 const a=(id:string)=>anchor(episode,id);const clock=f>=a('dive')&&f<a('calendar')+30;const days=f>=a('unwind')&&f<a('block')+28;
 const solo=f<a('dive')||f>=a('block')&&f<a('launch');
 const opening=phase(f,0,40),fold=phase(f,a('block'),a('block')+28);
 const unitScale=f<a('dive')?mix(1.9,1.15,opening):mix(.5,1,fold);
 return <>
  <color attach="background" args={['#10191b']}/><fog attach="fog" args={['#10191b',30,105]}/>
  <Camera f={f} episode={episode}/>
  <ambientLight intensity={.38}/><hemisphereLight args={['#d9f4ff','#171e1c',.9]}/>
  <directionalLight position={[-8,12,10]} color="#fff4df" intensity={3.6} castShadow shadow-mapSize={[1024,1024]} shadow-camera-left={-20} shadow-camera-right={20} shadow-camera-top={20} shadow-camera-bottom={-20} shadow-normalBias={.04}/>
  <directionalLight position={[9,3,-6]} color="#78c1df" intensity={2.8}/>
  <pointLight position={[-5,-1,5]} intensity={80} color={coral} distance={40}/>
  <mesh rotation={[-Math.PI/2,0,0]} position={[0,-6.6,0]} receiveShadow><planeGeometry args={[220,220]}/><meshStandardMaterial color="#10191b" roughness={.56} metalness={.32}/></mesh>
  {solo&&<group rotation={[(.28+f*.001)*(1-phase(f,a('block')+28,a('launch'))),(.45+f*.004)*(1-phase(f,a('block')+28,a('launch'))),.06*(1-phase(f,a('block')+28,a('launch')))]}><Cube scale={unitScale}/>{[0,1,2].map(i=><mesh key={i} position={[0,(i-1)*.22,unitScale/2+.003]} scale={[unitScale*.7,.022,.012]}><boxGeometry/><meshStandardMaterial color={ivory} metalness={.6} roughness={.3}/></mesh>)}</group>}
  {f>=a('shock')&&f<a('dive')&&<group rotation={[0,phase(f,a('shock'),a('zeros'))*.15,0]} scale={1-phase(f,a('zeros'),a('dive'))}><Thousand f={f} episode={episode} teaser/></group>}
  {f>=a('dive')&&f<a('clock')+20&&<group scale={1-phase(f,a('clock')-10,a('clock')+20)}>{Array.from({length:6},(_,i)=>{const axis=Math.floor(i/2),sign=i%2?1:-1,op=phase(f,a('dive'),a('clock'));const p:V3=[0,0,0];p[axis]=sign*(.55+op*2.2);const sc:V3=[1.1,1.1,1.1];sc[axis]=.08;const rot:V3=[0,0,0];rot[(axis+1)%3]=sign*op*1.25;return <Cube key={i} position={p} scale={sc} rotation={rot}/>;})}</group>}
  {clock&&<group scale={1-phase(f,a('calendar'),a('calendar')+30)}><Clock f={f} episode={episode}/></group>}
  {days&&<Days f={f} episode={episode}/>}
  {f>=a('launch')-16&&<Thousand f={f} episode={episode}/>}
 </>;
};
export const Sculpture=({f,episode}:{f:number;episode:Episode})=><ThreeCanvas width={1080} height={1920} dpr={1} shadows={{type:THREE.PCFShadowMap}} gl={{antialias:true,alpha:false,powerPreference:'high-performance'}} camera={{near:.08,far:250,fov:44}}><World f={f} episode={episode}/></ThreeCanvas>;
