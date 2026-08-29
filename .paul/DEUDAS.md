# Libro de deudas — food

> **Lista VIVA, no un acta.** Se lee al arrancar cada sesión. Toda deuda diferida en un UNIFY sube
> aquí en el MISMO commit, con su origen citado. Si una deuda sólo existe en un SUMMARY, es como
> si no existiera. Norma completa en `CLAUDE.md` §8.
>
> Cada ficha dice: **qué es · cómo se midió · estado · qué la reabre.**

Última medición contra el código: **2026-08-29**, revisión `9b88521` + trabajo en curso.

---

## Abiertas — riesgo de pérdida de datos

### D-01 · El sync reemplaza el libro de operaciones en vez de fusionarlo
- **Qué es:** `applySyncPayload` sustituye `ops` entero por lo que venga de la nube, con
  last-write-wins por un único `savedAt` de documento. Importar operaciones en el móvil sin red y
  abrir luego el portátil puede borrarlas sin aviso.
- **Cómo se midió:** lectura del código en la auditoría del 2026-08-29 (`index.html:2874`,
  `2911`). **No reproducido en vivo**: el comportamiento de Firestore con escrituras encoladas
  offline está razonado sobre la semántica documentada de `set()`, no observado.
- **Estado:** planificada como Fase 3 del roadmap. Depende de tener backup antes (D-02).
- **Qué la reabre:** cualquier cambio en `buildSyncPayload`/`applySyncPayload` antes de la Fase 3.

### D-02 · No existe copia de seguridad fuera de Firestore
- **Qué es:** todo el estado vive en localStorage y en un único documento de Firestore que se
  pisan mutuamente. No hay exportación ni restauración.
- **Cómo se midió:** búsqueda de código de backup/restore en `index.html` — no hay ninguno.
- **Estado:** planificada como Fase 2. Arrastrada desde 2026-05-30.
- **Qué la reabre:** nada; está en cola.

### D-03 · El documento de Firestore crece hacia el límite de 1 MB
- **Qué es:** `buildSyncPayload` mete todos los snapshots mensuales de todos los activos en UN
  documento. Firestore corta en 1 MB, y el fallo de `set()` sólo hace `console.error`
  (`index.html:2945`) mientras el indicador de sync sigue verde.
- **Cómo se midió:** lectura del código. **El tamaño real del payload NO se ha medido nunca.**
- **Estado:** abierta, sin fase asignada.
- **Qué la reabre:** medir el payload. Si pasa de ~500 KB, sube a fase propia.

---

## Abiertas — corrección fiscal

### D-04 · El orden de operaciones del mismo día lo decide el azar
- **Qué es:** el desempate del FIFO es lexicográfico por `id`, y `genOpId` lleva un sufijo
  aleatorio, así que una compra y una venta del mismo día pueden procesarse al revés.
- **Cómo se midió:** lectura del código (`index.html:1015`, `1042`).
- **Estado:** Fase 4, plan 04-01.
- **Qué la reabre:** nada; está en cola. Debe cerrarse antes de la próxima campaña de la renta.

### D-05 · No existe el tipo de operación «split»
- **Qué es:** un split contable dejaría el FIFO mal para siempre.
- **Cómo se midió:** búsqueda de `split` en `index.html` — cero resultados.
- **Estado:** Fase 4, plan 04-03.
- **Qué la reabre:** que el bróker haga un split antes de que se implemente.

### D-06 · La regla de los dos meses del IRPF no se avisa
- **Qué es:** una pérdida con recompra de valores homogéneos en ±2 meses no es deducible ese año.
  El Excel la declara como pérdida sin marca.
- **Cómo se midió:** lectura de `exportTaxExcel`.
- **Estado:** Fase 4, plan 04-04. **Pendiente de investigar** la redacción exacta de la norma y
  qué cuenta como valor homogéneo.
- **Qué la reabre:** nada; está en cola.

### D-07 · El tipo de cambio puede caer al de hoy
- **Qué es:** si a una operación le falta el cambio congelado, `opFx` usa el spot actual o un
  1,08 fijo. El mismo Excel da cifras distintas según el día que se genere.
- **Cómo se midió:** lectura del código (`index.html:1020`, `2703`).
- **Estado:** Fase 4, plan 04-02.
- **Qué la reabre:** nada; está en cola.

### D-08 · No se sabe si los dividendos del OCR llegan brutos o netos
- **Qué es:** el Excel avisa de revisar la retención, pero nadie ha confirmado qué importe extrae
  realmente `parseRevolutStatement` de un extracto de verdad.
- **Cómo se midió:** no se ha medido. **Requiere una captura real del operador.**
- **Estado:** abierta, bloqueada por falta de dato.
- **Qué la reabre:** que el operador comparta una captura con dividendos.

---

## Abiertas — tamaño del código

### D-09 · Doce funciones por encima del presupuesto de 60 líneas
- **Qué es:** deuda de tamaño declarada y congelada. Sólo pueden encoger; ninguna función nueva
  puede unirse a la lista.
- **Cómo se midió:** `tools/funcsize.py`, 2026-08-29, sobre 146 funciones vistas. Sellada en
  `.paul/baseline-funcs.json`. Exenciones nombradas una a una:

  | Función | Líneas | Motivo de la exención |
  |---|---|---|
  | `exportTaxExcel` | 449 | genera el Excel del IRPF entero; trocearla toca la Fase 4 |
  | `calcRebalance` | 141 | cálculo del rebalanceo; se toca en la Fase 6 |
  | `renderTable` | 132 | pintado principal de activos; se toca en la Fase 5 |
  | `drawBar` | 132 | gráfico de barras en canvas |
  | `parseRevolutTrade` | 117 | parseo de extractos, con muchos casos límite |
  | `renderGlobalPosition` | 110 | cabecera global |
  | `renderOps` | 102 | tabla de operaciones; se toca en la Fase 5 |
  | `parseRevolutStatement` | 96 | parseo de extractos |
  | `renderImportPreview` | 83 | previsualización de importación |
  | `refreshRowDerived` | 80 | recálculo incremental de una fila |
  | `drawPie` | 75 | gráfico de tarta en canvas |
  | `drawGlobalSpark` | 66 | sparkline global |

- **Estado:** congelada. El trinquete impide que empeore.
- **Qué la reabre:** tocar cualquiera de esas funciones en su fase correspondiente — es la
  ocasión de bajarla del listado.

### D-10 · El trinquete de tamaño no ve funciones flecha
- **Qué es:** `funcsize.py` sólo ve `function NOMBRE(...)` de primer nivel. Una función de 300
  líneas escrita como `const f = () => {…}` le es invisible.
- **Cómo se midió:** ceguera declarada a propósito en la cabecera del propio instrumento.
- **Estado:** abierta y **declarada**, no descubierta. Un límite declarado es un límite; uno
  descubierto después es un agujero.
- **Qué la reabre:** que aparezca código nuevo escrito con funciones flecha grandes.

---

## Abiertas — limpieza

### D-11 · `worker.js` es un proxy obsoleto
- **Qué es:** proxy de precios de Yahoo, sin uso desde que se quitó la obtención automática de
  precios.
- **Cómo se midió:** confirmado en la auditoría del 2026-08-29.
- **Estado:** Fase 6, plan 06-04. Incluye borrar también el Worker en el panel de Cloudflare.
- **Qué la reabre:** nada; está en cola.

---

## Cerradas

### D-00 · Un número tecleado con coma se multiplicaba por mil — CERRADA 2026-08-29
- **Qué era:** `parseNum` aplicaba una heurística de miles y leía `0,123` como `123`. Afectaba a
  títulos, precios y a la edición de operaciones importadas, o sea al FIFO y al Excel del IRPF.
- **Cómo se midió:** reproducido ejecutando el código real fuera del navegador antes de tocarlo.
- **Cómo se cerró:** revisión `69f728e`. En la entrada de teclado el último separador es el
  decimal; la heurística de miles se quedó sólo en el camino del OCR.
- **Qué la reabriría:** el invariante está en `runSelfTests()` y hay un sabotaje permanente que
  lo verifica. Si `tools/sabotage.py` deja de morder ahí, esta deuda vuelve a estar abierta.
