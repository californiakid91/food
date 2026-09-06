// ¿Qué queda en pantalla si la subida sale por la rama "sin sesión"?
(async () => {
  const R = {};
  const v = abrirVentanaDePintura();
  try {
    setSyncUI('error', 'algo falló antes');          // estado previo ROJO
    R.antes = { punto: v.el('sync-dot').title, texto: v.el('sync-status').textContent };
    R.resultado = await subirALaNube('sin sesion', { ref: null, paquete: buildSyncPayload,
      mirar: async () => ({estado:'vacia',ops:[],activos:0}), cerrojo: () => false, activos: () => true });
    R.despues = { punto: v.el('sync-dot').title, texto: v.el('sync-status').textContent };
  } finally { v.cerrar(); }
  console.log(JSON.stringify(R, null, 2));
  process.exit(0);
})().catch(e => { require('fs').writeSync(2, 'INSTRUMENTO ROTO: '+(e&&e.stack||e)+'\n'); process.exit(2); });
