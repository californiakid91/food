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
| 1 | Guardado que no miente | 3 | In progress (2/3 ciclos; transición devolvió un hallazgo) | - |
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

- [ ] 01-03: El cerrojo del libro ilegible — abierto por la transición de fase del 2026-08-30

**La fase NO está cerrada.** Los tres objetivos del scope están en el código, medidos uno a uno
contra él, desplegados y verificados en el navegador real. Lo que la mantiene abierta es otra cosa:
la **transición de fase** (2026-08-30) encontró un defecto de correctness introducido en la propia
fase — el cerrojo que impide escribir sobre un libro ilegible se levanta antes de confirmar la
reparación, y el cruce de esas dos condiciones no lo mide ninguna autoprueba. Se arregla en el
ciclo 01-03. Acta completa: `.paul/phases/01-guardado-fiable/01-TRANSICION.md`.

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
*Last updated: 2026-08-29*
