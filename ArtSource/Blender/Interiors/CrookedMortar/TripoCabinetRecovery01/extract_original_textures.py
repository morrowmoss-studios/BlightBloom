"""Extract embedded bytes unchanged; never recompress the original 4K source artwork."""
from pathlib import Path
import struct,json,hashlib
D=Path(__file__).resolve().parent;p=D.parent/'TripoImports/rustic wooden cabinet 3d model.glb';b=p.read_bytes();n=struct.unpack_from('<I',b,12)[0];j=json.loads(b[20:20+n]);binary=b[28+n:];r={};(D/'Textures').mkdir(exist_ok=True)
for im in j['images']:
 v=j['bufferViews'][im['bufferView']];data=binary[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']];(D/'Textures'/im['name']).write_bytes(data);r[im['name']]={'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
(D/'TextureManifest.json').write_text(json.dumps(r,indent=2))
