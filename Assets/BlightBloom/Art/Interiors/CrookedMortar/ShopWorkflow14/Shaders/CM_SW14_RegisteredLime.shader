Shader "BlightBloom/Workflow14/RegisteredLime"
{
 Properties {
  _BaseMap("Painted Albedo",2D)="white"{} _BaseColor("Paint Tint",Color)=(1,1,1,1)
  _AmbientStrength("Indirect Light Strength",Range(0,1))=.72
  _OcclusionStrength("Baked Cavity Strength",Range(0,1))=.65
  _Cull("Cull",Float)=2 _Cutoff("Cutoff",Float)=.5
 }
 SubShader {
  Tags {"RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" "Queue"="Geometry"}
  Pass {
   Name "PaintedForward" Tags {"LightMode"="UniversalForward"}
   Cull [_Cull]
   HLSLPROGRAM
   #pragma vertex Vert
   #pragma fragment Frag
   #pragma multi_compile _ _MAIN_LIGHT_SHADOWS _MAIN_LIGHT_SHADOWS_CASCADE _MAIN_LIGHT_SHADOWS_SCREEN
   #pragma multi_compile _ _ADDITIONAL_LIGHTS_VERTEX _ADDITIONAL_LIGHTS
   #pragma multi_compile _ _CLUSTER_LIGHT_LOOP
   #pragma multi_compile_fragment _ _ADDITIONAL_LIGHT_SHADOWS
   #pragma multi_compile_fragment _ _SHADOWS_SOFT _SHADOWS_SOFT_LOW _SHADOWS_SOFT_MEDIUM _SHADOWS_SOFT_HIGH
   #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
   #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"
   TEXTURE2D(_BaseMap);SAMPLER(sampler_BaseMap);
   CBUFFER_START(UnityPerMaterial)
    float4 _BaseMap_ST;half4 _BaseColor;half _AmbientStrength;half _OcclusionStrength;float _Cull;float _Cutoff;
   CBUFFER_END
   struct A{float4 pos:POSITION;float3 normal:NORMAL;float2 uv:TEXCOORD0;half4 color:COLOR;};
   struct V{float4 pos:SV_POSITION;float3 ws:TEXCOORD0;half3 normal:TEXCOORD1;float2 uv:TEXCOORD2;half cavity:TEXCOORD3;};
   V Vert(A a){V o;VertexPositionInputs p=GetVertexPositionInputs(a.pos.xyz);o.pos=p.positionCS;o.ws=p.positionWS;o.normal=TransformObjectToWorldNormal(a.normal);o.uv=TRANSFORM_TEX(a.uv,_BaseMap);o.cavity=a.color.r;return o;}
   half4 Frag(V v):SV_Target{
    half3 n=normalize(v.normal);
    float2 paintUV=float2(abs(n.x)>abs(n.z)?v.ws.z:v.ws.x,v.ws.y*0.5)/1.8;
    half3 base=SAMPLE_TEXTURE2D(_BaseMap,sampler_BaseMap,paintUV).rgb*_BaseColor.rgb;
    // Broad local maintenance/edge shading, independent of triangle or module UV seams.
    half edge=0.10h*saturate(1-(v.ws.y-.2)/.45)+0.07h*saturate(1-abs(v.ws.y-3.2)/.18);
    base*=1-edge;
    half ao=lerp(1,saturate(v.cavity),_OcclusionStrength);
    InputData data=(InputData)0;data.positionWS=v.ws;data.normalWS=n;data.viewDirectionWS=GetWorldSpaceNormalizeViewDir(v.ws);data.shadowCoord=TransformWorldToShadowCoord(v.ws);data.bakedGI=SampleSH(n)*_AmbientStrength;data.normalizedScreenSpaceUV=GetNormalizedScreenSpaceUV(v.pos);data.shadowMask=half4(1,1,1,1);data.vertexLighting=VertexLighting(v.ws,n);
    SurfaceData surface=(SurfaceData)0;surface.albedo=base;surface.specular=half3(0,0,0);surface.metallic=0;surface.smoothness=.04h;surface.occlusion=ao;surface.alpha=1;
    return UniversalFragmentPBR(data,surface);
   }
   ENDHLSL
  }
  UsePass "Universal Render Pipeline/Lit/ShadowCaster"
  UsePass "Universal Render Pipeline/Lit/DepthOnly"
  UsePass "Universal Render Pipeline/Lit/DepthNormals"
 }
}
