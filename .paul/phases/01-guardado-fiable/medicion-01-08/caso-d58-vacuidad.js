// D-58: un libro de la nube que NO CABE adelanta el reloj y el siguiente
// guardado lo exporta encima. Se mide EJECUTANDO, no leyendo.
const paso = m => require('fs').writeSync(2, 'PASO: ' + m + '\n');
(async () => {
  const R = {};
  // --- Siembra: disco con libro POBRE (2 ops) y reloj viejo ---
  const pobres = [ {id:'o1',date:'2024-01-01',type:'buy',ticker:'A',titulos:1,price:1,currency:'EUR'},
                   {id:'o2',date:'2024-01-02',type:'buy',ticker:'A',titulos:1,price:1,currency:'EUR'} ];
  const ricas = [];
  for (let i = 0; i < 42; i++) ricas.push({id:'n'+i,date:'2024-02-0'+(i%9+1),type:'buy',ticker:'RICO',titulos:1,price:1,currency:'EUR'});
  localStorage.setItem('balance-ops', JSON.stringify(pobres));
  localStorage.setItem('balance-meta-v2', JSON.stringify({portfolios:[{id:7,name:'C'}],currentPortId:7,nextId:8,savedAt:1000}));
  localStorage.setItem('balance-rows-7', JSON.stringify({rows:[{id:1,name:'A'}],nextId:2}));
  portfolios=[{id:7,name:'C'}]; currentPortId=7; nextId=8; opsIlegible=false;
  paso('siembra');
  ops = loadOpsAll();
  R.opsAntes = ops.length;

  // --- CUOTA LLENA: la escritura del libro falla, el resto del disco no ---
  paso('cuota');
  const setReal = localStorage.setItem.bind(localStorage);
  let cuota = false;   // CONTROL DE VACUIDAD: sin cuota llena
  localStorage.setItem = (k, v) => {
    if (cuota && String(k) === 'balance-ops') { const e = new Error('QuotaExceededError'); e.name='QuotaExceededError'; throw e; }
    return setReal(k, v);
  };

  // --- Llega de la nube un libro RICO con reloj NUEVO ---
  const doc = { portfolios:[{id:7,name:'C'}], currentPortId:7, nextId:8,
                portfolioData:{}, historyData:{}, opsAll: ricas, savedAt: 9000 };
  paso('aplicar');
  R.aplicado = applySyncPayload(doc);
  R.discoOps = JSON.parse(localStorage.getItem('balance-ops')).map(o=>o.id);
  R.metaSavedAt = JSON.parse(localStorage.getItem('balance-meta-v2')).savedAt;
  R.opsEnMemoria = ops.length;

  // --- Ahora el dispositivo guarda: ¿sube su libro pobre encima del rico? ---
  cuota = false;                      // la cuota se libera; el libro ya es pobre
  paso('ventana');
  const v = abrirVentanaDePintura();
  let nubeAhora = ricas.slice();
  const ref = { set: async (p) => { nubeAhora = p.opsAll; }, get: async () => ({ exists:true, data:()=>doc }) };
  try {
  paso('guardarTodo');
    R.guardado = guardarTodo();
    R.pintadoGuardado = v.el('save-indicator') ? { texto: v.el('save-indicator').textContent, color: v.el('save-indicator').style.color } : null;
  paso('subir');
    const res = await subirALaNube('medicion', { ref, paquete: buildSyncPayload, mirar: observarNube,
                                                 cerrojo: () => opsIlegible, activos: hasRealLocalData });
    R.subida = res;
    R.nubeAntes = ricas.length;
    R.nubeDespues = Array.isArray(nubeAhora) ? nubeAhora.length : null;
    R.puntoSync = v.el('sync-dot') ? v.el('sync-dot').title : null;
    R.textoSync = v.el('sync-status') ? v.el('sync-status').textContent : null;
  } finally { v.cerrar(); }
  console.log(JSON.stringify(R, null, 2));
  process.exit(0);
})().catch(e => { require('fs').writeSync(2, 'INSTRUMENTO ROTO: ' + (e && e.stack || e) + '\n'); process.exit(2); });
