# Project State

## Project Reference

See: .paul/PROJECT.md (updated 2026-08-29)

**Core value:** Llevar al día tus carteras con precios manuales y sacar de ahí una declaración de la renta correcta, sin backend propio.
**Current focus:** v0.1 Datos fiables — Fase 1 "Guardado que no miente"

## Current Position

Milestone: v0.1 Datos fiables (v0.1.0)
Phase: 1 of 6 (Guardado que no miente) — **ABIERTA tras la segunda transición**
Planes: 01-01 CERRADO (`dd13e42` + `86ad865` + `80d523f`); 01-02 CERRADO (`77f8cef` +
`56795eb` + acta); 01-03 CERRADO (`96c7a3e`, desplegado y verificado en el navegador);
**01-04 PLANIFICADO Y REVISADO** (`01-04-PLAN.md`, versión 2)
Status: la SEGUNDA transición de la Fase 1 midió los tres objetivos del alcance contra el código
sobre el diff completo `69f728e..HEAD`: los tres en **PASS**. Pero la **META de la fase FALLA**:
hay tres escrituras a la nube y sólo dos pasan por la guarda de no-vaciado. La tercera, en el
manejador de inicio de sesión, se recorre también cuando la lectura de la nube FALLA y sube un
libro vacío encima de uno completo, con el indicador en verde. Fichado como **D-33** (y **D-34**,
dos `catch` vacíos dentro de `buildSyncPayload`), y **son el objetivo del ciclo 01-04**, no deuda
diferida: ficharlos y cerrar la fase la blanquearía como hecha.
Last activity: 2026-08-30 — segunda transición de la Fase 1. Puerta verde por sus DOS variantes,
árbol en exclusiva, despliegue idéntico a lo medido. Cuatro brazos adversarios disjuntos (radio de
impacto, objetivos contra código, seguridad, documentos contra evidencia). Acta:
`01-TRANSICION-2.md`. Ocho fichas nuevas: D-27 a D-34.

Progress:
- Milestone: [█░░░░░░░░░] 14% (1 de 7 fases, contando la 0)
- Phase: [████████░░] 80% (3 ciclos cerrados; la meta de la fase falla por D-33 → falta el 01-04)

## Loop Position

Current loop state:
```
PLAN ──▶ APPLY ──▶ UNIFY
  ✓        ○        ○     [01-04 — plan revisado, listo para APPLY]
```

Ciclos 01-01, 01-02 y 01-03: cerrados. La transición de fase NO cerró la fase: devolvió un hallazgo
de correctness que contradice su meta. El PLAN 01-04 está escrito y **ya pasó la revisión
adversaria**: se le dieron ocho frases concretas a demoler y tumbó CUATRO, todas verificadas
después contra el código. El plan se reescribió entero (versión 2, diez enmiendas E-1..E-10).

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
| La segunda transición tampoco cierra la FASE 1: abre el ciclo 01-04 | Fase 1 transición 2 | Los tres objetivos del alcance están en PASS, pero la META no: la guarda de no-vaciado cubre dos de las tres escrituras a la nube. Es la misma forma del defecto que abrió el 01-03. Ficharlo como deuda lo blanquearía como «fase hecha» (§5.10) |
| El 01-04 cierra la CLASE, no los dos casos | Fase 1 transición 2 | Enumerar a mano las tres escrituras repetiría el defecto: una lista blanca sólo protege de lo que ya conoce (§5.15). El conjunto se deriva del código y hace falta un control que muerda si aparece una cuarta |
| Los números de línea del libro de deudas se declaran NO fiables en vez de actualizarse | Fase 1 transición 2 | La auditoría encontró casi todas desfasadas. Corregirlas una a una las deja mal otra vez mañana — es la trampa de §9. Se cierra la clase: para localizar código se usa el NOMBRE y `grep` |
| El juez de subida falla CERRADO también cuando no puede mirar los ACTIVOS | 01-04 PLAN | La revisión adversaria destapó un cruce sin medir: libro con operaciones, sin activos, y la lectura de la nube fallando. Hoy no sube por accidente —la excepción aborta el push—; la primera versión del plan lo habría convertido en «subir». El fallo cerrado estaba escrito para las operaciones y no para los activos: **la asimetría ERA el defecto** (§5.16) |
| La nube es un TRI-ESTADO, no un booleano | 01-04 PLAN | «Leída y vacía», «ilegible» y «no consultada» son tres cosas distintas. Colapsarlas en un booleano pierde exactamente la distinción que causó D-33 |
| El censo de escrituras usa DOS redes disjuntas, no una regla más lista | 01-04 PLAN | La regla «descartar receptores ligados a `new Map`/`new Set`» aplicada a `.add(` daba falso rojo con `root.classList.add`, y arreglarlo por nombre habría sido la lista blanca que la propia ficha D-33 prohíbe. Se derivan los enlaces a referencias de Firestore (red A) Y se vigila el método (red B): cazan fallos distintos |
| El manejador de inicio de sesión se extrae para poder EJECUTARLO en node | 01-04 PLAN | Hoy es una flecha anónima que ni siquiera se registra fuera del navegador. Sin extraerlo, el sabotaje de su aviso no tenía oráculo posible y declararlo mordiente habría sido §5.1 con uniforme de test |
| El sabotaje del eslabón PRODUCTOR es obligatorio, no opcional | 01-04 PLAN | Los sabotajes del juez y del censo pasan los dos aunque la marca de «paquete incompleto» no se ponga NUNCA. La inyección tiene que caer donde el error PROPAGA (§5.9): una clave corrupta sembrada en el arnés |
| D-31 se cierra por la CLASE: cero llamadas literales `setSyncUI('ok')` | 01-04 PLAN | La ficha nombraba un `catch`, pero había dos miembros más vivos —el callback de error vacío del `onSnapshot` y el verde incondicional del arranque—. Cerrar sólo el caso habría sido §5.10 en pequeño |
| Se cruzan dos boundaries y se dice en voz alta | 01-04 PLAN | `buildSyncPayload` (sólo su manejo de errores) y `funcsize.py` (extraer el localizador de funciones para no tener dos escáneres). Un boundary cruzado sin decirlo es deriva; dicho, es una decisión |
| El coste del arreglo se ficha como deuda antes de construirlo | 01-04 PLAN | Rechazar la subida por un paquete incompleto deja el libro sin copia en la nube mientras dure el fallo, sin salida en la interfaz. Es el gemelo de D-23. Mejor para el dato y peor para el operador: se escribe o no existe |
| Cuatro brazos adversarios disjuntos sustituyen a G7, que sigue ciego | Fase 1 transición 2 | El de seguridad no encontró nada y el de objetivos encontró el hallazgo que paró la fase. Brazos que miden lo mismo se corroboran en su punto ciego; éstos midieron cosas distintas |

### Deferred Issues

**Las deudas viven ahora en `.paul/DEUDAS.md`** (D-01 a D-11), que es la lista viva que se lee al
arrancar cada sesión. Esta tabla ya no se mantiene: duplicarla sería tener dos fuentes de verdad.

### Blockers/Concerns

| Blocker | Impact | Resolution Path |
|---------|--------|-----------------|
| ~~El cerrojo del libro ilegible se levanta antes de confirmar la reparación~~ | **RESUELTO** en el ciclo 01-03 (`96c7a3e`) | Arreglado, con autoprueba del cruce y diez controles positivos. Acta: `01-03-SUMMARY.md` |
| ~~La FASE 1 no se ha medido contra el código después del 01-03~~ | **RESUELTO**: medida el 2026-08-30 sobre `69f728e..HEAD` | Acta: `01-TRANSICION-2.md`. La medición cambió el resultado: destapó D-33 |
| **D-33 · una tercera escritura a la nube esquiva la guarda de no-vaciado** | **Impide cerrar la FASE 1**: contradice su meta —puede borrar el libro de la nube en silencio y con el indicador en verde | Ciclo **01-04**: cerrar la CLASE (derivar del código el conjunto de escrituras a la nube) y dejar un control que muerda si aparece una cuarta. Va con D-34 y arrastra D-31 (el aviso) |
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
Stopped at: SEGUNDA transición de la Fase 1 terminada. Puerta VERDE por sus dos variantes (manual
`rc=0` y enganche `pre-push` `rc=0`, comparados byte a byte para descartar deriva), árbol en
exclusiva (`HEAD^{tree}` idéntico antes y después de medir), y lo desplegado en Pages idéntico a lo
medido (`md5 661acd6b17aed4808c9d8367a2cd72b4`). Cuatro brazos adversarios disjuntos. **La fase NO
se cerró**: D-33 contradice su meta. Ocho fichas nuevas en el libro: D-27 a D-34.
Next action: **`/paul:apply .paul/phases/01-guardado-fiable/01-04-PLAN.md`**, en contexto LIMPIO.
El plan ya incorpora la decisión sobre D-31: entra en este ciclo y se cierra por la CLASE, no por
el caso. Cuatro tareas; la 4 es la revisión adversaria del diff, y es BLOQUEANTE.
Resume file: .paul/phases/01-guardado-fiable/01-04-PLAN.md

---
*STATE.md — Updated after every significant action*
