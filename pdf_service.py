import base64,gzip,os,re,textwrap,math
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import unquote
ROOT=os.path.dirname(os.path.abspath(__file__))
DOCS={'Bala-Kanda.pdf':('Bala-Kanda','BALA KANDA'),'Ayodhya-Kanda.pdf':('Ayodhya-Kanda','AYODHYA KANDA'),'Aranya-Kanda.pdf':('Aranya-Kanda','ARANYA KANDA'),'Kishkindha-Kanda.pdf':('Kishkindha-Kanda','KISHKINDHA KANDA'),'Sundara-Kanda.pdf':('Sundara-Kanda','SUNDARA KANDA'),'Yuddha-Kanda.pdf':('Yuddha-Kanda','YUDDHA KANDA')}
W,H=432.,648.; CREAM=(.984,.957,.894); RED=(.58,.09,.06); GOLD=(.78,.55,.13); BROWN=(.20,.12,.06); BLUE=(.10,.28,.55); GREEN=(.12,.42,.20); ORANGE=(.88,.38,.06)
def load_text(k):
 p=os.path.join(ROOT,'textdata',k+'.txt'); return gzip.decompress(base64.b64decode(open(p,encoding='ascii').read().strip())).decode('utf-8')
def hx(s): return s.encode('cp1252','replace').hex().upper()
def rgb(c): return f'{c[0]:.3f} {c[1]:.3f} {c[2]:.3f}'
def txt(x,y,s,z=10.3,b=False,c=BROWN): return f'{rgb(c)} rg BT /{"F2" if b else "F1"} {z:.2f} Tf 1 0 0 1 {x:.2f} {y:.2f} Tm <{hx(s)}> Tj ET\n'
def ln(a,b,c,d,col=BROWN,w=1): return f'{rgb(col)} RG {w:.2f} w {a:.2f} {b:.2f} m {c:.2f} {d:.2f} l S\n'
def rect(x,y,w,h,col=BROWN,lw=1,fill=None): return (f'{rgb(fill)} rg {x} {y} {w} {h} re f\n' if fill else '')+f'{rgb(col)} RG {lw} w {x} {y} {w} {h} re S\n'
def circ(x,y,r,col=BROWN,lw=1,fill=None):
 k=.55228475*r; p=f'{x+r} {y} m {x+r} {y+k} {x+k} {y+r} {x} {y+r} c {x-k} {y+r} {x-r} {y+k} {x-r} {y} c {x-r} {y-k} {x-k} {y-r} {x} {y-r} c {x+k} {y-r} {x+r} {y-k} {x+r} {y} c '
 return (f'{rgb(fill)} rg ' if fill else '')+f'{rgb(col)} RG {lw} w {p}{"B" if fill else "S"}\n'
def border(n=None,head=None):
 s=f'{rgb(CREAM)} rg 0 0 {W} {H} re f\n'+rect(12,12,W-24,H-24,RED,2)+rect(18,18,W-36,H-36,GOLD,.8)
 for x,y in [(24,24),(W-24,24),(24,H-24),(W-24,H-24)]: s+=circ(x,y,5,GOLD,.8)+ln(x-7,y,x+7,y,GOLD,.7)+ln(x,y-7,x,y+7,GOLD,.7)
 if head:s+=txt(118,H-32,head,10.2,True,RED)
 if n:s+=txt(W/2-3,16,str(n),8.2,False,BROWN)
 return s
def art(k):
 s=''
 if k=='Bala-Kanda':
  s+=circ(216,382,42,GOLD,1.5,(1,.83,.25)); s+=f'{rgb(RED)} RG 4 w 140 230 m 175 270 175 340 140 375 c S\n'+ln(142,303,285,303,BLUE,2.3)+ln(270,311,285,303,GOLD,1.5)+ln(270,295,285,303,GOLD,1.5)
 elif k=='Ayodhya-Kanda':
  s+=rect(100,210,232,120,GOLD,2,(.96,.82,.48));
  for x in [120,160,200,240,280]:s+=rect(x,210,18,100,RED,1.2,(.98,.92,.72))
  s+=ln(90,330,342,330,RED,3)+f'{rgb(GOLD)} rg {rgb(RED)} RG 1.5 w 166 330 m 216 395 l 266 330 l h B\n'
 elif k=='Aranya-Kanda':
  for x in [125,205,295]:s+=rect(x-6,205,12,115,BROWN,1,(.45,.24,.10))+circ(x,345,40,GREEN,1.2,(.33,.64,.28))+circ(x-24,325,27,GREEN,1,(.42,.70,.32))+circ(x+24,325,27,GREEN,1,(.42,.70,.32))
  s+=circ(218,250,25,GOLD,1.2,(.84,.58,.20))+circ(250,270,13,GOLD,1.2,(.84,.58,.20))+ln(205,230,200,195,BROWN,2)+ln(225,230,220,195,BROWN,2)
 elif k=='Kishkindha-Kanda':
  s+=f'{rgb(GREEN)} rg {rgb(BROWN)} RG 1.5 w 70 210 m 155 365 l 220 245 l 285 385 l 365 210 l h B\n'+circ(220,300,28,ORANGE,1.5,(.82,.52,.18))+circ(220,340,19,ORANGE,1.5,(.82,.52,.18))+f'{rgb(ORANGE)} RG 4 w 245 300 m 300 310 300 245 260 250 c S\n'
 elif k=='Sundara-Kanda':
  for y in [210,230,250,270]:s+=f'{rgb(BLUE)} RG 2 w 60 {y} m 100 {y+12} 140 {y-12} 180 {y} c 220 {y+12} 260 {y-12} 300 {y} c 340 {y+12} 370 {y} 380 {y} c S\n'
  s+=circ(190,355,15,ORANGE,1.2,(.88,.55,.18))+ln(200,347,250,315,ORANGE,6)+ln(238,322,285,350,RED,4)+ln(235,322,275,285,ORANGE,5)+ln(205,348,155,320,ORANGE,5)
 else:
  for r in range(4):
   for c in range(7):s+=rect(75+c*42+(r%2)*18,205+r*28,36,20,BROWN,.8,(.72,.60,.42))
  s+=ln(125,350,305,245,RED,4)+ln(125,245,305,350,BLUE,4)
 return s
def paras(t):
 out=[]
 for b in re.split(r'\n\s*\n',t.replace('\r','')):
  ls=[x.strip() for x in b.split('\n') if x.strip()]
  if ls:out.append(' '.join(ls))
 return out
def make_pdf(k,title):
 ps=[]; c=border(1)+txt(96,565,'RAMAYANAM',30,True,RED)+txt(max(65,216-len(title)*4.6),525,title,19,True,GOLD)+txt(135,492,'Mr. K.V.V Subramanyam',12,False,BROWN)+art(k)+txt(116,110,'Traditional illustrated reading edition',10.5,False,BROWN);ps.append(c)
 y=590;n=2;c=border(n,'RAMAYANAM - '+title)
 for p in paras(load_text(k)):
  ls=textwrap.wrap(p,72,break_long_words=False,break_on_hyphens=False) or ['']; need=len(ls)*13+8
  if y-need<46:ps.append(c);n+=1;c=border(n,'RAMAYANAM - '+title);y=590
  ind=not bool(re.match(r'^(?:\d+\.|\*|[A-Za-z]\.)\s',p))
  for i,q in enumerate(ls):c+=txt(52 if i==0 and ind else 40,y,q);y-=13
  y-=7
 ps.append(c);o=[]
 def add(x):o.append(x if isinstance(x,bytes) else x.encode('latin1'));return len(o)
 cat=add(b'');pag=add(b'');f1=add('<< /Type /Font /Subtype /Type1 /BaseFont /Times-Roman /Encoding /WinAnsiEncoding >>');f2=add('<< /Type /Font /Subtype /Type1 /BaseFont /Times-Bold /Encoding /WinAnsiEncoding >>');kids=[]
 for q in ps:
  st=q.encode('ascii');cid=add(b'<< /Length '+str(len(st)).encode()+b' >>\nstream\n'+st+b'endstream');kids.append(add(f'<< /Type /Page /Parent {pag} 0 R /MediaBox [0 0 432 648] /Resources << /Font << /F1 {f1} 0 R /F2 {f2} 0 R >> >> /Contents {cid} 0 R >>'))
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
   self.send_response(200);self.send_header('Content-Type','application/pdf');self.send_header('Content-Disposition',f'inline; filename="{f}"');self.send_header('Content-Length',str(len(b)));self.send_header('Cache-Control','public, max-age=900');self.end_headers();self.wfile.write(b);return
  body=b'Mana Puraanams PDF service is running.';self.send_response(200);self.send_header('Content-Type','text/plain');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
 def log_message(self,fmt,*a):print(fmt%a)
if __name__=='__main__':ThreadingHTTPServer(('0.0.0.0',int(os.environ.get('PORT','10000'))),Hdl).serve_forever()
