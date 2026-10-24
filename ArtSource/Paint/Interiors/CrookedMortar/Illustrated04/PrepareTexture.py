from pathlib import Path
from PIL import Image
D=Path(__file__).resolve().parent
R=D.parents[4]
im=Image.open(D/'CM_Illustrated04_Master.png');w,h=im.size
im.crop((int(w*.57),int(h*.58),int(w*.90),int(h*.90))).save(R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/Illustrated04/Textures/CM_Illustrated04_QuietPlaster.png')
# Central broad plaster brushwork crop deliberately excludes exposed masonry corners.
