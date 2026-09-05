# Roadmap: food

## Overview

Cerrar los 16 hallazgos de la auditoría del 2026-08-29 en seis fases, de dentro afuera: primero que el dato no se pierda ni se corrompa, luego una red de seguridad que haga reversible todo lo demás, después la corrección fiscal del FIFO, y solo al final la comodidad de uso diario y los extras. Cada fase deja su invariante blindado en `runSelfTests()`.

## Current Milestone

**v0.1 Datos fiables** (v0.1.0)
Status: In progress
Phases: 1 of 7 complete (Fase 0)

## Phases

| Phase | Name | Plans | Status | Completed |
|-------|------|-------|--------|-----------|
| 0 | Hotfix separador decimal | 1 | Complete | 2026-08-29 |
| 1 | Guardado que no miente | 7 (+1 por planificar) | In progress (**7 ciclos cerrados y CINCO transiciones**; la quinta, del 2026-09-05, midió la fase contra el código y **la fase NO cierra**: abre el ciclo **01-08**) | - |
| 2 | Backup y restauración | 2 | Not started | - |
| 3 | Sync que fusiona | 2 | Not started | - |
| 4 | Corrección fiscal del FIFO | 4 | Not started | - |
| 5 | UX del uso diario | 3 | Not started | - |
| 6 | Extras de valor | 4 | Not started | - |

## Phase Details

### Phase 0: Hotfix separador decimal [COMPLETE]

**Goal:** Que un número tecleado con coma deje de multiplicarse por mil.
**Depends on:** Nothing
**Research:** Unlikely

**Scope:**
- `parseNum`: el último separador tecleado es el decimal; `parseLooseNum` conserva su heurística de miles para el OCR
- `runSelfTests()` con `?selftest=1` cubriendo el round-trip `parseNum(numIn(x)) === x`

**Plans:**
- [x] 00-01: Arreglo desplegado en `69f728e` — 2026-08-29

### Phase 1: Guardado que no miente

**Goal:** Que ningún fallo de guardado ni de arranque pueda borrar el libro de operaciones en silencio.
**Depends on:** Fase 0
**Research:** Unlikely (código propio)

**Scope:**
- Cargar `ops` incondicionalmente al arrancar, fuera del `if` de META (`index.html:3061`) — hoy, si META se corrompe, el primer `schedSave` escribe `[]` sobre `balance-ops` (`index.html:3037`)
- Los `catch(e){}` vacíos de `saveOpsAll`/`saveRows`/`saveMeta` deben avisar en la UI en vez de mostrar "Guardado ✓" (`index.html:3019`)
- `applySyncPayload` debe deduplicar por `id`, nunca por huella; la huella se queda solo en la importación (`index.html:988`, `2874`)

**Plans:**
- [x] 01-01: Arranque y guardado honestos — cerrado 2026-08-29 (`dd13e42`, `86ad865`) — carga incondicional de `ops`, rescate de un libro ilegible, errores de guardado visibles
- [x] 01-02: Sincronización que no destruye — cerrado 2026-08-30 (`77f8cef`, `56795eb`) — identificadores sin colisión, deduplicación por identificador Y huella, guardas simétricas de no-vaciado (añadido por la revisión adversaria del 01-01)

- [x] 01-03: El cerrojo del libro ilegible — cerrado 2026-08-30 (`96c7a3e`) — la escritura del libro separada de
  su cerrojo, que ahora sólo se levanta tras confirmar la reparación; el cruce «ilegible × nube vacía» con
  autoprueba propia; el formato antiguo también repara; 10 controles positivos nuevos en el banco

- [x] 01-04: Una sola puerta de subida — cerrado 2026-08-31 (`21e1edb`) — las tres escrituras a
  Firestore reducidas a UNA, decidida por una función pura que falla cerrado y de forma simétrica
  cuando no puede mirar la nube; cero verdes escritos a mano; dos instrumentos nuevos cableados a
  la puerta (`cloudwrites.py`, `emptycatch.py`); 14 sabotajes nuevos mordiendo

**La fase SIGUE abierta tras su CUARTA transición (2026-09-01) — abrió el ciclo 01-07, ya cerrado.**
**Pendiente la QUINTA transición**, que es quien puede cerrar la fase. Las cuatro anteriores midieron
la meta contra el código y **las cuatro cambiaron el resultado**.
El detalle de la cuarta está al final de este bloque; lo que sigue es el registro de la tercera.

El defecto que paró la fase en la segunda transición (D-33) está cerrado y con control positivo, y
el ciclo 01-04 está desplegado y visto en el navegador. Lo que impide cerrar la fase ahora es otra
cosa, medida y no opinable:

**Los tres objetivos del ALCANCE están en PASS, pero la META no.** La meta dice «sin que el
operador se entere», y el aparato de medición **no cubre la capa de aviso**: pintar en VERDE un
guardado que ha fallado deja la puerta entera en `rc=0` y «VERDE — todo ejercido y en verde».
Nueve mutantes de esa capa sobreviven. Un fallo que se pinta verde ES, para el operador, el
borrado en silencio que esta fase existe para impedir. Ficharlo como deuda lo blanquearía como
«fase hecha» (§5.10) — la misma decisión que se tomó en las dos transiciones anteriores.

Además: los dos trinquetes se rompen con `rc=1` y traceback en vez de fallar cerrado, y la puerta
los rotula entonces como si el código hubiera engordado; `VERIFY_INNER=1` sale con `rc=0` sin
correr el banco; y nada vigila que el enganche `pre-push` exista.

**Es la TERCERA vez consecutiva que medir cambia el resultado.** `PLAN == SUMMARY` habría cerrado
la fase las tres veces.

**Aviso para quien repita la transición:** G7 (radio de impacto) sigue **DEGRADADO** —
`code-review-graph` no ve el JS dentro de `index.html` (**D-22**). Se sustituye a mano por cuatro
brazos adversarios disjuntos, cada uno con una FRASE concreta que demoler. En esta transición los
cuatro demolieron su frase y **cada uno encontró algo que ninguno de los otros vio**: el de
documentos no vio un mutante, y el del oráculo no vio una cifra falsa.

**Planes:** 01-01, 01-02, 01-03 y 01-04 cerrados. La tercera transición abre **DOS** ciclos, y se
partieron a propósito tras la revisión adversaria del primer borrador:

- [x] **01-05: La vara de medir** — cerrado 2026-08-31 (`4e81e6c`). Cierra **D-39** (los trinquetes
  fallan CERRADO, rc=2 con nombre, clave y remedio), **D-40** (la variante interior devuelve rc=4,
  que no es verde para nadie salvo el banco, **y** el enganche limpia la variable: dos capas) y
  **D-41** (`tools/hookcheck.py`, cableado a la puerta, deriva lo esperado del instalador).
  **`index.html` intacto byte a byte** y ninguna foto resellada, que es la prueba de que los
  instrumentos siguen midiendo lo mismo. Abre **D-42** y **D-43**. Re-derivadas en fresco: 9 pasos
  en la puerta, 52 mordidas del banco, 61 controles verdes, **11 de este ciclo**.
  Acta: `01-05-SUMMARY.md`.
- [x] **01-06: El aviso que no miente** — **APPLY hecho y revisado 2026-08-31**. Cierra
  **D-38** ENTERA: los dos pintores ejecutados de verdad fuera del navegador (color, texto,
  visibilidad y duración con reloj falso), el campo `aviso` del juez de subida en todas sus ramas
  de rechazo, los avisos de consola por mensaje literal, y una red **por receptor** cableada a la
  puerta para que un aviso nuevo no nazca sin oráculo.
  El enfoque se decidió por **dialéctica adversaria** (dos posturas, dos rondas) y el borrador fue
  **demolido por dos brazos disjuntos**: dejaba viva una de las tres familias —un rechazo de subida
  etiquetado «todo bien» sale HOY `rc=0` con «✅ Autopruebas OK», re-verificado a mano— y su reloj
  falso sin `try/finally` podía dejar de guardar los datos del operador en silencio. Once hallazgos
  incorporados; **retirada la cifra «nueve mutantes»** por no tener artefacto.

  **Y entonces el ciclo, ya escrito y con la puerta VERDE, fue demolido otra vez por TRES brazos
  adversarios disjuntos sobre el diff: diez hallazgos más, ninguno visto por más de un brazo.** El
  peor: los asertos exigían que los colores de éxito y de fallo fueran DISTINTOS, nunca CUÁLES, así
  que **intercambiarlos —el fallo de guardado pintado en VERDE— salía `rc=0` y «✅ Autopruebas
  OK»**: el daño titular de D-38, vivo dentro del ciclo escrito para matarlo (§5.8). También: el
  error de sync en naranja pasaba, un aviso de 2 ms pasaba, el detector de cesión de control pasaba
  con el mecanismo borrado, nueve avisos reales del guardado por sync y del arranque escapaban al
  censo, y el banco restauraba la puerta en otro inodo mientras el hash decía «árbol limpio».
  Los diez arreglados dentro del ciclo. Puerta VERDE por sus dos variantes con salida idéntica;
  banco `rc=0` con **74 controles mordiendo** (eran 52) más 10 guardas.
  Acta: `01-06-SUMMARY.md`.
  **Verificación en navegador HECHA** el 2026-08-31 sobre `685b44b` desplegado: cuatro puntos en
  PASS, incluido que **guardar sigue funcionando después de las autopruebas**; 90 operaciones y 5
  carteras idénticas antes y después. Sin reportar: el estado del indicador de sincronización.
  Acta: `01-06-VERIFICACION-NAVEGADOR.md`. **LOOP CERRADO** (PLAN ✓ APPLY ✓ UNIFY ✓).

Con el 01-06 cerrado y visto en el navegador, **D-38 ya no impide nada** y no queda ningún punto de
control bloqueante antes de la CUARTA transición. El punto ciego declarado del ciclo —la fidelidad
del simulador, que no resuelve `var(--green)` a un color ni aplica CSS— se cubrió con el intento
real, que es lo único que supera a una sonda verde. Y **el cierre de un CICLO no autoriza el cierre
de una FASE** (§7): quien decide es la medición contra el código, no el conteo de actas. Las tres
transiciones anteriores cambiaron el resultado al hacerlas.

El borrador que juntaba ambas cosas cubría seis de los nueve mutantes y llamaba a eso «cerrar la
clase». La revisión adversaria lo demolió, y además destapó que exigir «rc≠0 con `VERIFY_INNER=1`»
tal cual **mataba el banco de sabotaje**, porque el banco ejecuta la puerta con esa misma variable.
Los dos hallazgos se verificaron con comando propio antes de aceptarlos.

Actas: `01-04-SUMMARY.md`, `01-TRANSICION-3.md` y `01-05-SUMMARY.md`.


---

#### CUARTA transición (2026-09-01) — la fase tampoco cierra: abre el ciclo 01-07

Medida sobre `571659c`, árbol limpio, con la huella de `index.html` confirmada idéntica a la que
sirve Pages. Puerta fresca: `rc=0`, diez pasos, VERDE.

**Dos cosas cambiaron respecto a las tres transiciones anteriores, y las dos son buenas:**

1. **Por primera vez un brazo NO demolió su frase.** El de instrumentos y cableado intentó cinco
   roturas concretas del aparato de medición y ninguna cedió; el fallo cerrado se reprodujo uno a
   uno en los ocho instrumentos (rc=2 con nombre y remedio), las dos variantes de la puerta ejercen
   lo mismo, y no hay un solo script huérfano.
2. **Por primera vez ninguna cifra publicada es falsa.** Las cuatro re-derivadas en fresco —74
   controles del banco, 34 avisos censados, diez pasos, y la huella de lo desplegado— dieron
   exactamente lo que dicen los documentos. En la tercera transición había tres falsas.

**Y aun así la META no se cumple**, por dos defectos del PRODUCTO, los dos re-verificados a mano
sobre copia aislada, y los dos con la misma forma —una **ASIMETRÍA**— que ya paró las transiciones
2 y 3:

- **D-45**: `hasRealLocalData()` mira sólo los activos y **nunca el libro de operaciones**. Un
  operador con todo vendido —activos vacíos, libro fiscal rico— cae en la rama donde la comparación
  de fechas se desactiva, y **cualquier** documento de la nube gana por viejo que sea: un libro de
  tres operaciones sustituido por uno de una, con el punto de sync **en VERDE**. La puerta entera
  sale `rc=0` sobre ese código. El juez de SUBIDA ya mira las dos cosas desde el 01-04; el de
  BAJADA se quedó con el predicado viejo.
- **D-46**: quitar la lista de carteras del veredicto de `guardarTodo` deja la puerta en `rc=0` y
  VERDE. Las autopruebas ejercen el «fallo parcial» rompiendo siempre el guardado del libro, nunca
  el de META a solas: el cruce no lo mide nadie (§5.5). Con la cuota llena, el operador ve
  «Guardado ✓» en verde **y** se sube a la nube.

**Es la CUARTA vez consecutiva que medir cambia el resultado.** `PLAN == SUMMARY` habría cerrado la
fase las cuatro veces.

**Deudas re-medidas, no heredadas:** **D-15 se CIERRA** —ignorar el veredicto del juez en
`subirALaNube` da hoy `rc=1`; la cerró el 01-04 sin que nadie lo anotara—. D-42, D-43 y D-44 siguen
siendo cegueras acotadas y declaradas. D-27 y D-29 siguen vivas y van al 01-07 con D-46, porque son
la misma familia. Nueva **D-47** (sin volcado al cerrar la pestaña), que no abre ciclo por sí sola.

**Nota de proceso:** se rompió la exclusividad del árbol. Un brazo corrió el banco de sabotaje sobre
el repositorio real —el banco muta `index.html` en vivo— y al detenerlo lo dejó sucio. Lo destapó el
control de huella de otro brazo; restaurado y verificado byte a byte contra HEAD, sin pérdida. Regla
nueva en `CLAUDE.md` §3.4: **los brazos trabajan sobre COPIA y sobre el árbol real sólo LEEN** — la
prohibición se escribe por lo que EJECUTAN, no sólo por lo que editan.

**La QUINTA transición (2026-09-05) tampoco cierra la fase: abre el ciclo 01-08.** Acta:
`01-TRANSICION-5.md`. Cinco brazos adversarios disjuntos, cada uno sobre **su propia copia**, y los
cinco demolieron su frase. Los tres objetivos del ALCANCE siguen en PASS; la META no. Lo decisivo,
reproducido y **re-verificado a mano**: un libro de la nube que **no cabe** en el almacenamiento no
aterriza pero **adelanta el reloj**, y el siguiente guardado lo **exporta encima** —42 operaciones
→ 2— con «Guardado ✓» y el punto verde; y la capa de aviso del camino de nube deja **pintar verde
sobre un fallo de sincronización** con la puerta en `rc=0`. Las cinco deudas que cerró el 01-07 se
re-midieron revirtiendo su arreglo: **las cinco están bien cerradas**. Un brazo reportó como vivo
un mutante que **muere**: se corrigió al re-verificar.

**Es la QUINTA vez consecutiva que medir cambia el resultado.** `PLAN == SUMMARY` habría cerrado la
fase las cinco veces.

**Planes:**
- [ ] **01-08: El aviso de la nube y el libro que no aterriza** — por planificar. Entran **D-58**
  (una escritura fallida al aplicar no puede adelantar el reloj), **D-59** (todo pintado del camino
  de nube afirmado por color Y texto, cerrado por receptor), **D-48** (el anuncio de la lista de
  carteras depende de su escritura) y **D-61** (`avisos.py` deja de amnistiar el silencio).
  **Fuera:** D-65 (falta medir el orden en el navegador), D-60, D-62 a D-64, D-66 a D-69 y Fase 3.
- [x] **01-07: Un solo juez en las dos direcciones** — **CERRADO el 2026-09-05**, acta `01-07-SUMMARY.md`, desplegado y verificado dos veces en el navegador real. Cierra además **D-30** y **D-54**, ésta última encontrada por el propio checkpoint humano: el naranja afirmaba una causa y lo alcanzaban ocho veredictos. Abre D-48 a D-53, D-55, D-56 y D-57.

  Detalle original del plan: — cierra **D-45** (el predicado de «hay datos
  locales que proteger» tiene que contar el libro, en bajada igual que en subida) y **D-46** junto
  con **D-27** y **D-29** (la invariante «un fallo de guardado no se anuncia como éxito y no se
  sincroniza» tiene que valer en todos los caminos). **Fuera de alcance:** la fusión de `ops` por
  `id` y el `savedAt` por sección, que siguen siendo Fase 3.

Acta: `01-TRANSICION-4.md`.

### Phase 2: Backup y restauración

**Goal:** Poder recuperar el estado completo aunque Firestore y localStorage estén mal a la vez.
**Depends on:** Fase 1 (el guardado debe ser fiable antes de fiarse de una copia)
**Research:** Unlikely

**Scope:**
- Botón "Descargar copia": `buildSyncPayload()` (`index.html:2838`) a un `.json` fechado
- Botón "Restaurar copia": fichero → `applySyncPayload()` (`index.html:2860`) con confirmación previa
- Copia rotativa (3 últimas) en localStorage antes de cada `applySyncPayload`
- Invariante en `runSelfTests()`: `applySyncPayload(buildSyncPayload())` es idempotente y nunca reduce `ops.length`

**Plans:**
- [ ] 02-01: Exportar e importar JSON
- [ ] 02-02: Copia rotativa automática + invariante de idempotencia

### Phase 3: Sync que fusiona

**Goal:** Que abrir la app en otro dispositivo no pueda borrar operaciones importadas en el primero.
**Depends on:** Fase 2 (hacerlo con red de seguridad puesta)
**Research:** Likely
**Research topics:** semántica real de `set()` de Firestore con escrituras encoladas offline; si el last-write-wins por `savedAt` global puede sustituirse por `savedAt` por sección sin migración

**Scope:**
- Fusionar `ops` por `id` (unión, nunca reemplazo) en `applySyncPayload` (`index.html:2874`)
- `savedAt` por sección en vez de por documento (`index.html:2911`)
- `applySyncPayload` debe guardar META con su `savedAt` (`index.html:2882`)
- `hasRealLocalData()` debe mirar `ops`, no solo `rows` (`index.html:2890`)
- Aviso al usuario: "sincronizado: N operaciones nuevas"

**Plans:**
- [ ] 03-01: Fusión de `ops` por `id` + `savedAt` por sección
- [ ] 03-02: Guardia de push y aviso de sincronización

### Phase 4: Corrección fiscal del FIFO

**Goal:** Que el Excel de la renta salga igual se genere el día que se genere, y correcto en los casos límite.
**Depends on:** Fase 1 (libro íntegro) y Fase 2 (poder revertir)
**Research:** Likely
**Research topics:** redacción exacta de la regla de los dos meses del IRPF y qué cuenta como valor homogéneo; tratamiento contable de un split en base FIFO

**Scope:**
- Campo `seq` al importar y desempate por él antes que por `id`: hoy el orden intradía lo decide el sufijo aleatorio de `genOpId` (`index.html:1015`, `1042`)
- Tipo de operación `split` (multiplica qty y divide `unitCostEur` de los lotes vivos)
- Regla de los dos meses: marcar en `exportTaxExcel` las ventas con pérdida que tengan recompra del mismo `assetKey` a ≤2 meses
- Reparación de `opFx`: congelar con `fetchFxOn(op.date)` (`index.html:1149`) toda op con `fxApprox` o sin `fx`, en vez de caer al cambio de hoy (`index.html:1020`)
- Invariantes en `runSelfTests()`: conservación FIFO, `Σ gainEur = Σ proceeds − Σ costes`, y cierre del año N == apertura del N+1

**Plans:**
- [ ] 04-01: Orden intradía determinista (`seq`)
- [ ] 04-02: Congelado definitivo del tipo de cambio
- [ ] 04-03: Tipo de operación `split`
- [ ] 04-04: Aviso de la regla de los dos meses + invariantes FIFO en las autopruebas

### Phase 5: UX del uso diario

**Goal:** Que la tarea más frecuente (repasar precios) y la corrección de errores del OCR dejen de ser incómodas.
**Depends on:** Fase 1
**Research:** Unlikely

**Scope:**
- Vista "Actualizar precios" en bloque: ticker + precio + moneda de todos los activos, foco encadenado con Enter, reutilizando `updateRow` (hoy el precio vive en el acordeón y solo hay uno abierto, `index.html:3663`, `3570`)
- Alta y edición manual de operaciones: hoy solo entran por OCR (`index.html:2118`) y existe `deleteOp` pero no `editOp`
- `priceAt` por precio + aviso de precio rancio en la cabecera global

**Plans:**
- [ ] 05-01: Actualización de precios en bloque
- [ ] 05-02: Alta y edición manual de operaciones
- [ ] 05-03: Antigüedad del precio y aviso

### Phase 6: Extras de valor

**Goal:** Enseñar datos que la app ya guarda y cerrar el bucle del rebalanceo.
**Depends on:** Fase 5
**Research:** Unlikely

**Scope:**
- Vista del histórico mensual: los snapshots ya guardan `assets[]` completos (`index.html:945`) y solo se ven como sparkline
- Dividendos dentro del P&L: `getRowPnl` (`index.html:4403`) solo calcula `(precio − medio) × títulos`
- Rebalanceo con títulos fraccionarios: `Math.floor` (`index.html:3939`) asume acciones enteras y Revolut permite fracciones; botón "he comprado esto"
- Borrar `worker.js` (proxy Yahoo obsoleto)

**Plans:**
- [ ] 06-01: Histórico mensual navegable
- [ ] 06-02: Dividendos en el P&L
- [ ] 06-03: Rebalanceo fraccionario y aplicación en un toque
- [ ] 06-04: Limpieza de `worker.js`

---
*Roadmap created: 2026-08-29*
*Last updated: 2026-09-05*
