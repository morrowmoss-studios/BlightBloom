"""Editable code-native sign artwork: deliberate lettering and mortar/herb emblem."""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
out=Path(__file__).resolve().parents[5]/'Assets/BlightBloom/Art/Architecture/CrookedMortar/StyledProof06/Textures'
im=Image.new('RGBA',(1024,768),(229,211,163,255));d=ImageDraw.Draw(im)
d.rounded_rectangle((18,18,1006,750),radius=95,fill='#d8be88',outline='#59412b',width=23);d.rounded_rectangle((45,45,979,723),radius=75,fill='#e5d3a3',outline='#92724a',width=5)
font='/System/Library/Fonts/Supplemental/Georgia.ttf'
def text(y,s,size):
 f=ImageFont.truetype(font,size);b=d.textbbox((0,0),s,font=f);d.text(((1024-(b[2]-b[0]))/2,y),s,font=f,fill='#453725')
text(65,'The Crooked',90);text(540,'Mortar',120)
# Mortar with intentionally simplified painted silhouette and medicinal sprig.
d.line([(536,386),(646,248)],fill='#796044',width=43);d.ellipse((622,226,665,269),fill='#91744e')
d.polygon([(332,365),(684,365),(651,465),(584,502),(434,502),(365,465)],fill='#8a7954',outline='#4c5638',width=8);d.arc((326,338,690,399),0,180,fill='#b5aa73',width=17)
d.line([(250,480),(218,410),(223,320),(271,254)],fill='#617444',width=10)
for y in [302,350,398,440]:
 d.ellipse((177,y-23,229,y+5),fill='#7f8d51');d.ellipse((223,y-36,277,y-8),fill='#879452')
d.line([(778,480),(809,404),(799,318),(761,262)],fill='#617444',width=10)
for y in [303,350,398,440]:
 d.ellipse((800,y-22,849,y+5),fill='#7f8d51');d.ellipse((748,y-36,802,y-8),fill='#879452')
im.save(out/'CM_CrookedMortarSign06.png')
