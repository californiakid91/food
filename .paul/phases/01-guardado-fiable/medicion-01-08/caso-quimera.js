// ¿Qué pasa si la cuota está llena DE VERDAD (todas las claves), no sólo el libro?
const R = {};
const pobres = [{id:'o1',date:'2024-01-01',type:'buy',ticker:'A',titulos:1,price:1,currency:'EUR'}];
const ricas = []; for (let i=0;i<42;i++) ricas.push({id:'n'+i,date:'2024-02-01',type:'buy',ticker:'R',titulos:1,price:1,currency:'EUR'});
localStorage.setItem('balance-ops', JSON.stringify(pobres));
localStorage.setItem('balance-meta-v2', JSON.stringify({portfolios:[{id:7,name:'Vieja'}],currentPortId:7,nextId:8,savedAt:1000}));
localStorage.setItem('balance-rows-7', JSON.stringify({rows:[{id:1,name:'A'}],nextId:2}));
portfolios=[{id:7,name:'Vieja'}]; currentPortId=7; nextId=8; opsIlegible=false; ops=loadOpsAll();
const doc = { portfolios:[{id:9,name:'DeLaNube'}], currentPortId:9, nextId:20,
              portfolioData:{ 9:{rows:[{id:5,name:'NUEVO'}],nextId:6} }, historyData:{ 9:[1,2,3] },
              opsAll: ricas, savedAt: 9000 };
const setReal = localStorage.setItem.bind(localStorage);
localStorage.setItem = () => { const e=new Error('QuotaExceededError'); e.name='QuotaExceededError'; throw e; };
try { R.aplicado = applySyncPayload(doc); }
catch (e) { R.LANZO = String(e && e.name) + ': ' + String(e && e.message); }
finally { localStorage.setItem = setReal; }
R.discoOps      = JSON.parse(localStorage.getItem('balance-ops')).map(o=>o.id);
R.discoMeta     = JSON.parse(localStorage.getItem('balance-meta-v2'));
R.memoriaCarteras = portfolios.map(p=>p.name);
R.memoriaCurrent  = currentPortId;
R.memoriaNextId   = nextId;
console.log(JSON.stringify(R, null, 2));
process.exit(0);
