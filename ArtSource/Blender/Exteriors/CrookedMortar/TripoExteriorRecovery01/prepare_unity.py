from pathlib import Path
from PIL import Image
import shutil,json,hashlib
D=Path(__file__).resolve().parent;ROOT=D.parents[4];A=ROOT/'Assets/BlightBloom/Art/Exteriors/CrookedMortar/TripoExteriorRecovery01'
for name in ['Models','Textures','Materials','Prefabs']: (A/name).mkdir(parents=True,exist_ok=True)
shutil.copy2(D/'Exports/CM_CrookedMortar_ExteriorRecovery01.fbx',A/'Models/CM_CrookedMortar_ExteriorRecovery01.fbx')
for src,dest in [('Original_00.jpg','House_BaseColor.jpg'),('Original_02.png','House_Normal.png'),('Sign_ApprovedWalnut.png','Sign_Walnut.png')]:shutil.copy2(D/'Textures'/src,A/'Textures'/dest)
im=Image.open(D/'Textures/Original_01.jpg').convert('RGB');r,g,b=im.split();inv=g.point(lambda n:255-n);zero=r.point(lambda n:0);Image.merge('RGBA',(b,zero,zero,inv)).save(A/'Textures/House_MetallicSmoothness.png')
paths=['Assets/Scenes/CM_CrookedMortar_Production02.unity','Assets/Scenes/CM_CrookedMortar_B_StyledDetails07.unity','Assets/Scenes/CM_CrookedMortar_ShopWorkflow14_Review.unity'];(D/'ProtectedSceneHashes.json').write_text(json.dumps({p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths if (ROOT/p).exists()},indent=2));print(A)
