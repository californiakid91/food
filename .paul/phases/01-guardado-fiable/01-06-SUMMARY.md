---
phase: 01-guardado-fiable
plan: 06
tipo: acta
fecha: 2026-08-31
---

# Acta del ciclo 01-06 — «El aviso que no miente»

> Un SUMMARY es un ACTA: se escribe una vez y se entierra. Las deudas vivas están en
> `.paul/DEUDAS.md`, no aquí.

## Qué se cerró

**D-38: la capa de aviso no tenía oráculo.** Hasta este ciclo, un guardado fallido **pintado en
verde** dejaba `tools/verify.sh` en `rc=0` con «VERDE — todo ejercido y en verde». Los pintores
(`showSaveIndicator` y `setSyncUI`) no los había **ejecutado jamás ningún test**: se les sustituía
por espías, así que se medía que los llamantes pasaban `ok=false`, nunca qué hacía la función con
ese `false`.

Ahora los pintores **se ejecutan de verdad** sobre un DOM observable con reloj falso, y se lee su
efecto: texto, color **por su valor**, visibilidad y duración. Se cerró además la familia que el
borrador del plan dejaba viva (el campo `aviso` del juez de subida) y se añadió un instrumento
nuevo, `tools/avisos.py`, cableado a la puerta.

## Lo que de verdad pasó en este ciclo

**El ciclo se dio por hecho una vez, y estaba mal.** La puerta salió verde, el banco de sabotaje
verde con 68 controles mordiendo, las dos variantes idénticas. Y entonces los **tres brazos
adversarios del diff lo demolieron**, cada uno viendo cosas que los otros dos no.

El peor hallazgo, re-verificado a mano sobre copia aislada:

> El aserto exigía que los colores de éxito y de fallo fueran **DISTINTOS**. Nunca **CUÁLES**.
> Intercambiarlos —el fallo de guardado pintado en **VERDE**— salía `rc=0` y «✅ Autopruebas OK».

Es literalmente el daño que nombra D-38, vivo dentro del ciclo escrito para matarlo. Mi oráculo
heredó mi punto ciego (§5.8), que es la reincidencia número uno del catálogo.

**Diez hallazgos en total, todos atendidos dentro del ciclo. Ninguno diferido.**

### Brazo del oráculo (falsos verdes) — 4

| # | Hallazgo | Antes | Arreglo |
|---|---|---|---|
| 1 | Colores **intercambiados**: fallo en verde | `rc=0` | se afirma el VALOR, oráculo escrito aparte |
| 2 | Error de sincronización pintado naranja | `rc=0` | cada estado afirma su color; estado nuevo ⇒ rojo con nombre |
| 3 | Aviso de fallo de **2 milisegundos** | `rc=0` | duración mínima legible exigida |
| 4 | El detector de cesión de control pasaba con el **mecanismo borrado** | `rc=0` | control positivo: se comprueba que reacciona |

El 4 es §5.1 con uniforme: el comentario lo llamaba «MECANISMO explícito» y el aserto era cierto
por defecto.

### Brazo del cableado — 2

- **La cabecera de `tools/avisos.py` afirmaba que el agujero «está fichado en `.paul/DEUDAS.md`».
  No lo estaba.** La trampa §5.1 escrita por mí, en el ciclo que va justamente de eso. Hoy existe:
  es la ficha **D-44**.
- **Nueve avisos reales** del guardado por sincronización, de la lectura de nube y del arranque
  escapaban al censo (`applySyncPayload` ×5, `pullFromFirestore`, `listenFirestore`,
  `repararLibroIlegible`, `migrateOpsToGlobal`). Sembrar un aviso nuevo en el guardado por
  sincronización daba `rc=0`.

### Brazo de correctness — 4 propios, que ninguno de los otros vio

- **El banco restauraba `verify.sh` creando un fichero nuevo.** El intérprete que lo estaba
  ejecutando conservaba un descriptor sobre el inodo viejo y seguía leyendo los bytes **mutados**
  el resto de la corrida; y `hash_arbol()`, que lee por RUTA, informaba del árbol como limpio.
  Ahora se restaura **en el mismo inodo**.
- **El banco suponía `.git/hooks`** para el enganche, que es exactamente la suposición que el
  ciclo 01-05 quitó de `install-hooks.sh` y de `hookcheck.py`. Con `core.hooksPath` puesto o en un
  `git worktree`, vigilaba un fichero que nadie instala. Ahora se lo pregunta a git (§5.16).
- Un `roto()` de `funcsize.py` **sin su REMEDIO**, contra la decisión del 01-05.
- Un comentario que decía «48 filas» cuando son 84, y la derivación de identificadores del marcado
  que colaba `data-id=` y se dejaba fuera `id='...'` con comilla simple.

## La decisión difícil del ciclo: el ámbito del censo

El ámbito de `tools/avisos.py` se intentó acotar **dos veces**, y las dos perdió avisos reales:

1. **Ocho raíces escritas a mano** → escapaban los nueve avisos de arriba. Cada agujero se tapaba
   añadiendo la novena raíz: la lista blanca que el instrumento existe para no necesitar (§5.15).
2. **Raíces derivadas con cierre transitivo** → se perdió **`guardarTodo`**, el guardado en
   persona, porque sólo se alcanza como ARGUMENTO (`setTimeout(guardarTodo, 600)`) y el cierre no
   seguía esa arista.

Un cierre transitivo sobre JavaScript tiene más formas de escaparse de las que uno puede enumerar.
**Se sustituyó por la regla honesta: se mide TODO el `<script>` y se exime por NOMBRE.** El único
corte es `runSelfTests`, con su motivo escrito (sus avisos son el veredicto de la propia suite y
ya tienen juez: el código de salida de la puerta). El instrumento MIDE; quien EXIME es el criterio.

**Desviación consciente del alcance del plan**, en la dirección segura y dicha por escrito: el
plan excluía «los avisos que no son de guardado ni de arranque». Con ámbito plano **sí entran**
(borrar carteras y operaciones, vaciar activos, el texto de una captura). No se excluyen: se
sellan con su motivo, uno a uno. Recortar el ámbito para que cuadre con el plan habría sido
meterle juicio al instrumento, y un instrumento con juicio dentro se dobla.

Segunda corrección de diseño, también por medición: **un aviso que DESAPARECE es un HALLAZGO, no
una mejora.** Degradar un `console.error` del arranque a `console.log` salía rotulado «ha
desaparecido» **con el comando de resellado debajo**: el instrumento dirigía la mano del operador
a amnistiar el silencio (§4.4). Aquí la dirección buena no es «menos»: una boca que se cierra es
exactamente el silencio que esta fase existe para impedir. Por eso este instrumento **no compara
por dominación**, al revés que `funcsize` y `emptycatch`.

## Criterios de aceptación

Todos re-medidos en esta sesión sobre el árbol limpio, no heredados de la ejecución.

| AC | Resultado | Evidencia |
|---|---|---|
| **AC-0** el arnés no secuestra el navegador | **PASS** | quitado el `finally` y sembrado un lanzamiento ⇒ `rc=1`, «AC-0 y aun así restauró getElementById». Tras restaurar se comprueba que un `setTimeout` nuevo **sí se ejecuta** |
| **AC-1** el pintor del guardado se ejecuta; color y visibilidad | **PASS** | colores intercambiados ⇒ `rc=1` «AC-1 el fallo se pinta con el color de PELIGRO»; opacidad a 0 ⇒ `rc=1` «AC-1 el aviso de fallo queda VISIBLE» |
| **AC-2** duración del `setTimeout` real, ids únicos | **PASS** | duración única ⇒ `rc=1`; 1 y 2 ms ⇒ `rc=1` «dura lo bastante para leerse»; sin `clearTimeout` y cancelando **otra** variable ⇒ `rc=1` por el id EXACTO |
| **AC-3** ningún fallo de sync en verde ni invisible | **PASS** | rama de error en verde ⇒ `rc=1`; en naranja ⇒ `rc=1` «el estado error pinta SU color» |
| **AC-4** el juez no etiqueta un rechazo como «todo bien» | **PASS** | `aviso: 'ok'` en la rama de vaciado ⇒ `rc=1`. **Antes de este ciclo: `rc=0` y «✅ Autopruebas OK»** |
| **AC-5** avisos de consola por prefijo literal y nivel | **PASS** | los tres espías por subcadena sustituidos por prefijo literal completo + nivel aparte; degradar el aviso del cerrojo ⇒ `rc=1` en dos asertos |
| **AC-6** el derivador descubre y falla CERRADO | **PASS** | cero ids ⇒ `rc=2` «no derive ningun id»; **conjunto incompleto** ⇒ `rc=2` nombrando `save-indicator` |
| **AC-7** la clase cerrada por RECEPTOR | **PASS** | intruso en `schedSave` ⇒ `rc=1` con nombre; `--check` no escribe (hash); foto corrupta ⇒ `rc=2` con remedio; cambiar el corte ⇒ `rc=3` sin comando de resellado |
| **AC-8** todo control nuevo se ha visto ROJO | **PASS** | banco `rc=0`, vacuidad verde, árbol idéntico antes y después |
| **AC-9** ni una clave de datos reales tocada | **PASS** | el control de datos reales vive en el arnés, fuera de la suite, y sigue verde |

**Desviación anotada del AC-7:** el enunciado pedía derivar el ámbito del código alcanzable desde
guardado, subida y arranque. Se derivó dos veces y las dos perdió avisos reales, así que el ámbito
es TODO el `<script>` menos un corte nombrado. Es **más** de lo que pedía el AC, no menos.

**Desviación anotada del AC-5:** el plan pedía «un espía por aviso del censo». Se hizo así donde
había espía (los tres, corregidos a prefijo literal + nivel), y para los 34 avisos del censo el
oráculo es la foto sellada, que muere ante un cambio de mensaje **o de nivel**. Provocar en
tiempo de ejecución los 34 exigiría, entre otras cosas, fallos de ventana emergente que no se
pueden inyectar sin cambiar el producto. Está dicho en vez de callado.

## Verificación

Árbol en exclusiva. `HEAD^{tree}` = `36d1bbd41a657cfcde4ecbcc788c7b6eaef60f87`, **idéntico antes
y después** de todas las mediciones que se comunican aquí.

- `bash tools/verify.sh` → **rc=0**, «VERDE — todo ejercido y en verde», **diez pasos**, con el
  nuevo «capa de aviso (censo y receptores)» listado
- variante automática (enganche `pre-push`) con `VERIFY_INNER=1` **exportado** → **rc=0**, y la
  salida es **idéntica** a la manual salvo el rótulo propio del enganche (comprobado con `diff`).
  Es decir: el enganche limpia la variable y ejerce los diez pasos, banco incluido
- `python3 tools/sabotage.py` → **rc=0**, «Todos los controles de la puerta muerden»,
  **74 controles muerden** (eran 52 al empezar el ciclo) **+ 10 guardas** = 84, control de
  vacuidad verde, árbol idéntico antes y después (`258609686981`)
- `python3 tools/avisos.py --check` → **rc=0**, 34 avisos en 34 claves, y los cuatro elementos de
  aviso (`auth-btn`, `save-indicator`, `sync-dot`, `sync-status`) sólo los tocan los pintores

**22 controles nuevos** respecto al estado inicial del ciclo, y **seis de ellos nacieron de los
hallazgos de los brazos adversarios**, no del plan.

## Lo que este ciclo NO hizo

- **No cierra la FASE 1.** Cerrar un ciclo nunca autoriza cerrar una fase (§7).
- **No cierra D-18** (ver el rojo del guardado local fallido agotando el almacenamiento).
- **No cierra D-42 ni D-43.**
- **No toca el truncamiento por sync** (D-01): es Fase 3.
- **No re-mide D-15 ni D-03**, marcadas A RE-MEDIR: es trabajo de la transición.

## Punto ciego que este ciclo CONSERVA

**La fidelidad del simulador (§5.3).** El arnés reproduce el contrato de identificadores y la forma
de las escrituras; **no** resuelve `var(--green)` a un color real, no aplica CSS, no tiene
disposición ni service worker. Un pintor puede quedar verde fuera del navegador y no verse en
pantalla. Por eso el ciclo **no cierra sin la verificación en el navegador** (§7 bis).
