// DOM de mentira, lo minimo para que el script de index.html se cargue en node.
// No simula la app: solo evita que el codigo de arranque reviente al definirse
// las funciones. Las autopruebas solo tocan funciones puras.
const noop = () => {};
const el = new Proxy({}, {
  get: (t, k) => {
    if (k === 'style') return {};
    if (k === 'classList') return { add: noop, remove: noop, toggle: noop, contains: () => false };
    if (k === 'value' || k === 'textContent' || k === 'innerHTML') return '';
    if (k === 'children') return [];
    if (Symbol.iterator === k) return undefined;
    return typeof k === 'string' ? noop : undefined;
  },
  set: () => true,
});
globalThis.document = {
  getElementById: () => null,
  querySelector: () => null,
  querySelectorAll: () => [],
  createElement: () => el,
  addEventListener: noop,
  body: el,
  documentElement: el,
};
globalThis.location = { search: '', href: '', hash: '', reload: noop };
globalThis.navigator = { onLine: true, serviceWorker: { register: () => Promise.resolve() }, userAgent: 'node' };
const store = new Map();
globalThis.localStorage = {
  getItem: k => (store.has(String(k)) ? store.get(String(k)) : null),
  setItem: (k, v) => { store.set(String(k), String(v)); },
  removeItem: k => { store.delete(String(k)); },
  clear: () => store.clear(),
  key: i => [...store.keys()][i] ?? null,
  get length() { return store.size; },
};
globalThis.window = globalThis;
globalThis.addEventListener = noop;
globalThis.fetch = () => Promise.reject(new Error('sin red en las autopruebas'));
globalThis.alert = noop;
globalThis.confirm = () => false;
globalThis.matchMedia = () => ({ matches: false, addEventListener: noop, addListener: noop });
