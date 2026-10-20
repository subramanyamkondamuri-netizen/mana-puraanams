import base64,gzip,os,re,textwrap
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import unquote
ROOT=os.path.dirname(os.path.abspath(__file__))
DOCS={'Bala-Kanda.pdf':('Bala-Kanda','BALA KANDA'),'Ayodhya-Kanda.pdf':('Ayodhya-Kanda','AYODHYA KANDA'),'Aranya-Kanda.pdf':('Aranya-Kanda','ARANYA KANDA'),'Kishkindha-Kanda.pdf':('Kishkindha-Kanda','KISHKINDHA KANDA'),'Sundara-Kanda.pdf':('Sundara-Kanda','SUNDARA KANDA'),'Yuddha-Kanda.pdf':('Yuddha-Kanda','YUDDHA KANDA')}
W,H=432.,648.; CREAM=(.984,.957,.894); RED=(.58,.09,.06); GOLD=(.78,.55,.13); BROWN=(.20,.12,.06); BLUE=(.12,.32,.64); GREEN=(.15,.48,.23); ORANGE=(.92,.42,.08); SKIN=(.82,.58,.38)
def load_text(k):
 p=os.path.join(ROOT,'textdata',k+'.txt'); return gzip.decompress(base64.b64decode(open(p,encoding='ascii').read().strip())).decode('utf-8')
def hx(s): return s.encode('cp1252','replace').hex().upper()
def rgb(c): return f'{c[0]:.3f} {c[1]:.3f} {c[2]:.3f}'
def txt(x,y,s,z=10.3,b=False,c=BROWN): return f'{rgb(c)} rg BT /{"F2" if b else "F1"} {z:.2f} Tf 1 0 0 1 {x:.2f} {y:.2f} Tm <{hx(s)}> Tj ET\n'
def ln(a,b,c,d,col=BROWN,w=1): return f'{rgb(col)} RG {w:.2f} w {a:.2f} {b:.2f} m {c:.2f} {d:.2f} l S\n'
def rect(x,y,w,h,col=BROWN,lw=1,fill=None): return (f'{rgb(fill)} rg {x:.2f} {y:.2f} {w:.2f} {h:.2f} re f\n' if fill else '')+f'{rgb(col)} RG {lw:.2f} w {x:.2f} {y:.2f} {w:.2f} {h:.2f} re S\n'
def circ(x,y,r,col=BROWN,lw=1,fill=None):
 k=.55228475*r;p=f'{x+r:.2f} {y:.2f} m {x+r:.2f} {y+k:.2f} {x+k:.2f} {y+r:.2f} {x:.2f} {y+r:.2f} c {x-k:.2f} {y+r:.2f} {x-r:.2f} {y+k:.2f} {x-r:.2f} {y:.2f} c {x-r:.2f} {y-k:.2f} {x-k:.2f} {y-r:.2f} {x:.2f} {y-r:.2f} c {x+k:.2f} {y-r:.2f} {x+r:.2f} {y-k:.2f} {x+r:.2f} {y:.2f} c '
 return (f'{rgb(fill)} rg ' if fill else '')+f'{rgb(col)} RG {lw:.2f} w {p}{"B" if fill else "S"}\n'
def tri(x1,y1,x2,y2,x3,y3,col=BROWN,lw=1,fill=None): return (f'{rgb(fill)} rg ' if fill else '')+f'{rgb(col)} RG {lw:.2f} w {x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l {x3:.2f} {y3:.2f} l h {"B" if fill else "S"}\n'
def border(n=None,head=None):
 s=f'{rgb(CREAM)} rg 0 0 {W} {H} re f\n'+rect(12,12,W-24,H-24,RED,2)+rect(18,18,W-36,H-36,GOLD,.8)
 for x,y in [(24,24),(W-24,24),(24,H-24),(W-24,H-24)]: s+=circ(x,y,5,GOLD,.8)+ln(x-7,y,x+7,y,GOLD,.7)+ln(x,y-7,x,y+7,GOLD,.7)
 if head:s+=txt(118,H-32,head,10.2,True,RED)
 if n:s+=txt(W/2-3,16,str(n),8.2,False,BROWN)
 return s
def person(x,y,s=1,robe=ORANGE,crown=False,bow=False,beard=False):
 o=circ(x,y+31*s,6*s,BROWN,1,SKIN)
 if crown:o+=tri(x-6*s,y+38*s,x,y+48*s,x+6*s,y+38*s,GOLD,1,GOLD)
 if beard:o+=tri(x-5*s,y+25*s,x,y+15*s,x+5*s,y+25*s,BROWN,1,BROWN)
 o+=tri(x-10*s,y+22*s,x,y-6*s,x+10*s,y+22*s,BROWN,1,robe)
 o+=ln(x-4*s,y-6*s,x-6*s,y-20*s,BROWN,2*s)+ln(x+4*s,y-6*s,x+6*s,y-20*s,BROWN,2*s)
 o+=ln(x-7*s,y+14*s,x-17*s,y+3*s,BROWN,1.5*s)+ln(x+7*s,y+14*s,x+17*s,y+3*s,BROWN,1.5*s)
 if bow:
  o+=f'{rgb(GOLD)} RG {1.4*s:.2f} w {x+18*s:.2f} {y-8*s:.2f} m {x+34*s:.2f} {y+15*s:.2f} {x+34*s:.2f} {y+28*s:.2f} {x+18*s:.2f} {y+40*s:.2f} c S\n'+ln(x+18*s,y-8*s,x+18*s,y+40*s,GOLD,.8*s)
 return o
def tree(x,y,s=1):
 o=rect(x-3*s,y,6*s,26*s,BROWN,1,(.42,.23,.10))
 for dx,dy,r in [(0,35,14),(-10,30,10),(10,30,10),(0,45,10)]:o+=circ(x+dx*s,y+dy*s,r*s,GREEN,1,(.38,.68,.30))
 return o
def hut(x,y,s=1): return rect(x-22*s,y,44*s,28*s,BROWN,1,(.92,.78,.50))+tri(x-27*s,y+28*s,x,y+50*s,x+27*s,y+28*s,BROWN,1,(.58,.30,.12))
def fire(x,y,s=1):
 o=''
 for dx,h,c in [(-8,22,ORANGE),(0,31,GOLD),(8,20,RED)]:o+=tri(x+dx*s-6*s,y,x+dx*s,y+h*s,x+dx*s+6*s,y,BROWN,.6,c)
 return o
def palace(x,y,s=1):
 o=rect(x-30*s,y,60*s,35*s,GOLD,1,(.96,.82,.48))
 for dx in [-20,0,20]:o+=rect(x+dx*s-5*s,y,10*s,30*s,RED,.7,(.98,.93,.75))+tri(x+dx*s-9*s,y+30*s,x+dx*s,y+44*s,x+dx*s+9*s,y+30*s,GOLD,.8,GOLD)
 return o
def deer(x,y,s=1):
 return circ(x,y+12*s,9*s,BROWN,1,GOLD)+circ(x+14*s,y+20*s,5*s,BROWN,1,GOLD)+ln(x-5*s,y+5*s,x-8*s,y-9*s,BROWN,1.2)+ln(x+5*s,y+5*s,x+8*s,y-9*s,BROWN,1.2)+ln(x+16*s,y+25*s,x+20*s,y+32*s,BROWN,1)+ln(x+13*s,y+25*s,x+11*s,y+33*s,BROWN,1)
def monkey(x,y,s=1):
 return person(x,y,s,robe=ORANGE)+f'{rgb(BROWN)} RG {1.5*s:.2f} w {x+8*s:.2f} {y+2*s:.2f} m {x+30*s:.2f} {y+12*s:.2f} {x+28*s:.2f} {y+29*s:.2f} {x+18*s:.2f} {y+28*s:.2f} c S\n'
def ocean(x,y,w,h):
 o=''
 for yy in [y+8,y+18,y+28,y+38]:o+=f'{rgb(BLUE)} RG 1.2 w {x:.2f} {yy:.2f} m {x+w*.25:.2f} {yy+5:.2f} {x+w*.5:.2f} {yy-5:.2f} {x+w*.75:.2f} {yy:.2f} c {x+w*.87:.2f} {yy+4:.2f} {x+w:.2f} {yy:.2f} {x+w:.2f} {yy:.2f} c S\n'
 return o
def bridge(x,y,w):
 return ''.join(rect(x+i*w/7,y,w/7-2,8,BROWN,.5,(.70,.56,.36)) for i in range(7))
def generic(kind):
 def f(cx,by,w,h):
  if kind=='palace': return palace(cx,by+8,.8)+person(cx-45,by+5,.55,robe=BLUE,crown=True)+person(cx+42,by+5,.55,robe=RED,crown=True)
  if kind=='forest': return tree(cx-50,by,.7)+tree(cx+50,by,.7)+hut(cx,by+2,.6)+person(cx-15,by+4,.55,robe=BLUE,crown=True,bow=True)+person(cx+20,by+4,.5,robe=ORANGE,crown=True,bow=True)
  if kind=='deer': return tree(cx-50,by,.65)+deer(cx+18,by+5,1.2)+person(cx-35,by+5,.55,robe=BLUE,crown=True,bow=True)
  if kind=='abduct': return person(cx-28,by+4,.55,robe=RED,crown=True)+person(cx+26,by+15,.68,robe=(.30,.18,.20),crown=True)+ln(cx-5,by+20,cx+12,by+34,RED,2)
  if kind=='monkey': return monkey(cx-10,by+4,.7)+person(cx-45,by+5,.55,robe=BLUE,crown=True,bow=True)+person(cx+45,by+5,.5,robe=ORANGE,crown=True,bow=True)
  if kind=='ocean': return ocean(cx-w/2,by,w,50)+monkey(cx,by+37,.55)
  if kind=='bridge': return ocean(cx-w/2,by,w,40)+bridge(cx-w/2+8,by+18,w-16)+person(cx-45,by+40,.45,robe=BLUE,crown=True,bow=True)+monkey(cx+45,by+40,.45)
  if kind=='battle': return person(cx-35,by+5,.6,robe=BLUE,crown=True,bow=True)+person(cx+35,by+5,.68,robe=(.25,.15,.18),crown=True,bow=True)+ln(cx-15,by+25,cx+18,by+30,RED,2)
  return tree(cx,by,.7)
 return f
def b1(cx,by,w,h): return person(cx-28,by+15,.7,robe=ORANGE,beard=True)+person(cx+25,by+10,.75,robe=(.95,.90,.75),beard=True)+tree(cx+55,by+5,.55)
def b2(cx,by,w,h): return fire(cx,by+15,1.1)+person(cx-40,by+8,.65,robe=RED,crown=True)+person(cx+40,by+10,.6,robe=ORANGE,beard=True)
def b3(cx,by,w,h): return palace(cx,by+5,.8)+person(cx-35,by+8,.55,robe=RED,crown=True)+person(cx-10,by+8,.5,robe=BLUE,crown=True)+person(cx+15,by+8,.5,robe=GREEN,crown=True)+person(cx+40,by+8,.5,robe=ORANGE,crown=True)
def b4(cx,by,w,h): return person(cx-40,by+8,.65,robe=ORANGE,beard=True)+person(cx,by+5,.6,robe=BLUE,crown=True,bow=True)+person(cx+40,by+5,.6,robe=ORANGE,crown=True,bow=True)
def b5(cx,by,w,h): return tree(cx-55,by,.55)+person(cx-25,by+5,.6,robe=BLUE,crown=True,bow=True)+circ(cx+40,by+28,11,BROWN,1,(.35,.18,.18))+fire(cx+35,by+2,.5)
def b6(cx,by,w,h): return palace(cx+45,by+2,.55)+person(cx-25,by+5,.62,robe=BLUE,crown=True,bow=True)+person(cx+20,by+5,.55,robe=RED,crown=True)+ln(cx-5,by+25,cx+5,by+45,GOLD,3)
SCENES={
'Bala-Kanda':[('Valmiki & Narada',b1),('Putra Kameshti',b2),('Birth of Four Princes',b3),('Viswamitra Arrives',b4),('Tataka & Divine Astras',b5),('Sita Swayamvara',b6)],
'Ayodhya-Kanda':[('Coronation Planned',generic('palace')),('Kaikeyi - Two Boons',generic('palace')),('Forest Exile',generic('forest')),('Bharata & Sandals',generic('palace')),('Chitrakuta',generic('forest')),('Ayodhya in Grief',generic('palace'))],
'Aranya-Kanda':[('Forest Hermitages',generic('forest')),('Surpanakha Episode',generic('forest')),('Golden Deer',generic('deer')),('Sita Abducted',generic('abduct')),('Jatayu Battle',generic('battle')),('Search & Shabari',generic('forest'))],
'Kishkindha-Kanda':[('Hanuma Meets Rama',generic('monkey')),('Sugriva Alliance',generic('monkey')),('Vali Duel',generic('battle')),('Sugriva Crowned',generic('palace')),('Vanara Search',generic('monkey')),('Sampati Reveals Lanka',generic('ocean'))],
'Sundara-Kanda':[('Leap Across Ocean',generic('ocean')),('Surasa & Simhika',generic('ocean')),('Ashoka Vana',generic('forest')),('Ring for Sita',generic('monkey')),('Lanka in Flames',generic('battle')),('Return with News',generic('monkey'))],
'Yuddha-Kanda':[('Rama Setu',generic('bridge')),('Army Crosses',generic('bridge')),('Battle of Lanka',generic('battle')),('Indrajit & Kumbhakarna',generic('battle')),('Ravana Falls',generic('battle')),('Return to Ayodhya',generic('palace'))]}
def panel(x,y,w,h,label,scene):
 return rect(x,y,w,h,GOLD,1.3,(1,.965,.86))+rect(x+3,y+3,w-6,h-6,RED,.45)+txt(x+9,y+h-18,label,8.6,True,RED)+ln(x+8,y+h-24,x+w-8,y+h-24,GOLD,.7)+scene(x+w/2,y+25,w-18,h-55)
def cover(k,title):
 s=f'{rgb(CREAM)} rg 0 0 {W} {H} re f\n'+rect(10,10,W-20,H-20,RED,2.4)+rect(16,16,W-32,H-32,GOLD,1)
 s+=txt(102,602,'RAMAYANAM',29,True,RED)+txt(max(120,216-len(title)*4.1),576,title,16.5,True,GOLD)+txt(144,558,'Mr. K.V.V Subramanyam',10.5,False,BROWN)
 for (lab,fn),(y,x) in zip(SCENES[k],[(yy,xx) for yy in [389,213,37] for xx in [22,220]]): s+=panel(x,y,190,158,lab,fn)
 return s
def paras(t):
 out=[]
 for b in re.split(r'\n\s*\n',t.replace('\r','')):
  ls=[x.strip() for x in b.split('\n') if x.strip()]
  if ls:out.append(' '.join(ls))
 return out
def stream(data,extra=''):
 if isinstance(data,str): data=data.encode('ascii')
 return f'<< /Length {len(data)} {extra}>>\nstream\n'.encode()+data+b'\nendstream'
def make_pdf(k,title):
 ps=[cover(k,title)]; y=590;n=2;c=border(n,'RAMAYANAM - '+title)
 for p in paras(load_text(k)):
  ls=textwrap.wrap(p,72,break_long_words=False,break_on_hyphens=False) or ['']; need=len(ls)*13+8
  if y-need<46:ps.append(c);n+=1;c=border(n,'RAMAYANAM - '+title);y=590
  ind=not bool(re.match(r'^(?:\d+\.|\*|[A-Za-z]\.)\s',p))
  for i,q in enumerate(ls):c+=txt(52 if i==0 and ind else 40,y,q);y-=13
  y-=7
 ps.append(c);o=[]
 def add(x):
  if isinstance(x,str):x=x.encode('latin1')
  o.append(x);return len(o)
 cat=add(b'');pag=add(b'');f1=add('<< /Type /Font /Subtype /Type1 /BaseFont /Times-Roman /Encoding /WinAnsiEncoding >>');f2=add('<< /Type /Font /Subtype /Type1 /BaseFont /Times-Bold /Encoding /WinAnsiEncoding >>');kids=[]
 for q in ps:
  st=q.encode('ascii');cid=add(stream(st));kids.append(add(f'<< /Type /Page /Parent {pag} 0 R /MediaBox [0 0 432 648] /Resources << /Font << /F1 {f1} 0 R /F2 {f2} 0 R >> >> /Contents {cid} 0 R >>'))
 o[cat-1]=f'<< /Type /Catalog /Pages {pag} 0 R >>'.encode();o[pag-1]=f'<< /Type /Pages /Kids [{" ".join(f"{x} 0 R" for x in kids)}] /Count {len(kids)} >>'.encode();out=bytearray(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n');offs=[0]
 for i,x in enumerate(o,1):offs.append(len(out));out+=f'{i} 0 obj\n'.encode()+x+b'\nendobj\n'
 xr=len(out);out+=f'xref\n0 {len(o)+1}\n'.encode()+b'0000000000 65535 f \n'+b''.join(f'{x:010d} 00000 n \n'.encode() for x in offs[1:])+f'trailer\n<< /Size {len(o)+1} /Root {cat} 0 R >>\nstartxref\n{xr}\n%%EOF\n'.encode();return bytes(out)
class Hdl(BaseHTTPRequestHandler):
 def do_GET(self):
  p=unquote(self.path.split('?',1)[0])
  if p.startswith('/pdfs/'):
   f=p.rsplit('/',1)[-1];d=DOCS.get(f)
   if not d:self.send_error(404);return
   try:b=make_pdf(*d)
   except Exception as e:self.send_error(500,str(e));return
   self.send_response(200);self.send_header('Content-Type','application/pdf');self.send_header('Content-Disposition',f'inline; filename="{f}"');self.send_header('Content-Length',str(len(b)));self.send_header('Cache-Control','no-cache, no-store, must-revalidate');self.end_headers();self.wfile.write(b);return
  body=b'Mana Puraanams PDF service is running.';self.send_response(200);self.send_header('Content-Type','text/plain');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
 def log_message(self,fmt,*a):print(fmt%a)
if __name__=='__main__':ThreadingHTTPServer(('0.0.0.0',int(os.environ.get('PORT','10000'))),Hdl).serve_forever()
