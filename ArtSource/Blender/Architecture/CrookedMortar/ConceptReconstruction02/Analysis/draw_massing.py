"""Pre-construction architectural interpretation diagram; no reference pixels altered."""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,json
out=Path(__file__).parent
im=Image.new('RGB',(1800,1200),'#f0ede4');d=ImageDraw.Draw(im)
font='/System/Library/Fonts/Supplemental/Arial.ttf'
def F(n):return ImageFont.truetype(font,n)
colors={'A':'#adbfc5','B':'#c1b3cf','C':'#c8b698','D':'#a8bc9d','P':'#d7bd86','F':'#b8aba0'}
def text(p,s,n=22,fill='#28353b'):d.text(p,s,font=F(n),fill=fill)
text((45,25),'THE CROOKED MORTAR — CONCEPT MASSING INTERPRETATION',34)
text((45,75),'Visible roof hierarchy first; rear dimensions are inferred for a compact playable two-storey house.',23)
# Pinhole projection matching the illustration's front + right-side view.
eye=(18,6,-20);target=(1,4.7,1)
def sub(a,b):return tuple(a[i]-b[i] for i in range(3))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def norm(a):return tuple(v/math.sqrt(dot(a,a)) for v in a)
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
f=norm(sub(target,eye));right=norm(cross((0,1,0),f));up=cross(f,right)
def project(v):
 rel=sub(v,eye);z=dot(rel,f);return (530+dot(rel,right)/z*1200,500-dot(rel,up)/z*1200)
faces=[]
def poly(vs,color):faces.append((sum(dot(sub(v,eye),f) for v in vs)/len(vs),vs,color))
def block(x0,x1,z0,z1,h,col):
 poly([(x0,0,z0),(x1,0,z0),(x1,h,z0),(x0,h,z0)],col)
 poly([(x1,0,z0),(x1,0,z1),(x1,h,z1),(x1,h,z0)],col)
def roof(profile,z0,z1,col):
 poly([(x,y,z0) for x,y in profile],col)
 for (x,y),(xx,yy) in zip(profile,profile[1:]):poly([(x,y,z0),(x,y,z1),(xx,yy,z1),(xx,yy,z0)],col)
block(-2.8,2.8,-3,4.8,6.15,'#d4dde0')
roof([(-3.25,5.92),(-2.7,6.22),(-1.45,8.75),(-.35,10.25),(.55,9.15),(2.35,6.52),(3.3,5.96)],-3.65,5.15,colors['A'])
block(2.8,6,1.8,6.8,5.55,'#dfd3c1');roof([(2.45,5.4),(3,5.75),(4.35,7.55),(5.7,5.8),(6.35,5.4)],1.45,7.1,colors['C'])
block(2.8,5.5,-1.1,1.8,3.05,'#d2ddcb')
block(1.45,2.35,3.4,4.3,11.2,colors['F']);block(-1.8,-1.25,2.9,3.45,10.3,colors['F'])
poly([(2.65,4.0,-1.4),(2.65,4.0,2.0),(5.8,3.02,2.0),(5.8,3.02,-1.4)],colors['D'])
# Real porch canopy and open columns; front wall remains recessed behind it.
poly([(-3.5,4.0,-2.95),(3.5,4.0,-2.95),(3.5,3.05,-5.4),(-3.5,3.05,-5.4)],colors['P'])
# Roof dormer across the main slope (not a full house-width cross wing).
poly([(3.18,6.45,-.35),(3.18,6.45,1.45),(3.18,8.05,.55)],colors['B'])
poly([(.8,8.05,.55),(3.4,8.05,.55),(3.4,6.75,-.45),(.8,6.75,-.45)],colors['B'])
for _,vs,c in sorted(faces,reverse=True):d.polygon([project(v) for v in vs],fill=c,outline='#49545a',width=2)
for x in [-3.05,3.05]:d.line([project((x,.2,-5.1)),project((x,3.0,-5.1))],fill='#6b5945',width=9)
for label,point in [('A',(-1.1,8.3,-1)),('B',(3.4,7.55,.5)),('C',(4.9,6.5,4.5)),('D',(4.9,3.45,.1)),('P',(-1,3.4,-4.3)),('F',(1.9,11.2,3.9))]:
 x,y=project(point);d.ellipse((x-20,y-20,x+20,y+20),fill=colors[label],outline='#28353b',width=2);text((x-9,y-15),label,25)
text((65,800),'Three-quarter interpretation: front gable at left, long roof side at right.',21)
# Plan view / ridge directions.
ox,oy,scale=1300,420,40
text((1070,140),'ROOF / FOOTPRINT PLAN',25)
def planbox(key,bounds):
 x0,z0,x1,z1=bounds;box=(ox+x0*scale,oy+z0*scale,ox+x1*scale,oy+z1*scale);d.rectangle(box,fill=colors[key],outline='#35434a',width=3);text((box[0]+10,box[1]+8),key,26)
planbox('A',(-2.8,-3,2.8,4.8));planbox('C',(2.8,1.8,6,6.8));planbox('D',(2.8,-1.1,5.5,1.8));planbox('P',(-3.15,-5.2,3.15,-3));planbox('B',(.8,-.45,3.4,1.45))
def arrow(a,b,c='#34464e'):
 d.line((a,b),fill=c,width=5);ang=math.atan2(b[1]-a[1],b[0]-a[0]);pts=[b,(b[0]-17*math.cos(ang-.45),b[1]-17*math.sin(ang-.45)),(b[0]-17*math.cos(ang+.45),b[1]-17*math.sin(ang+.45))];d.polygon(pts,fill=c)
arrow((ox-.35*scale,oy-2.7*scale),(ox-.35*scale,oy+4.4*scale))
arrow((ox+4.35*scale,oy+2.1*scale),(ox+4.35*scale,oy+6.4*scale))
arrow((ox+1.0*scale,oy+.55*scale),(ox+3.3*scale,oy+.55*scale))
arrow((ox,oy-3.2*scale),(ox,oy-5.05*scale))
arrow((ox+3.0*scale,oy+.2*scale),(ox+5.4*scale,oy+.2*scale))
text((1070,730),'Arrows: A/C ridge directions; B cross-dormer ridge.',20)
text((1070,758),'P/D arrows show single-slope drainage direction.',20)
# Legend below both views, with explicit visible/inferred distinction.
legend=[('A','Dominant steep longitudinal roof + front gable — main two-storey body'),('B','Substantial dormer on the visible right slope — ridge across A'),('C','Smaller receding right gable — parallel to A, lower and narrower'),('P','Broad deep entrance porch — door recessed behind its front beam'),('D','Low projecting shop-side volume / lean-to — below upper windows'),('F','Two staggered chimney masses — taller stack behind the right roof slope')]
for i,(k,s) in enumerate(legend):
 y=855+i*40;d.rectangle((55,y,81,y+26),fill=colors[k],outline='#35434a');text((95,y-1),k+'  '+s,22)
text((55,1160),'Inference boundary: hidden rear walls, exact footprint, dormer depth and room partitions are not recoverable from one painting.',20)
im.save(out/'MassingDiagram.png')
(out/'reference_analysis.json').write_text(json.dumps({'reference':'/Users/zak/Downloads/Storybook Apothecary by the River.png','visible_hierarchy':['A dominant steep longitudinal roof with front gable','B cross-dormer on visible right slope','C lower parallel receding gabled wing','P substantial full-width front lean-to porch','D low shop-side projection'],'inferred':['rear footprint','dimensions','internal circulation','exact side projection depth'],'key_departure_from_redesign01':'No full-width transverse residential cross roof; one dominant roof with a dormer and a smaller parallel wing.'},indent=2))
