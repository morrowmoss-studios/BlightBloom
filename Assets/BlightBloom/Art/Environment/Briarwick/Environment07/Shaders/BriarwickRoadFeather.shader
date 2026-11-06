Shader "BlightBloom/Environment07/RoadFeather"
{
 Properties {
  _BaseMap("Soft earth diffuse",2D)="white"{}
  _BaseColor("Earth tint",Color)=(1.18,1.15,1.08,1)
  _WorldTile("World metres per tile",Float)=8
  _WorldOffset("Terrain UV world offset",Vector)=(160,170,0,0)
  _FeatherStart("Edge feather start",Range(0,1))=.65
  _RoadKind("Foot0 Cart1 Common2",Float)=0
 }
 SubShader {
  Tags {"RenderPipeline"="UniversalPipeline" "RenderType"="TransparentCutout" "Queue"="Geometry+20"}
  Pass {
   Name "RoadForward"
   Tags {"LightMode"="UniversalForward"}
   Blend SrcAlpha OneMinusSrcAlpha
   ZWrite On
   Cull Back
   HLSLPROGRAM
   #pragma vertex vert
   #pragma fragment frag
   #pragma target 3.5
   #pragma multi_compile_instancing
   #pragma multi_compile_fog
   #pragma multi_compile _ _MAIN_LIGHT_SHADOWS _MAIN_LIGHT_SHADOWS_CASCADE _MAIN_LIGHT_SHADOWS_SCREEN
   #pragma multi_compile _ _ADDITIONAL_LIGHTS_VERTEX _ADDITIONAL_LIGHTS
   #pragma multi_compile _ _CLUSTER_LIGHT_LOOP
   #pragma multi_compile_fragment _ _ADDITIONAL_LIGHT_SHADOWS
   #pragma multi_compile_fragment _ _SHADOWS_SOFT _SHADOWS_SOFT_LOW _SHADOWS_SOFT_MEDIUM _SHADOWS_SOFT_HIGH
   #pragma multi_compile_fragment _ _SCREEN_SPACE_OCCLUSION
   #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
   #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"
   TEXTURE2D(_BaseMap); SAMPLER(sampler_BaseMap);
   CBUFFER_START(UnityPerMaterial)
    float4 _BaseMap_ST;float4 _WorldOffset; half4 _BaseColor; float _WorldTile; float _FeatherStart; float _RoadKind;
   CBUFFER_END
   struct Attributes {float4 positionOS:POSITION;float3 normalOS:NORMAL;float2 road:TEXCOORD1;UNITY_VERTEX_INPUT_INSTANCE_ID};
   struct Varyings {float4 positionCS:SV_POSITION;float3 positionWS:TEXCOORD0;half3 normalWS:TEXCOORD1;float2 road:TEXCOORD2;half fog:TEXCOORD3;UNITY_VERTEX_INPUT_INSTANCE_ID UNITY_VERTEX_OUTPUT_STEREO};
   float Hash(float2 p){return frac(sin(dot(p,float2(127.1,311.7)))*43758.5453);}
   float Noise(float2 p){float2 i=floor(p),f=frac(p);f=f*f*(3-2*f);return lerp(lerp(Hash(i),Hash(i+float2(1,0)),f.x),lerp(Hash(i+float2(0,1)),Hash(i+1),f.x),f.y);}
   Varyings vert(Attributes v){Varyings o=(Varyings)0;UNITY_SETUP_INSTANCE_ID(v);UNITY_TRANSFER_INSTANCE_ID(v,o);UNITY_INITIALIZE_VERTEX_OUTPUT_STEREO(o);VertexPositionInputs p=GetVertexPositionInputs(v.positionOS.xyz);o.positionCS=p.positionCS;o.positionWS=p.positionWS;o.normalWS=TransformObjectToWorldNormal(v.normalOS);o.road=v.road;o.fog=ComputeFogFactor(p.positionCS.z);return o;}
   half4 frag(Varyings i):SV_Target {
    UNITY_SETUP_INSTANCE_ID(i);UNITY_SETUP_STEREO_EYE_INDEX_POST_VERTEX(i);
    float broad=Noise(i.positionWS.xz*.17),edgeNoise=(Noise(i.positionWS.xz*2.3)-.5)*.11;
    float edge=_RoadKind>1.5?i.road.x:abs(i.road.x*2-1);
    half alpha=1-smoothstep(_FeatherStart,1,edge+edgeNoise);clip(alpha-.003);
    half3 earth=SAMPLE_TEXTURE2D(_BaseMap,sampler_BaseMap,(i.positionWS.xz+_WorldOffset.xy)/_WorldTile).rgb*_BaseColor.rgb;
    earth*=lerp(.94,1.045,broad);
    // Shallow, irregular visual wheel wear only on rural cart routes; no physical trench.
    float ruts=exp(-pow((edge-.47)/.105,2))*lerp(.45,1,Noise(i.positionWS.xz*.48));
    float rural=1-smoothstep(38,54,abs(i.positionWS.z));rural=1-rural;
    if(_RoadKind>.5&&_RoadKind<1.5)earth*=1-ruts*rural*.075;
    InputData d=(InputData)0;d.positionWS=i.positionWS;d.normalWS=NormalizeNormalPerPixel(i.normalWS);d.viewDirectionWS=GetWorldSpaceNormalizeViewDir(i.positionWS);d.shadowCoord=TransformWorldToShadowCoord(i.positionWS);d.bakedGI=SampleSH(d.normalWS);d.shadowMask=half4(1,1,1,1);d.normalizedScreenSpaceUV=GetNormalizedScreenSpaceUV(i.positionCS);d.vertexLighting=VertexLighting(i.positionWS,d.normalWS);
    SurfaceData s=(SurfaceData)0;s.albedo=earth;s.normalTS=half3(0,0,1);s.metallic=0;s.specular=0;s.smoothness=0;s.occlusion=1;s.alpha=1;
    half4 color=UniversalFragmentPBR(d,s);color.rgb=MixFog(color.rgb,i.fog);color.a=alpha;return color;
   }
   ENDHLSL
  }
 }
 FallBack Off
}
