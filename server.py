import base64, gzip, os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = {
    'Bala-Kanda.pdf': 'Bala-Kanda',
}

def load_pdf(key):
    folder = os.path.join(ROOT, 'pdfdata', key)
    parts = []
    for name in sorted(os.listdir(folder)):
        if name.endswith('.txt'):
            with open(os.path.join(folder, name), 'r', encoding='ascii') as f:
                parts.append(f.read().strip())
    packed = base64.b64decode(''.join(parts))
    return gzip.decompress(packed)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = unquote(self.path.split('?',1)[0])
        if path.startswith('/pdfs/'):
            filename = path.rsplit('/',1)[-1]
            key = DOCS.get(filename)
            if not key:
                self.send_error(404)
                return
            try:
                data = load_pdf(key)
            except Exception as e:
                self.send_error(500, str(e))
                return
            self.send_response(200)
            self.send_header('Content-Type','application/pdf')
            self.send_header('Content-Disposition', f'inline; filename="{filename}"')
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control','public, max-age=3600')
            self.end_headers()
            self.wfile.write(data)
            return
        if path in ('/','/health'):
            body = b'Mana Puraanams PDF service is running.'
            self.send_response(200)
            self.send_header('Content-Type','text/plain; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_error(404)

if __name__ == '__main__':
    port = int(os.environ.get('PORT','10000'))
    ThreadingHTTPServer(('0.0.0.0', port), Handler).serve_forever()
