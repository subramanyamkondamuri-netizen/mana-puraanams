import base64, gzip, os, re, textwrap, json, hashlib
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = {
    'Bala-Kanda.pdf': ('Bala-Kanda', 'BALA KANDA'),
    'Ayodhya-Kanda.pdf': ('Ayodhya-Kanda', 'AYODHYA KANDA'),
    'Aranya-Kanda.pdf': ('Aranya-Kanda', 'ARANYA KANDA'),
    'Kishkindha-Kanda.pdf': ('Kishkindha-Kanda', 'KISHKINDHA KANDA'),
    'Sundara-Kanda.pdf': ('Sundara-Kanda', 'SUNDARA KANDA'),
    'Yuddha-Kanda.pdf': ('Yuddha-Kanda', 'YUDDHA KANDA'),
}

W, H = 432.0, 648.0
CREAM = (.984, .957, .894)
RED = (.58, .09, .06)
GOLD = (.78, .55, .13)
BROWN = (.20, .12, .06)


def load_text(key):
    path = os.path.join(ROOT, 'textdata', key + '.txt')
    with open(path, encoding='ascii') as f:
        packed = base64.b64decode(f.read().strip())
    return gzip.decompress(packed).decode('utf-8')


def hx(s):
    return s.encode('cp1252', 'replace').hex().upper()


def rgb(c):
    return f'{c[0]:.3f} {c[1]:.3f} {c[2]:.3f}'


def txt(x, y, s, z=10.3, bold=False, color=BROWN):
    font = 'F2' if bold else 'F1'
    return f'{rgb(color)} rg BT /{font} {z:.2f} Tf 1 0 0 1 {x:.2f} {y:.2f} Tm <{hx(s)}> Tj ET\n'


def line(x1, y1, x2, y2, color=BROWN, width=1):
    return f'{rgb(color)} RG {width:.2f} w {x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S\n'


def rect(x, y, w, h, color=BROWN, width=1):
    return f'{rgb(color)} RG {width:.2f} w {x:.2f} {y:.2f} {w:.2f} {h:.2f} re S\n'


def circle(x, y, r, color=BROWN, width=1):
    k = .55228475 * r
    p = (
        f'{x+r:.2f} {y:.2f} m '
        f'{x+r:.2f} {y+k:.2f} {x+k:.2f} {y+r:.2f} {x:.2f} {y+r:.2f} c '
        f'{x-k:.2f} {y+r:.2f} {x-r:.2f} {y+k:.2f} {x-r:.2f} {y:.2f} c '
        f'{x-r:.2f} {y-k:.2f} {x-k:.2f} {y-r:.2f} {x:.2f} {y-r:.2f} c '
        f'{x+k:.2f} {y-r:.2f} {x+r:.2f} {y-k:.2f} {x+r:.2f} {y:.2f} c S\n'
    )
    return f'{rgb(color)} RG {width:.2f} w ' + p


def border(page_no=None, head=None):
    s = f'{rgb(CREAM)} rg 0 0 {W} {H} re f\n'
    s += rect(12, 12, W - 24, H - 24, RED, 2)
    s += rect(18, 18, W - 36, H - 36, GOLD, .8)
    for x, y in [(24, 24), (W-24, 24), (24, H-24), (W-24, H-24)]:
        s += circle(x, y, 5, GOLD, .8)
        s += line(x-7, y, x+7, y, GOLD, .7)
        s += line(x, y-7, x, y+7, GOLD, .7)
    if head:
        s += txt(118, H-32, head, 10.2, True, RED)
    if page_no:
        s += txt(W/2-3, 16, str(page_no), 8.2, False, BROWN)
    return s


def paragraphs(text):
    out = []
    for block in re.split(r'\n\s*\n', text.replace('\r', '')):
        lines = [x.strip() for x in block.split('\n') if x.strip()]
        if lines:
            out.append(' '.join(lines))
    return out


def make_pdf(key, title):
    pages = []
    page_no = 1
    y = 590
    page = border(page_no, 'RAMAYANAM - ' + title)

    for p in paragraphs(load_text(key)):
        lines = textwrap.wrap(p, 72, break_long_words=False, break_on_hyphens=False) or ['']
        needed = len(lines) * 13 + 8
        if y - needed < 46:
            pages.append(page)
            page_no += 1
            page = border(page_no, 'RAMAYANAM - ' + title)
            y = 590

        is_list = bool(re.match(r'^(?:\d+\.|\*|[A-Za-z]\.)\s', p))
        for i, line_text in enumerate(lines):
            x = 40 if is_list or i > 0 else 52
            page += txt(x, y, line_text, 10.3, False, BROWN)
            y -= 13
        y -= 7

    pages.append(page)

    objects = []

    def add(obj):
        objects.append(obj if isinstance(obj, bytes) else obj.encode('latin1'))
        return len(objects)

    catalog_id = add(b'')
    pages_id = add(b'')
    f1_id = add('<< /Type /Font /Subtype /Type1 /BaseFont /Times-Roman /Encoding /WinAnsiEncoding >>')
    f2_id = add('<< /Type /Font /Subtype /Type1 /BaseFont /Times-Bold /Encoding /WinAnsiEncoding >>')
    page_ids = []

    for content in pages:
        stream = content.encode('ascii')
        content_id = add(b'<< /Length ' + str(len(stream)).encode() + b' >>\nstream\n' + stream + b'endstream')
        page_ids.append(add(
            f'<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 432 648] '
            f'/Resources << /Font << /F1 {f1_id} 0 R /F2 {f2_id} 0 R >> >> '
            f'/Contents {content_id} 0 R >>'
        ))

    objects[catalog_id-1] = f'<< /Type /Catalog /Pages {pages_id} 0 R >>'.encode()
    kids = ' '.join(f'{pid} 0 R' for pid in page_ids)
    objects[pages_id-1] = f'<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>'.encode()

    out = bytearray(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n')
    offsets = [0]
    for i, obj in enumerate(objects, 1):
        offsets.append(len(out))
        out += f'{i} 0 obj\n'.encode() + obj + b'\nendobj\n'

    xref = len(out)
    out += f'xref\n0 {len(objects)+1}\n'.encode()
    out += b'0000000000 65535 f \n'
    out += b''.join(f'{off:010d} 00000 n \n'.encode() for off in offsets[1:])
    out += f'trailer\n<< /Size {len(objects)+1} /Root {catalog_id} 0 R >>\nstartxref\n{xref}\n%%EOF\n'.encode()
    return bytes(out)


def clean_value(value, limit=600):
    if value is None:
        return ''
    return str(value).replace('\r', ' ').replace('\n', ' ')[:limit]


class Handler(BaseHTTPRequestHandler):
    def cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(204)
        self.cors()
        self.end_headers()

    def do_POST(self):
        path = unquote(self.path.split('?', 1)[0])
        if path != '/api/hit':
            self.send_error(404)
            return

        try:
            length = min(int(self.headers.get('Content-Length', '0') or 0), 16384)
            raw = self.rfile.read(length) if length else b'{}'
            payload = json.loads(raw.decode('utf-8', 'replace'))
        except Exception:
            payload = {}

        forwarded = self.headers.get('X-Forwarded-For', '')
        ip = forwarded.split(',')[0].strip() if forwarded else self.client_address[0]
        salt = os.environ.get('ANALYTICS_SALT', 'mana-puraanams-analytics')
        visitor_id = hashlib.sha256((salt + '|' + ip).encode('utf-8')).hexdigest()[:20]

        event = {
            'event': 'page_view',
            'timestamp_utc': datetime.now(timezone.utc).isoformat(),
            'ip': clean_value(ip, 80),
            'visitor_id': visitor_id,
            'page': clean_value(payload.get('page'), 900),
            'title': clean_value(payload.get('title'), 300),
            'referrer': clean_value(payload.get('referrer'), 900),
            'language': clean_value(payload.get('language'), 80),
            'timezone': clean_value(payload.get('timezone'), 120),
            'screen': clean_value(payload.get('screen'), 80),
            'platform': clean_value(payload.get('platform'), 160),
            'user_agent': clean_value(self.headers.get('User-Agent', ''), 700),
            'accept_language': clean_value(self.headers.get('Accept-Language', ''), 220),
        }
        print('VISIT ' + json.dumps(event, ensure_ascii=False, separators=(',', ':')), flush=True)

        body = b'{"ok":true}'
        self.send_response(200)
        self.cors()
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = unquote(self.path.split('?', 1)[0])
        if path.startswith('/pdfs/'):
            filename = path.rsplit('/', 1)[-1]
            doc = DOCS.get(filename)
            if not doc:
                self.send_error(404)
                return
            try:
                data = make_pdf(*doc)
            except Exception as exc:
                self.send_error(500, str(exc))
                return
            self.send_response(200)
            self.send_header('Content-Type', 'application/pdf')
            self.send_header('Content-Disposition', f'inline; filename="{filename}"')
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store, max-age=0')
            self.end_headers()
            self.wfile.write(data)
            return

        body = b'Mana Puraanams PDF and analytics service is running.'
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(fmt % args, flush=True)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '10000'))
    ThreadingHTTPServer(('0.0.0.0', port), Handler).serve_forever()
