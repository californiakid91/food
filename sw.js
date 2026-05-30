// Service worker de Food — caché del app-shell para uso offline.
// Bump CACHE al cambiar la estrategia o los assets precacheados.
const CACHE = 'food-shell-v1';
const ASSETS = ['./', './index.html', './manifest.json', './icon.svg', './icon-180.png'];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  // Solo gestionamos recursos del propio origen. Firebase, Firestore y el
  // proxy de precios (otros orígenes) van siempre directos a la red.
  if (url.origin !== self.location.origin) return;

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
