# 01-01 — Arranque y guardado honestos · ACTA

**Fase:** 1 (Guardado que no miente) · **Plan:** 01-01 · **Cerrado:** 2026-08-29
**Commits:** `dd13e42` (ejecución) y `86ad865` (hallazgos de la revisión del diff)

---

## Qué se construyó

- El libro de operaciones se carga al principio de `initPortfolios()`, antes de mirar la lista de
  carteras. Antes vivía dentro del `if` que la validaba, así que un META corrupto arrancaba con el
  libro vacío y el primer `schedSave()` lo escribía encima del bueno.
- `parseOpsBlob` distingue «no hay nada» (`[]`) de «no se entiende» (`null`). Un libro ilegible se
  copia a `balance-ops-rescate-<marca>` —una copia por contenido, no una por arranque— y
  `saveOpsAll` se niega a escribir encima mientras dure.
- Las tres funciones de guardado devuelven si lo consiguieron y registran el fallo. El anuncio lo
  decide `guardarTodo()`, extraída del temporizador para que sea verificable.
- `saveRows(anunciar)` permite que quien la llama decida el aviso; los dos llamantes que cantaban
  éxito 600 ms antes de guardar (`applyPosition`, `confirmTarget`) pasan su mensaje a `schedSave`.
- Un libro válido que llega de la nube repara el estado ilegible: el original ya está rescatado, así
  que negarse a escribirlo sólo añadía pérdida y dejaba un cerrojo sin llave.
- Si el guardado local falla, **no se sincroniza**: subir memoria que no se pudo persistir
  machacaría la copia buena de la nube.

## Reconciliación de los criterios de aceptación

Verificado ejecutando `tools/verify.sh` (rc=0) y `python3 tools/run_selftests.py` (rc=0), no por
lectura. 31 comprobaciones en total, 22 de ellas atadas a un criterio:

| AC | Veredicto | Evidencia |
|---|---|---|
| AC-1 · el libro sobrevive a un META corrupto | **PASS** | `AC-1 el libro sobrevive a un META corrupto`, `AC-1 el guardado no vacía el libro` |
| AC-2 · un guardado fallido se ve | **PASS** | 11 comprobaciones `AC-2 …`, incluido el camino de éxito parcial y que no se sube nada a la nube tras un fallo |
| AC-3 · un libro ilegible no se sustituye por uno vacío | **PASS** | 5 comprobaciones `AC-3 …`, incluidas la existencia y el contenido de la copia de rescate |
| AC-4 · las autopruebas no destruyen los datos del usuario | **PASS** | 4 comprobaciones `AC-4 …`, con centinelas sembrados antes de la foto |

**La parte visual de AC-2 sigue sin verificar por máquina**, tal como el plan declaraba: que el
aviso se vea en rojo en pantalla exige abrir la app. Ver «pendiente» abajo.

## Control positivo

Cada arreglo fue revertido y se comprobó que **su prueba muere**. Un intento dijo al principio
«pasa igual sin el arreglo»: era falso, el sabotaje no llegó a aplicarse porque su ancla aparecía
dos veces. Se repitió demostrando primero que la mutación había entrado. Los controles quedaron
permanentes: el banco pasó de 9 a **16**, y todos muerden.

## Revisión del diff — tres brazos disjuntos

Se atacó el commit `dd13e42`, que ya estaba verde. Los tres encontraron defectos reales.

**Corrección — 4 hallazgos, todos arreglados en `86ad865`:**
1. Con el libro ilegible, `schedSave` empujaba `opsAll: []` a Firestore y destruía la copia buena de
   la nube. El más grave: de ahí sale la declaración.
2. Un pull con libro bueno se descartaba en silencio y `opsIlegible` era un cerrojo irrecuperable.
3. Las copias de rescate se duplicaban en cada arranque, sin cota.
4. El temporizador de un «Guardado ✓» apagaba a los 1,8 s el aviso de error que lo sustituía.

**Falsos verdes — 3 hallazgos, todos arreglados:**
1. La agregación del guardado vivía dentro de un `setTimeout` que ninguna prueba ejecutaba: el
   revisor revirtió esa mitad del commit y la puerta siguió **verde**. Al extraer `guardarTodo()` y
   escribir su prueba, ésta falló de inmediato y destapó que `saveRows` anunciaba éxito antes de
   saber si el libro se había guardado — la garantía que afirmaba el comentario era falsa.
2. AC-4 era vacuo: en node el almacenamiento arranca vacío, así que comparaba cero con cero. El
   revisor borró la restauración entera y las pruebas siguieron pasando.
3. `throw /}/;` —JavaScript válido— hacía que el trinquete midiera una función de 85 líneas como si
   tuviera 2, **en silencio y sin rc=2**, contradiciendo su propio docstring.

**Documentos contra evidencia — 1 hallazgo real:** se publicó «146 funciones» y este mismo ciclo la
invalidó. Corregido, y la cifra se ha retirado de los documentos: ahora vive sólo en la foto
sellada, que se actualiza con el instrumento.

## Desviaciones respecto al plan

- **`guardarTodo()` y `saveRows(anunciar)` no estaban en el plan.** Surgieron porque la garantía de
  la Task 2 no era verificable dentro de un temporizador, y al hacerla verificable resultó ser
  falsa. El plan advertía que ese punto podía obligar a tocar el orden del guardado; se avisó
  entonces y así ha sido.
- **Se tocó el camino de sincronización**, que el plan excluía. Justificación: los hallazgos 1 y 2
  de corrección los introducía o volvía alcanzables este mismo cambio. Se limitó a dos guardas
  mínimas; la fusión de libros sigue siendo la Fase 3.
- **`tools/funcsize.py` creció bastante** (saltar cadenas, plantillas, comentarios y regex). No
  estaba planeado: una llave dentro de un texto entrecomillado en una prueba dejó ciego al
  instrumento, y sin eso no medía nada.

## Decisiones

- No sellar con amnistía cuando las autopruebas engordaron su función: se troceó. Aflojar la vara el
  día que se estrena habría convertido la amnistía en rutina.
- Retirar de los documentos toda cifra medida que un ciclo pueda invalidar, y remitir a la foto
  sellada. Se desactualizó dos veces el mismo día.

## Pendiente al cerrar

- **Verificación manual en la app desplegada**, recargando dos veces: que «Guardado ✓» siga
  apareciendo al guardar y que el aviso rojo se vea cuando falle. Es la única parte que la puerta no
  puede ejercer (`CLAUDE.md` §7 bis).
- **El plan 01-02 no está ejecutado.** El escenario de pérdida por sincronización sigue abierto
  salvo por las dos guardas de vaciado añadidas aquí.

Deudas nuevas o modificadas en `.paul/DEUDAS.md`: **D-14** (la distinción regex/división es
heurística). D-09 y D-10 revisadas.
