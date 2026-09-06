// ¿El freno propuesto sería un CALLEJÓN? Se mide sobre los eslabones de HOY:
// el sello de saveMeta y el veredicto del juez de bajada.
const R = {};
const pobres=[{id:'o1',date:'2024-01-01',type:'buy',ticker:'A',titulos:1,price:1,currency:'EUR'},
              {id:'o2',date:'2024-01-02',type:'buy',ticker:'A',titulos:1,price:1,currency:'EUR'}];
localStorage.setItem('balance-ops', JSON.stringify(pobres));
localStorage.setItem('balance-meta-v2', JSON.stringify({portfolios:[{id:7,name:'C'}],currentPortId:7,nextId:8,savedAt:1000}));
localStorage.setItem('balance-rows-7', JSON.stringify({rows:[{id:1,name:'A'}],nextId:2}));
portfolios=[{id:7,name:'C'}]; currentPortId=7; nextId=8; opsIlegible=false; ops=loadOpsAll(); rows=loadRows(7);
const nube = { portfolios:[{id:7,name:'C'}], currentPortId:7, nextId:8, opsAll:[], savedAt: 9000 };
for (let i=0;i<42;i++) nube.opsAll.push({id:'n'+i,date:'2024-02-01',type:'buy',ticker:'R',titulos:1,price:1,currency:'EUR'});

R.antesDeLiberar = JSON.parse(localStorage.getItem('balance-meta-v2')).savedAt;
// El operador libera espacio borrando una operación y la app guarda.
ops = ops.slice(0,1);
R.guardarTodo = guardarTodo();
R.savedAtTrasGuardar = JSON.parse(localStorage.getItem('balance-meta-v2')).savedAt;
R.selloMayorQueLaNube = R.savedAtTrasGuardar > 9000;

// ¿Volvería a aplicarse la nube (que es lo ÚNICO que levanta el freno)?
R.veredictoTrasLiberar = decidirBajada({ ops: ops, hayActivosLocales: hasRealLocalData(),
                                         savedAt: R.savedAtTrasGuardar }, nube);
R.veredictoRelojCero  = decidirBajada({ ops: ops, hayActivosLocales: true, savedAt: 0 }, nube);
console.log(JSON.stringify(R, null, 2));
process.exit(0);
