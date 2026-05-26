#!/usr/bin/env python3
"""
Servidor seguro de sincronización — Balanceo de Cartera.

La contraseña se genera automáticamente en el primer arranque
y se guarda en sync.key (permisos 600, solo tú puedes leerla).

Uso:
    python3 sync.py                    # arrancar
    python3 sync.py --port 9090        # puerto alternativo
    python3 sync.py --reset-password   # generar nueva contraseña
"""
import http.server, json, os, socket, base64, secrets, argparse, hmac
from pathlib import Path

PORT     = 8080
BASE     = Path(__file__).parent
DATA     = BASE / 'portfolio-sync.json'
KEY_FILE = BASE / 'sync.key'


# ── Contraseña ──────────────────────────────────────────────────────────
def load_or_create_password():
    if KEY_FILE.exists():
        pwd = KEY_FILE.read_text().strip()
        if pwd:
            return pwd
    pwd = secrets.token_urlsafe(16)
    KEY_FILE.write_text(pwd + '\n')
    try:
        KEY_FILE.chmod(0o600)   # solo el dueño puede leer/escribir
    except Exception:
        pass
    return pwd


# ── Verificación de token ────────────────────────────────────────────────
def check_auth(headers, password):
    """Acepta X-Auth-Token o Authorization: Bearer <token>."""
    token = (
        headers.get('X-Auth-Token', '').strip()
        or _bearer(headers.get('Authorization', ''))
    )
    if not token:
        return False
    # Comparación segura (evita timing attacks)
    return hmac.compare_digest(token, password)


def _bearer(header):
    parts = header.strip().split(' ', 1)
    return parts[1] if len(parts) == 2 and parts[0] == 'Bearer' else ''


# ── Handler HTTP ─────────────────────────────────────────────────────────
class Handler(http.server.SimpleHTTPRequestHandler):
    password = ''

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(BASE), **kw)

    # CORS preflight — sin datos, sin auth requerida
    def do_OPTIONS(self):
        self._send(200)

    def do_GET(self):
        if not check_auth(self.headers, self.password):
            self._unauthorized()
            return
        if self.path == '/api/sync':
            body = DATA.read_bytes() if DATA.exists() else b'{}'
            self._send(200, 'application/json', body)
        elif self.path in ('/', '/index.html'):
            super().do_GET()
        else:
            super().do_GET()

    def do_POST(self):
        if not check_auth(self.headers, self.password):
            self._unauthorized()
            return
        if self.path == '/api/sync':
            n    = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(n)
            try:
                json.loads(body)
            except json.JSONDecodeError:
                self._send(400, 'application/json', b'{"error":"json invalido"}')
                return
            DATA.write_bytes(body)
            self._send(200, 'application/json', b'{"ok":true}')
        else:
            self.send_error(404)

    # ── Helpers ────────────────────────────────────────────────────────
    def _unauthorized(self):
        body = b'{"error":"no autorizado"}'
        self.send_response(401)
        self.send_header('Access-Control-Allow-Origin',  '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Auth-Token')
        self.send_header('Content-Type',   'application/json')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def _send(self, code, ct='application/json', body=b''):
        self.send_response(code)
        self.send_header('Access-Control-Allow-Origin',  '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Auth-Token')
        self.send_header('Content-Type',   ct)
        self.send_header('Content-Length', len(body))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def log_message(self, fmt, *args):
        # Solo mostrar accesos denegados y errores
        if args and str(args[1]) not in ('200', '304', '206'):
            status = args[1] if len(args) > 1 else '?'
            ip     = self.address_string()
            path   = self.path if hasattr(self, 'path') else ''
            print(f'  [{status}] {ip}  {path}')


# ── IP local ────────────────────────────────────────────────────────────
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return 'localhost'


# ── Arranque ────────────────────────────────────────────────────────────
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Servidor seguro de Balanceo de Cartera')
    parser.add_argument('--port',           type=int, default=PORT, help='Puerto (defecto: 8080)')
    parser.add_argument('--reset-password', action='store_true',    help='Genera una nueva contraseña')
    args = parser.parse_args()

    if args.reset_password:
        KEY_FILE.unlink(missing_ok=True)
        print('  Contraseña eliminada. Generando nueva...')

    password = load_or_create_password()
    Handler.password = password

    ip   = get_local_ip()
    port = args.port

    print()
    print('  ╔══════════════════════════════════════════════╗')
    print('  ║   Balanceo de Cartera — Servidor Seguro      ║')
    print('  ╚══════════════════════════════════════════════╝')
    print()
    print(f'  PC:     http://localhost:{port}')
    print(f'  iPhone: http://{ip}:{port}')
    print()
    print(f'  Contraseña: {password}')
    print()
    print('  Introduce la contraseña en la app (icono 🔐 en la cabecera).')
    print('  La app la recuerda — solo necesitas introducirla una vez.')
    print()
    print('  Para generar nueva contraseña: python3 sync.py --reset-password')
    print('  Pulsa Ctrl+C para detener.')
    print()

    try:
        server = http.server.HTTPServer(('0.0.0.0', port), Handler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n  Servidor detenido.')
