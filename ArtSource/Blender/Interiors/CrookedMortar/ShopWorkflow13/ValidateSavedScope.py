from pathlib import Path
import re,json
D=Path(__file__).resolve().parent;R=D.parents[4]
def docs(path):
 s=(R/path).read_text();matches=list(re.finditer(r'^--- !u!(\d+) &(-?\d+).*$',s,re.M));return {m.group(2):(int(m.group(1)),s[m.end():matches[i+1].start() if i+1<len(matches) else len(s)]) for i,m in enumerate(matches)}
a=docs('Assets/Scenes/CM_CrookedMortar_ShopWorkflow12_Review.unity');b=docs('Assets/Scenes/CM_CrookedMortar_ShopWorkflow13_Review.unity')
changes=[{'fileID':k,'classID':v[0]} for k,v in a.items() if k not in b or b[k]!=v]
critical=[c for c in changes if c['classID'] in [114,143,65,64,135,136,54,20]]
r={'passed':not critical,'changedOriginalRecords':changes,'changedScriptsCameraOrColliders':critical,'addedRecords':len(set(b)-set(a))};(D/'SavedScopeValidation.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
