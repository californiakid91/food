// D-48: cinco llamantes ignoran el booleano de saveMeta. ¿Pintan verde?
const R = {};
globalThis.getComputedStyle = () => ({ getPropertyValue: () => '#000', width: '300px', height: '150px' });
globalThis.requestAnimationFrame = fn => { fn(0); return 1; };
globalThis.cancelAnimationFrame = () => {};
globalThis.devicePixelRatio = 1;
function sembrar() {
  localStorage.clear();
  portfolios = [{id:1,name:'A'},{id:2,name:'B'}]; currentPortId = 1; nextId = 5; rows = [];
  localStorage.setItem('balance-meta-v2', JSON.stringify({portfolios,currentPortId,nextId,savedAt:1}));
  localStorage.setItem('balance-rows-1', JSON.stringify({rows:[{id:1,name:'AAA'}],nextId:2}));
  localStorage.setItem('balance-rows-2', JSON.stringify({rows:[{id:2,name:'BBB'}],nextId:3}));
  localStorage.setItem('balance-ops','[]');
}
// META_KEY falla; el resto del disco no. Ancla del sabotaje: la clave exacta.
function conMetaRota(fn) {
  const setReal = localStorage.setItem.bind(localStorage);
  localStorage.setItem = (k,v) => {
    // VACUIDAD: sin cuota rota
    return setReal(k,v);
  };
  try { return fn(); } finally { localStorage.setItem = setReal; }
}
function medir(nombre, fn) {
  sembrar();
  const v = abrirVentanaDePintura();
  // El DOM de mentira no tiene lienzo y `render()` lo pide. Se le añade un
  // contexto inerte SIN tocar lo que la ventana observa (texto, color, título).
  const ctxInerte = new Proxy({}, { get: (t,k) => (k==='canvas'?{width:0,height:0}:
      (k==='measureText'? (()=>({width:0})) : (k==='createLinearGradient'? (()=>({addColorStop(){}})) : (()=>{})))), set: ()=>true });
  const dameVent = document.getElementById;
  document.getElementById = id => {
    const e = dameVent(id);
    if (e && typeof e.getContext !== 'function') {
      e.getContext = () => ctxInerte;
      if (!('width' in e)) { e.width = 300; e.height = 150; }
      if (!e.getBoundingClientRect) e.getBoundingClientRect = () => ({width:300,height:150,left:0,top:0});
      if (!e.appendChild) e.appendChild = () => {};
      if (!e.addEventListener) e.addEventListener = () => {};
    }
    return e;
  };
  let subidas = 0; const spOrig = schedulePush;
  schedulePush = () => { subidas++; };
  try {
    conMetaRota(fn);
    const ind = v.el('save-indicator');
    R[nombre] = {
      pintado: ind ? { texto: ind.textContent, color: ind.style.color } : null,
      subidas,
      metaEnDisco: JSON.parse(localStorage.getItem('balance-meta-v2')).portfolios.map(p=>p.name),
      carterasEnMemoria: portfolios.map(p=>p.name),
      rowsB: localStorage.getItem('balance-rows-2') === null ? 'BORRADO DEL DISCO' : 'presente',
    };
  } catch (e) { R[nombre] = { lanzo: String(e && e.message) }; }
  finally { v.cerrar(); schedulePush = spOrig; }
}
medir('switchPortfolio', () => switchPortfolio(2));
medir('addPortfolio',    () => { globalThis.prompt = () => 'Nueva'; addPortfolio(); });
medir('renamePortfolio', () => { globalThis.prompt = () => 'Renombrada'; renamePortfolio(1); });
medir('deletePortfolio', () => { globalThis.confirm = () => true; deletePortfolio(2); });
medir('createDefaultPortfolios', () => createDefaultPortfolios());
console.log(JSON.stringify(R, null, 2));
process.exit(0);
