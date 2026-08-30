# Project State

## Project Reference

See: .paul/PROJECT.md (updated 2026-08-29)

**Core value:** Llevar al día tus carteras con precios manuales y sacar de ahí una declaración de la renta correcta, sin backend propio.
**Current focus:** v0.1 Datos fiables — Fase 1 "Guardado que no miente"

## Current Position

Milestone: v0.1 Datos fiables (v0.1.0)
Phase: 1 of 6 (Guardado que no miente) — en curso
Planes: 01-01 CERRADO (`dd13e42` + `86ad865` + `80d523f`); 01-02 CERRADO (`77f8cef` +
`56795eb` + acta); **01-03 CERRADO** (`96c7a3e`, desplegado y verificado en el navegador)
Status: los 5 AC del 01-03 en PASS con su evidencia. El cerrojo del libro ilegible ya no se levanta
sin una escritura de reparación confirmada, y el cruce que nadie medía tiene autoprueba propia y
diez controles positivos. **La FASE 1 sigue abierta**: cerrarla exige repetir la transición sobre
`abe5e80..96c7a3e`, y el cierre de un ciclo nunca autoriza el de una fase.
Last activity: 2026-08-30 — ciclo 01-03 ejecutado, revisado por cuatro brazos, desplegado a Pages
y verificado en el navegador real (90 operaciones y 4 carteras, idénticas antes y después de
`?selftest=1`). Acta en `01-03-SUMMARY.md`

Progress:
- Milestone: [█░░░░░░░░░] 14% (1 de 7 fases, contando la 0)
- Phase: [█████████▓] 95% (ciclo 01-03 cerrado y desplegado; falta repetir la transición de fase)

## Loop Position

Current loop state:
```
PLAN ──▶ APPLY ──▶ UNIFY
  ✓        ✓        ✓     [01-03 cerrado — `96c7a3e`]
```

Ciclos 01-01, 01-02 y 01-03: cerrados. **Parar aquí** (`CLAUDE.md` §1): no se encadena otro ciclo
en la misma sesión. Lo siguiente es la transición de fase, en contexto limpio.

## Performance Metrics

**Velocity:**
- Total plans completed: 4
- Average duration: —
- Total execution time: —

**By Phase:**

| Phase | Plans | Total Time | Avg/Plan |
|-------|-------|------------|----------|
| 00-hotfix-decimal | 1/1 | — | — |
| 01-guardado-fiable | 3/3 | — | — |

## Accumulated Context

### Decisions

| Decision | Phase | Impact |
|----------|-------|--------|
| Bug de la coma como Fase 0 fuera del ciclo | Fase 0 | Ya desplegado; el resto va por PLAN→APPLY→UNIFY |
| Fiscal antes que UX | Roadmap | Fases 3-4 antes que la 5 |
| Autopruebas con `?selftest=1`, sin build system | Fase 0 | Cada fase añade su invariante a `runSelfTests()` |
| Sin SonarQube ni audit enterprise | Init | No se crea `.paul/config.md` |
| Adoptada la doctrina de `CLAUDE.md` | 2026-08-29 | Todo PLAN lleva revisión adversaria; nada se cierra sin la puerta en verde |
| La puerta es `tools/verify.sh` | 2026-08-29 | Enganchada a `pre-push`; 16 controles con sabotaje que demuestra que muerden |
| Ninguna cifra medida se copia a los documentos | 01-01 | Vive sólo en la foto sellada; se desactualizó dos veces el mismo día |
| No sellar con amnistía al estrenar el trinquete | 01-01 | Se trocea la función; aflojar la vara el primer día haría rutina la amnistía |
| Un único juez para las dos guardas de no-vaciado | 01-02 | `vaciariaElLibro` + `opsDelDocumento`: la misma función en los dos lados, no el mismo criterio escrito dos veces |
| Fallar CERRADO si no se puede leer la nube | 01-02 | Se prefiere perder sincronía a perder el libro; y se ve en naranja, no en verde |
| Los controles de las autopruebas viven en el ARNÉS | 01-02 | Uno dentro de la suite sería juez y parte; el de datos reales está en `run_selftests.py` |
| La transición de fase abre el ciclo 01-03 en vez de cerrar la fase | Fase 1 transición | El brazo de radio de impacto encontró un cruce sin medir que deja escribir un libro vacío sobre uno ilegible. Registrarlo como deuda lo blanquearía como «fase hecha»; se arregla |
| G7 se declara DEGRADADO y se sustituye, no se salta | Fase 1 transición | `code-review-graph` no parsea el JS inline de un `.html`: 0 nodos de `index.html`. Un verde suyo sobre esta fase sería un falso verde |
| El arreglo del cerrojo cierra la CLASE, no el caso: la rama del formato antiguo también repara | 01-03 PLAN | La revisión adversaria vio que un dispositivo sin actualizar no podría reparar nunca, porque `loadOpsAll` re-marca el cerrojo y `saveOpsAll` se niega. Cerrar sólo `opsAll` habría dejado el mismo defecto vivo por el otro camino (§5.15) |
| El coste del arreglo se registra como deuda en vez de esconderse | 01-03 PLAN | El arreglo convierte un caso recuperable-con-pérdida-acotada en un bloqueo silencioso indefinido. Es mejor para el dato y peor para el operador; se dice por escrito o no existe |
| La reparación llama a la escritura CRUDA, no a la puerta | 01-03 | Si pasara por `saveOpsAll`, con el cerrojo puesto no podría escribir jamás: el libro quedaría bloqueado para siempre. Desde este ciclo tiene mutante propio |
| Los checks enmascarados por la relectura se ANOTAN, no se borran | 01-03 | `applySyncPayload` termina releyendo el disco, así que varios checks del cerrojo pasan con y sin el arreglo. Documentan el estado esperado; lo que no se hace es confiar en ellos. Lo que mide de verdad es la llamada directa a `repararLibroIlegible` |
| Los cuatro hallazgos de correctness ajenos al ciclo se difieren por escrito | 01-03 UNIFY | D-24 exige releer el disco en cada guardado y cambiar el contrato de `escribirOpsAll` recién fijado; D-26 exige cambiar qué compara `--check`, que el instrumento declara DERIVA (rc=3). Rediseñar la pieza recién puesta dentro de un ciclo que va de otra cosa es mover la vara sin plan |
| Cerrar el ciclo 01-02 sin cerrar la FASE 1 | 01-02 UNIFY | Los 3 objetivos del scope están en el código, medidos uno a uno; pero ningún eslabón se ha visto en un navegador y nada está desplegado. Una sonda verde no supera a un intento real |

### Deferred Issues

**Las deudas viven ahora en `.paul/DEUDAS.md`** (D-01 a D-11), que es la lista viva que se lee al
arrancar cada sesión. Esta tabla ya no se mantiene: duplicarla sería tener dos fuentes de verdad.

### Blockers/Concerns

| Blocker | Impact | Resolution Path |
|---------|--------|-----------------|
| ~~El cerrojo del libro ilegible se levanta antes de confirmar la reparación~~ | **RESUELTO** en el ciclo 01-03 (`96c7a3e`) | Arreglado, con autoprueba del cruce y diez controles positivos. Acta: `01-03-SUMMARY.md` |
| La FASE 1 no se ha medido contra el código DESPUÉS del 01-03 | No puede cerrarse la fase: el cierre de un ciclo nunca autoriza el de una fase | Repetir la transición sobre `abe5e80..96c7a3e`, en contexto limpio, midiendo los objetivos contra el código antes de preguntar nada |
| G7 (radio de impacto) no ve `index.html` | La transición de fase no tiene instrumento propio; hoy se hace a mano | D-22. Se cierra cuando el grafo indexe el `<script>`, o cuando el sustituto sea un script del repo cableado a la puerta |

## Verificación manual de la Fase 1 — app desplegada, 2026-08-30

Hecha sobre `https://californiakid91.github.io/food/` con `feb643b` publicado. Confirmado antes de
empezar que Pages servía la versión nueva (huella del fichero descargado idéntica a la local) y que
el navegador del operador la tenía cargada (`typeof dedupeOpsById === 'function'` en consola, no
por el aspecto de la pantalla).

| Punto | Resultado | Evidencia |
|---|---|---|
| Aviso verde «Guardado ✓» al guardar | **PASS** | visto en pantalla por el operador |
| El naranja «Cambios sin subir» NO sale en uso normal | **PASS** | el puntito quedó verde |
| `?selftest=1` deja los datos intactos | **PASS** | **90 operaciones y 4 carteras, idénticas antes y después**, contadas en consola. Es el fallo que estaba vivo en producción |
| `?selftest=1` imprime «✅ Autopruebas OK» | **PASS** | leído en la consola del navegador |
| El aviso sale en ROJO cuando el guardado falla | **NO COMPROBADO** | → **D-18**. Exige agotar el almacenamiento del navegador; no se improvisó con 90 operaciones reales delante |

Los dos últimos se comprobaron por separado a propósito: el fallo original consistía justamente en
imprimir «OK» **mientras** borraba, así que «no borró» y «dijo OK» son afirmaciones independientes.

### Segunda pasada — ciclo 01-03, `96c7a3e`, 2026-08-30

Misma disciplina: confirmado antes de mirar nada que Pages servía la versión nueva (huella
`661acd6b17aed4808c9d8367a2cd72b4`, idéntica a la local; el primer intento devolvió la anterior).

| Punto | Resultado | Evidencia |
|---|---|---|
| El navegador tiene el código nuevo | **PASS** | `typeof repararLibroIlegible === 'function'` en consola |
| `?selftest=1` imprime «✅ Autopruebas OK» | **PASS** | leído en la consola |
| `?selftest=1` deja los datos intactos | **PASS** | **90 operaciones y 4 carteras**, leídas de `balance-ops` y `balance-meta-v2` antes y después. Las mismas que en la pasada anterior |
| El aviso sale en ROJO cuando el guardado falla | **NO COMPROBADO** | sigue siendo **D-18**; el 01-03 no lo tocó |

## Boundaries (Active)

Del PLAN 01-03 (ya ejecutado; se mantienen como invariantes vivos):

- `vaciariaElLibro` / `tieneOperaciones` / `opsDelDocumento` intactos: son el juez único del 01-02
- `rescatarOpsIlegible` intacto: es la red que hace que este defecto no sea pérdida de datos
- `dedupeOps` / `opFingerprint` intactos: los necesitan `migrateOpsToGlobal` y el formato antiguo `opsData`
- `parseNum` / `numIn` / `parseLooseNum` no se tocan (Fase 0)
- `buildSyncPayload` y la resolución por `savedAt` son Fase 3; `computeFifo` y `exportTaxExcel`, Fase 4
- No se cierran D-01, D-15, D-18, D-21 ni D-22 en este ciclo

Permanentes del proyecto:

- `index.html` sigue siendo un fichero único sin build system ni dependencias nuevas
- No reintroducir la obtención automática de precios

## Session Continuity

Last session: 2026-08-30
Stopped at: ciclo 01-03 CERRADO, desplegado (`96c7a3e`) y verificado en el navegador real. Puerta
verde por las dos variantes (a mano y `pre-push`), 30 controles de sabotaje mordiendo, árbol
idéntico antes y después de medir. Cuatro deudas nuevas registradas: D-23, D-24, D-25, D-26.
Next action: **transición de la Fase 1**, en contexto LIMPIO. Medir los tres objetivos del scope
contra el código sobre el diff `abe5e80..96c7a3e` ANTES de preguntar nada, y preguntarse por cada
medición heredada «¿qué eslabón NO miró?». G7 sigue DEGRADADO (D-22): sustituirlo a mano, no
aceptar su verde.
Resume file: .paul/phases/01-guardado-fiable/01-03-SUMMARY.md

---
*STATE.md — Updated after every significant action*
