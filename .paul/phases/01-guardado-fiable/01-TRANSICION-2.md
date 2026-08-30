# Transición de la Fase 1 — segunda pasada

**Fecha:** 2026-08-30 · **Revisión medida:** `85d56bb` (`index.html` idéntico al de `96c7a3e`)
**Alcance de la medición:** el diff completo de la fase, `69f728e..HEAD`.

> Esta es la SEGUNDA transición de la Fase 1. La primera (`01-TRANSICION.md`, sobre `abe5e80`)
> no cerró la fase: encontró un defecto de correctness y abrió el ciclo 01-03. Este documento
> repite la medición sobre el resultado de aquel ciclo, como exige `CLAUDE.md` §7: **el cierre de
> un CICLO nunca autoriza el de una FASE, y el disparador es medir contra el código, no contar
> actas.**

---

## 1. Veredicto

> ### 🔴 La FASE 1 **NO se cierra**. Se abre el ciclo **01-04**.

Los tres objetivos del alcance están en el código y se sostienen. Lo que **no** se sostiene es la
META de la fase:

> *«Que ningún fallo de guardado ni de arranque pueda borrar el libro de operaciones en silencio.»*

Hay **una tercera escritura a la nube que esquiva la guarda de no-vaciado** y puede borrar el libro
remoto sin que el operador vea nada. La guarda existe, está bien construida y tiene juez único —
pero hay una puerta que no pasa por ella. Es literalmente la misma forma del defecto que abrió el
ciclo 01-03: *el mecanismo está, y hay un camino que no lo atraviesa*.

Registrarlo como deuda lo blanquearía como «fase hecha» (`CLAUDE.md` §5.10: un hallazgo cerrado
con la categoría equivocada es peor que uno abierto). Se arregla.

---

## 2. La puerta, en fresco y por sus DOS variantes

| Variante | Comando | Resultado |
|---|---|---|
| Manual | `bash tools/verify.sh` | **rc=0 — VERDE**, los 6 controles OK |
| Automática | `.git/hooks/pre-push origin …` | **rc=0 — VERDE**, misma salida |

Además, control de deriva entre las dos: el enganche instalado se comparó **byte a byte** con el
que genera `tools/install-hooks.sh` (extrayendo el bloque del heredoc y haciendo `diff -u`, tras
afirmar que **ninguna de las dos entradas estaba vacía** — `CLAUDE.md` §5.14). **Idénticos.**

Árbol en exclusiva: `git status --porcelain` vacío antes y después, y `HEAD^{tree}` =
`e7a40cac79e9baf0c4436adaf63bb199cc472350` sin cambios tras medir.

**Despliegue:** `md5sum index.html` local = `661acd6b17aed4808c9d8367a2cd72b4`, idéntico al que
sirve `https://californiakid91.github.io/food/index.html`. Lo publicado ES lo medido.

---

## 3. Los tres objetivos del alcance, medidos contra el código

| Objetivo | Veredicto | Evidencia |
|---|---|---|
| **OBJ-1** · cargar `ops` fuera del `if` de META | **PASS** | `initPortfolios` (`function initPortfolios`) abre con `ops = loadOpsAll();` ANTES del `try` que lee META. Un META corrupto cae al `catch` con el libro ya cargado |
| **OBJ-2** · los guardados avisan en la UI en vez de mentir | **PASS** en las tres funciones nombradas | `saveOpsAll`, `saveRows` y `saveMeta` devuelven éxito/fallo y ya no tienen `catch` vacío; `guardarTodo` sólo canta «Guardado ✓» si las tres fueron bien. **Con huecos fuera de ellas** → D-27, D-28, D-29 |
| **OBJ-3** · deduplicar por `id`, no por huella | **PASS** | la rama moderna (`opsAll`) usa `dedupeOpsById`. La huella sola sobrevive **sólo** en `migrateOpsToGlobal` y en la rama del formato antiguo `opsData` — exactamente lo que **D-13** declara aceptado, ni más ni menos |
| **META de la fase** | **🔴 FAIL** | ver §4 |

---

## 4. El hallazgo que impide el cierre

### H-1 · Una tercera escritura a la nube esquiva la guarda de no-vaciado

Censo completo de escrituras al documento de Firestore:

    grep -n "\.set(" index.html   →   3124, 3137  (dentro de schedulePush, CON guarda)
                                      3172        (dentro de onAuthStateChanged, SIN guarda)

El camino de la tercera:

    const synced = await pullFromFirestore();
    if (!synced) {
      if (hasRealLocalData()) {
        const ref = userDocRef();
        if (ref) await ref.set(buildSyncPayload());   // ← sin vaciariaElLibro
      }
    }

Tres eslabones lo vuelven destructivo:

1. **`pullFromFirestore` devuelve `false` también cuando la lectura FALLA**, no sólo cuando la
   nube está vacía: su `catch` hace `console.error` y `return false`. Un fallo transitorio de red
   es indistinguible de «no hay nada arriba».
2. **`hasRealLocalData` mira las filas de ACTIVOS, no las operaciones.** Un dispositivo con
   activos y el libro vacío o **con el cerrojo puesto** (D-23) la satisface.
3. **`buildSyncPayload` sube `opsAll: ops`**, que en ese estado es `[]`.

Resultado: se sube un libro vacío encima de una nube que tiene el libro completo. Firestore lo
encola offline y lo aplica al reconectar. Y el `catch` que envuelve todo el bloque termina en
`setSyncUI('ok')`: **el indicador se queda verde**.

**No es una regresión de esta fase.** `git show 69f728e:index.html` muestra ese bloque idéntico
antes de empezar. Pero la fase se propuso cerrar exactamente esta clase de daño, y la cerró por
dos puertas de tres. **Presencia ≠ precedencia** (`CLAUDE.md` §5.11), y una lista blanca sólo
protege de lo que ya conoce (§5.15): la guarda se puso donde se sabía que había escritura, no
derivando el conjunto REAL de escrituras del código.

### H-6 · Dos `catch {}` vacíos dentro de la función que construye lo que se sube

Medición corregida: **hay 6 `catch` vacíos, no 4.** El acta de la transición anterior contó 4
porque su patrón sólo casaba `catch (e) {}` y no la variante `catch {}` sin parámetro — la trampa
de los dos predicados asimétricos sobre el mismo conjunto (`CLAUDE.md` §5.16). Contados bien:

    grep -nE "catch *(\([a-zA-Z_$]*\))? *\{ *\}" index.html   →   1236, 2827, 2838, 2851, 2969, 2977

Los dos nuevos (2969, 2977) están **dentro de `buildSyncPayload`**: si al leer los activos o el
histórico de una cartera falla el `JSON.parse` o el `getItem`, esa cartera **se omite del paquete
en silencio** y se sube un documento incompleto encima del bueno. Misma clase de daño que H-1,
sobre los activos en vez de sobre el libro.

Los otros cuatro son de caminos de precio y de FX; se fichan aparte, no bloquean.

---

## 5. Estado de G7 (radio de impacto): sigue DEGRADADO, y de nuevo se sustituye

`code-review-graph` no parsea el JavaScript inline de un `.html`, así que no ve `index.html`, que
ES el producto. Un verde suyo sobre esta fase sería un falso verde. **D-22 sigue abierta.**

Sustituto de esta pasada: cuatro brazos adversarios **disjuntos**, cada uno con una FRASE CONCRETA
que demoler y con la prohibición explícita y por nombre de mutar el árbol
(`checkout`/`restore`/`stash`/`reset`/escrituras):

| Brazo | Frase a demoler | Resultado |
|---|---|---|
| **Radio de impacto** | «el diff no deja ningún camino sin ejercer ni ningún contrato roto en silencio» | refutada en el matiz: 3 contratos rotos (D-27, D-28, D-29) |
| **Objetivos contra código** | «los tres objetivos están cumplidos y la meta se sostiene» | objetivos PASS, **meta FAIL** → H-1 |
| **Seguridad** | «no hay inyección, ni fuga de secretos, ni datos externos tratados como confiables» | **sostenida**. Sin hallazgos altos. Uno bajo (D-32) |
| **Documentos contra evidencia** | «toda afirmación factual de los documentos es cierta hoy» | **refutada** → §6 |

Los brazos midieron cosas disjuntas y lo demuestra el reparto: el de seguridad no encontró nada
y el de objetivos encontró el hallazgo que para la fase. Un solo brazo habría cerrado esto.

---

## 6. Lo que la auditoría de documentos encontró (y cómo se corrige)

- **Las citas de número de línea de `index.html` están masivamente desfasadas** en `DEUDAS.md`,
  `ROADMAP.md` y `01-TRANSICION.md`: el fichero creció ~180 líneas entre las revisiones que las
  midieron y HEAD. Las cifras derivadas de INSTRUMENTOS (tamaños de función, controles de
  sabotaje, hash de árbol) están todas **correctas**; lo que se pudre son las que se copian a mano.
- **Corrección aplicada:** no se actualizan una a una — mañana volverían a estar mal, que es
  exactamente la trampa de `CLAUDE.md` §9. Se **cierra la clase**: la cabecera de `DEUDAS.md`
  declara que los números de línea son de la revisión en que se midió y que para localizar el
  código se usa el NOMBRE, no la línea.
- **`01-TRANSICION.md` §2 decía «4 catches vacíos» y eran 6**, incluso en su propia revisión.
  Corregido aquí en §4 (H-6), no reescribiendo el acta anterior: un acta se escribe una vez.
- **`ROADMAP.md`** decía «2/3 ciclos» con los tres marcados cerrados, y «Last updated: 2026-08-29»
  narrando hechos del 30. Corregido.
- **`DEUDAS.md`** decía «última medición: `abe5e80`» teniendo fichas medidas sobre `96c7a3e`.
  Corregido.

---

## 7. Hallazgos que NO bloquean → al libro de deudas

Suben a `.paul/DEUDAS.md` en el MISMO commit que este acta (`CLAUDE.md` §8):

| Ficha | Qué es |
|---|---|
| **D-27** | `persistOps` pinta «Guardado ✓» verde antes de saber si el libro entró; el rojo llega 600 ms después |
| **D-28** | `migrateOpsToGlobal` ignora el booleano nuevo de `saveOpsAll` y devuelve `migrated: true` aunque la escritura falle |
| **D-29** | La invariante «si el guardado local falló, no se sube» vive sólo en `guardarTodo`; seis llamantes de `saveMeta` la esquivan |
| **D-30** | `applySyncPayload` escribe META **sin `savedAt`**, así que `localSaved` queda en 0 y cualquier snapshot posterior vuelve a aplicarse |
| **D-31** | El `catch` de `onAuthStateChanged` pinta el indicador de sincronía en VERDE después de un error |
| **D-32** | Las claves `balance-ops-rescate-*` no tienen tope ni caducidad |

Y dos fichas se marcan como **objetivo del ciclo 01-04**, no como deuda diferida: **D-33** (H-1) y
**D-34** (H-6).

---

## 8. Lo que este acta NO afirma

- **No afirma que el aviso en rojo se pinte**: sigue siendo **D-18**, sin comprobar. Exige agotar
  el almacenamiento del navegador con 90 operaciones reales delante.
- **No afirma que la guarda de subida corra ANTES del `set()`**: sigue siendo **D-15**, comprobada
  por presencia y no por precedencia. Cerrarla pide un doble de Firestore que hoy no existe.
- **No afirma haber reproducido H-1 en vivo**: está leído en el código y trazado eslabón a eslabón,
  no ejecutado contra un Firestore real. El ciclo 01-04 debe llevarlo a una autoprueba.
- **No afirma que las dos ramas del sync sean simétricas**: esa frase queda REFUTADA por **D-24**.

---

## 9. Siguiente acción

`/paul:plan 01-04` — en contexto limpio. Objetivo del ciclo: **cerrar la CLASE «escritura a la
nube sin guarda», no los dos casos**. Derivar el conjunto de escrituras del código en vez de
enumerarlo a mano, y dejar un control que se ponga rojo si aparece una cuarta.
