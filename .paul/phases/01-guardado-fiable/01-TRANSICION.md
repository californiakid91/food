# Transición de la Fase 1 — «Guardado que no miente»

**Fecha:** 2026-08-30 · **Revisión medida:** `abe5e80` · **Diff de la fase:** `69f728e..abe5e80`

**Veredicto: la fase NO cierra.** Los dos brazos de revisión de fase encontraron un defecto de
correctness introducido en la propia fase. Por `CLAUDE.md` §3.4 no se blanquea como «hecho»: se
abre el ciclo **01-03** para arreglarlo. Todo lo demás medido en esta transición queda abajo.

---

## 1. La puerta

`bash tools/verify.sh` ejecutado en exclusiva sobre `abe5e80`, árbol limpio.

```
RC=0
  OK    index.html presente y no vacio
  OK    sintaxis de index.html
  OK    autopruebas (runSelfTests)
  OK    trinquete de tamano de funciones
  OK    banco de sabotaje (los controles muerden)
  OK    lint de tools/
VERDE — todo ejercido y en verde.
```

Hash del árbol antes y después de la medición: `abe5e803c2d416ef7b336982a7a4629bab0d10a7`,
0 ficheros sucios en ambos momentos. El banco de sabotaje muta y revierte; se comprueba que
revirtió.

## 2. Los objetivos de la fase, medidos CONTRA EL CÓDIGO

No contra las actas, y después del último cambio que los afecta (`CLAUDE.md` §7).

| Objetivo del scope | Resultado | Evidencia |
|---|---|---|
| Cargar `ops` incondicionalmente al arrancar, fuera del `if` de META | **PASS** | `index.html:3261`: `ops = loadOpsAll()` es la primera sentencia de `initPortfolios`, antes del `try` que lee META, con el motivo escrito al lado |
| Los `catch` vacíos de `saveOpsAll`/`saveRows`/`saveMeta` avisan en vez de decir «Guardado ✓» | **PASS** | `index.html:1019`, `3178`, `3191`: los tres registran el error y devuelven `false`; `saveRows` además pinta el aviso en rojo. `saveOpsAll` añade el cerrojo del libro ilegible |
| `applySyncPayload` deduplica por `id`, nunca por huella | **PASS** | `index.html:2990` usa `dedupeOpsById` (clave `id` + huella, `index.html:1062`). `dedupeOps` (sólo huella) queda donde debía: importación y formato antiguo |

**Catch vacíos restantes en el fichero: 4**, ninguno en el camino de guardado del libro —
`index.html:1216` (migración FIFO por cartera), `2807` y `2818` (caché del tipo de cambio),
`2831` (re-render tras actualizar el cambio). El de `1216` silencia una escritura a
`localStorage`; queda señalado, no es de esta fase.

## 3. G7 — radio de impacto: **DEGRADADO y sustituido**

El instrumento previsto, `code-review-graph`, **no ve el producto**: no parsea el JavaScript
inline de un `.html`. Tras `build`, su grafo tiene 49 nodos en 10 ficheros y **ninguno es
`index.html`** (consultado contra `.code-review-graph/graph.db` agrupando por `file_path`).
`detect-changes --base 69f728e` devuelve rc=0 y «25 funciones cambiadas · Untested: roto, main,
noop, el, k» — nombres de `tools/` y `sync.py`. Un verde sobre el fichero que no miró.

Esto queda como **D-22**. El brazo no se saltó: se sustituyó por un análisis de radio de impacto
con grep dirigido, ejecutado por un revisor adversario con prohibición explícita y nominal de
mutar el árbol. Resultados:

- **Código muerto: ninguno.** Las 22 funciones de producción tocadas tienen llamante de producción.
- `sembrarCentinelas` y `clavesGuardadas` sólo las llaman las autopruebas, pero se cargan siempre
  en el navegador del usuario. Observación, no defecto.
- **Seis huecos de cobertura**, de los cuales los dos primeros son graves:
  - la guarda de no-vaciado del lado de SUBIDA nunca se ha ejecutado (ya registrado: **D-15**);
  - el cruce «libro local ilegible + libro vacío desde la nube» no lo mide nadie → **ciclo 01-03**;
  - `migrateOpsToGlobal` con blob ilegible, sin autoprueba → **D-21**;
  - el estado `pendiente` de `setSyncUI` sólo se alcanza desde la guarda no ejercida (dentro de D-15);
  - la cadena `schedSave` → `saveMensaje` → `guardarTodo` no se ejerce en node (cosmético);
  - el cuerpo real de `showSaveIndicator` nunca corre en tests (ya registrado: **D-18**).

## 4. G8 — seguridad: **APTO CON RESERVAS**

Diff netamente defensivo. Sin superficie nueva de inyección, sin secretos, sin dominios nuevos.

| Categoría | Resultado |
|---|---|
| Inyección en el DOM | **Sin hallazgos.** 31 usos de `innerHTML` antes y 31 después; el único nuevo del diff está en `tools/dom_stub.js`, inerte y fuera del navegador. Los 31 preexistentes no se auditaron: fuera de alcance |
| Secretos | **Sin hallazgos.** Ningún commit del rango añade claves ni credenciales. `firestore.rules` existe y limita cada documento a su `uid` autenticado |
| Peticiones de red | **Un solo cambio, benigno.** La lectura del propio documento del usuario en la guarda de subida. Ningún `fetch`/XHR/WebSocket nuevo |
| Integridad de datos | Tres reservas → **D-19**, **D-20**, y la ya conocida **D-01** (la guarda sólo distingue vacío de no-vacío; un libro *casi* vacío sigue pisando uno lleno, y eso es Fase 3) |

**Limitación declarada:** no se ha verificado que `firestore.rules` esté DESPLEGADO en el proyecto
Firebase real. El fichero en el repo no prueba nada sobre la nube. Comprobarlo exige la consola o
la CLI de Firebase, y no se ha hecho.

## 5. El hallazgo que impide cerrar

**El cerrojo del libro ilegible se levanta antes de confirmar la reparación.**

En `applySyncPayload` (`index.html:2980-2991`), cuando el libro local está marcado como ilegible y
llega un `opsAll` de la nube, `opsIlegible` se pone a `false` de inmediato — antes de que
`saveOpsAll` (línea 2990) confirme que la escritura ocurrió.

Escenario concreto, verificado leyendo el código:

1. El libro local no parsea → `loadOpsAll` devuelve `[]`, marca `opsIlegible = true` y rescata el
   contenido en `balance-ops-rescate-<fecha>`.
2. Llega de la nube un documento con `opsAll: []` (nube legítimamente vacía, o un dispositivo que
   subió vacío antes de que existiera la guarda).
3. El cerrojo se levanta (2981). `vaciariaElLibro([], [])` devuelve `false` — no salta, porque el
   libro local en memoria también está vacío.
4. `saveOpsAll(dedupeOpsById([]))` escribe `[]` **encima del blob ilegible**.

**Daño:** acotado, no definitivo — la copia de rescate sobrevive, y por eso esto no es una pérdida
de datos. Pero el mecanismo que protege queda desarmado antes de tiempo, y si `saveOpsAll` fallara
(cuota agotada), `opsIlegible` se quedaría en `false` sin que nada se hubiera escrito: el siguiente
`schedSave` escribiría encima con el cerrojo ya levantado.

Es literalmente `CLAUDE.md` §5.5: las dos condiciones están medidas por separado —hay autoprueba
del libro ilegible y autoprueba del no-vaciado— y **el cruce de las dos no lo mide nada**.

**Decisión del operador (2026-08-30):** abrir el ciclo **01-03** y arreglarlo. No se registra como
deuda: una deuda de correctness dentro de una fase dada por cerrada es exactamente lo que la norma
prohíbe.

## 6. Higiene

`tools/__pycache__/funcsize.cpython-312.pyc` estaba commiteado. Sacado del índice y añadidas a
`.gitignore` las reglas de `__pycache__/`, `*.pyc` y `.code-review-graph/`.

## 7. Qué queda para cerrar la Fase 1

1. Ciclo **01-03**: el defecto del §5, con su invariante en `runSelfTests()`, su sabotaje
   permanente, la puerta verde, despliegue y comprobación en el navegador real recargando dos veces.
2. Repetir esta transición sobre el diff resultante.
3. Sólo entonces: `PROJECT.md`, `ROADMAP.md`, `paul.json` y el commit de cierre de fase.
