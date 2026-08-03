// Service worker de Food — caché del app-shell para uso offline.
// Bump CACHE al cambiar la estrategia o los assets precacheados.
const CACHE = 'food-shell-v2';
const ASSETS = ['./', './index.html', './manifest.json', './icon.svg', './icon-180.png'];

// Recursos de otros orígenes que cacheamos para que la app abra en modo avión:
// SDK de Firebase (si no, `firebase` queda indefinido sin red) y la fuente Inter.
const CROSS_ORIGIN = [
  'https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js',
  'https://www.gstatic.com/firebasejs/10.12.2/firebase-auth-compat.js',
  'https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore-compat.js',
  'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap',
];
const CROSS_HOSTS = ['www.gstatic.com', 'fonts.googleapis.com', 'fonts.gstatic.com'];

// Motor de OCR (Tesseract) y sus datos de idioma: son decenas de MB y se
// descargan la primera vez que se sube una captura. Van en su propia caché
// para no rehacer esa descarga en cada despliegue de la app.
const OCR_CACHE = 'food-ocr-v1';
const OCR_HOSTS = ['cdn.jsdelivr.net', 'unpkg.com', 'tessdata.projectnaptha.com'];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE).then(async (c) => {
      await c.addAll(ASSETS);
      // Best-effort: si alguno falla (offline en la instalación) no abortamos.
      await Promise.all(CROSS_ORIGIN.map((u) =>
        fetch(u, { mode: 'no-cors' }).then((r) => c.put(u, r)).catch(() => {})
      ));
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE && k !== OCR_CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);

  // Otros orígenes: cache-first SOLO para Firebase SDK y fuentes (offline-capable).
  // Firestore/Auth (APIs en tiempo real) y demás orígenes van directos a la red.
  if (url.origin !== self.location.origin) {
    if (OCR_HOSTS.includes(url.hostname)) {
      e.respondWith(
        caches.match(req, { cacheName: OCR_CACHE }).then((cached) => cached || fetch(req).then((resp) => {
          const copy = resp.clone();
          caches.open(OCR_CACHE).then((c) => c.put(req, copy));
          return resp;
        }).catch(() => cached))
      );
      return;
    }
    if (CROSS_HOSTS.includes(url.hostname)) {
      e.respondWith(
        caches.match(req).then((cached) => cached || fetch(req).then((resp) => {
          const copy = resp.clone();
          caches.open(CACHE).then((c) => c.put(req, copy));
          return resp;
        }).catch(() => cached))
      );
    }
    return;
  }

  // HTML / navegación: network-first (para recibir actualizaciones), con
  // caída a la caché cuando no hay red.
  if (req.mode === 'navigate' || url.pathname.endsWith('/') || url.pathname.endsWith('index.html')) {
    e.respondWith(
      fetch(req)
        .then((resp) => {
          const copy = resp.clone();
          caches.open(CACHE).then((c) => c.put(req, copy));
          return resp;
        })
        .catch(() => caches.match(req).then((r) => r || caches.match('./index.html')))
    );
    return;
  }

  // Resto de estáticos propios (iconos, manifest): stale-while-revalidate.
  e.respondWith(
    caches.match(req).then((cached) => {
      const network = fetch(req)
        .then((resp) => {
          const copy = resp.clone();
          caches.open(CACHE).then((c) => c.put(req, copy));
          return resp;
        })
        .catch(() => cached);
      return cached || network;
    })
  );
});
