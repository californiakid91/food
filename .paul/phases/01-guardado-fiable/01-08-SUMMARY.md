# SUMMARY 01-08 — Que el camino de la nube no pueda pintar verde sobre un fallo

**Fase 1 · Guardado que no miente · ciclo 8** — 2026-09-06
Plan: `01-08-PLAN.md` · Medición previa: `01-08-MEDICION-PREVIA.md`

---

## 1. Qué se construyó, en una frase

Aplicar lo que llega de la nube pasa a ser **todo-o-nada**, y de ese único hecho de entrada/salida
—«el documento NO aterrizó entero»— cuelgan las tres cosas que faltaban: **el reloj no avanza**, **la
subida se frena**, y **la pantalla lo dice** con su causa y sus cifras.

El daño que cierra estaba medido: un libro de la nube que no cabía en el disco dejaba al
dispositivo creyéndose al día, y en el siguiente guardado **exportaba su libro pobre encima del
rico** —42 operaciones se quedaban en 2— con «Guardado ✓» y el punto en «Sincronizado». La pérdida
ocurría en la NUBE, que es de donde sale la declaración.

## 2. Reconciliación de los criterios de aceptación

Uno a uno **contra su artefacto**, no contra el color de la puerta: el propio plan avisaba de que
«cada control nuevo se ha visto rojo» no detecta un control que no se escribió.

| AC | Veredicto | Evidencia |
|---|---|---|
| **AC-1** el libro que no cabe no adelanta el reloj ni se exporta | **PASS** | `pruebasFrenoTodoONada`: `aplicado=false`, `savedAt` sigue en 1000, disco con 2 operaciones, memoria con «Vieja», freno con `ops=42` y persistido. Mutantes **M1, M2, M4b, M5, M6** (`rc=1`) |
| **AC-2** la aplicación es todo-o-nada, y el caso MIXTO cuenta | **PASS** | Quimera (todas las claves fallan): **no lanza**, devuelve `false`, memoria intacta en carteras / cartera activa / contador, disco coherente con su hora vieja. Caso mixto medido en `pruebasFrenoCasoMixto` y **definido por escrito** en **D-72**. Mutantes **T1×2** (`rc=1`) |
| **AC-3** se ve donde se produce | **PASS** | Arranque: `aviso='pendiente'`, motivo «la nube trae 42 operaciones y no caben en este dispositivo». Escucha: el pintor REAL escribe `#e67e22` y ese texto en los elementos. Mutantes **M3** y **M10** (`rc=1`) |
| **AC-4** el freno se levanta solo cuando deja de hacer falta | **PASS** | `pruebasFrenoSeLevanta`: cae **después** de confirmar la escritura, `savedAt` se sella en 9000 en ese momento, 42 operaciones en disco. Mutante **M5** (`rc=1`) |
| **AC-5** el freno no puede ser un callejón — las dos mitades | **PASS** | (a) `saveOpsAll` **sí escribe** con el freno puesto → mutante **M7**; (b) `saveMeta` funciona y **no adelanta** el reloj → **M9**, y **conserva** el freno → **M8**; (c) la subida devuelve `pendiente` con cero escrituras; (d) `decidirBajada` vuelve a decir «aplicar» sin que intervenga nadie |
| **AC-6** todo pintado del camino de nube tiene oráculo | **PASS** | `pruebasPinturaDeLaSubida` y `pruebasPinturaDeLaEscucha` **ejecutan** el pintor y afirman color Y texto por su valor, con vacuidad en las dos. **U8, U3, E7 y E2** mueren con mensaje nominal — E2 deja de cazarse «por accidente del banco». Y `setSyncUI` pasa a ser **receptor vigilado** (RED C de `avisos.py`): artefacto, no lista de casos |
| **AC-7** cambiar o crear cartera no canta victoria | **PASS** | `pruebasListaDeCarterasFallida`: los cinco **pintan en ROJO** —no «no pintan verde», que pasaría con y sin el arreglo— y deshacen su cambio; `deletePortfolio` no destruye los activos. `pruebasListaDeCarterasSana` es el control de vacuidad. Mutantes **D-48×2** (`rc=1`) |
| **AC-8** el censo de avisos no amnistía el silencio | **PASS** | `avisos.py --update` bloquea ahora en LAS DOS direcciones y **nombra** la clave. Control propio en el banco, que además restaura la foto sellada pase lo que pase |

## 3. Qué hace el arreglo, en lenguaje llano

- **Al bajar de la nube**: primero se escribe el libro —que es lo grande y lo que de verdad no
  cabe—, luego las filas y el historial, y **la lista de carteras con su hora la última**, y sólo si
  todo lo anterior entró. Si algo no entra, no se toca nada más y **la hora vieja se queda**.
- **El freno**: cuando algo no entra, queda apuntado que la nube trae más de lo que cabe. Con el
  freno puesto **no se exporta nada**, para que el libro pobre no se coma al rico.
- **Por qué el freno no atasca la app**: mientras está puesto, guardar en el móvil **sigue
  funcionando** —hay que poder borrar operaciones para hacer sitio— pero **no adelanta la hora**.
  Así la nube sigue pareciendo más nueva, la app lo vuelve a intentar sola, y el freno cae solo
  cuando el libro entero cabe. Ésta es la pieza que la primera versión del plan no tenía.
- **En pantalla**: el punto se pone naranja con la causa y las cifras, por los dos caminos por los
  que entra la nube, en vez de quedarse en verde.
- **Carteras**: cambiar, crear, renombrar o borrar una cartera avisa **en rojo** si la lista no se
  pudo guardar, y borrar ya no destruye los datos antes de saber si la lista se guardó.

## 4. Los sabotajes: qué se ha visto ROJO, con su rc

Los **19 controles nuevos** del banco, todos con ancla única afirmada antes de mutar y todos
revertidos. Transcritos de la salida, no recordados:

```
OK muerde: T1: las escrituras de la bajada vuelven a escapar sin captura (rc=1)
OK muerde: T1: la memoria se muta ANTES de saber si el documento aterriza (rc=1)
OK muerde: M1: la marca de tiempo vuelve a sellarse incondicionalmente (rc=1)
OK muerde: M2: aplicar vuelve a decir que si pasara lo que pasara (rc=1)
OK muerde: M3: el arranque vuelve a ignorar si se aplico (rc=1)
OK muerde: M4a: el freno sale del cableado de la subida (rc=1)
OK muerde: M4b: el freno sale del juez de la subida (rc=1)
OK muerde: M5: el freno se suelta ANTES de confirmar la escritura (rc=1)
OK muerde: M6: el freno se queda solo en memoria (rc=1)
OK muerde: M7: ANTI-CALLEJON, el freno bloquea tambien la escritura local (rc=1)
OK muerde: M8: guardar la lista de carteras borra el hecho del freno (rc=1)
OK muerde: M9: el guardado local vuelve a adelantar el reloj con el freno puesto (rc=1)
OK muerde: M10: la escucha en vivo ignora si se aplico (rc=1)
OK muerde: U8: una escritura a la nube que FALLA se pinta en verde (rc=1)
OK muerde: U3: una subida OMITIDA por el juez se pinta en verde (rc=1)
OK muerde: E7: el escucha de la nube MUERE y se pinta en verde (rc=1)
OK muerde: E2: el naranja de la escucha pierde su MOTIVO (rc=1)
OK muerde: D-48: el fallo de la lista de carteras vuelve a ser mudo (rc=1)
OK muerde: D-48: borrar cartera vuelve a destruir los activos ANTES de guardar (rc=1)
OK avisos --update se niega a sellar una boca que se cierra, y la nombra
```

A éstos se suman los **doce** que nacieron de la revisión adversaria (B2, el freno que gana al
reloj, las dos suertes de freno permanente, la relectura del disco, el aviso que culpaba al libro,
las filas escritas de más, el libro vacío, el historial, el contador, y los dos controles de la
amnistía y la vacuidad del censo).

**VACUIDAD:** el control de vacuidad del banco pasó en todas las corridas («sin sabotaje, la puerta
interior da rc=4»), así que estos rojos distinguen de verdad.

**LA PUERTA, LEÍDA:** `tools/verify.sh` completo → **`rc=0`**, once pasos, banco de sabotaje y
enganche `pre-push` incluidos, «VERDE — todo ejercido y en verde». El banco por su cuenta:
**161 controles, `rc=0`, «Todos los controles de la puerta muerden»**, con el árbol **idéntico
antes y después**.

## 4 bis. La revisión adversaria del diff: ONCE arreglos que no estaban

**Los tres brazos y la revisión del diff demolieron el ciclo ya escrito y con la
puerta en verde.** Ninguno vio lo mismo que otro. Todo lo que sigue se arregló
DENTRO del ciclo: pasar a UNIFY con un hallazgo de correctness sin atender lo
blanquea como «hecho» (§3.4).

**Lo que estaba MAL en el producto:**

| Hallazgo | Quién | Qué pasaba | Arreglo |
|---|---|---|---|
| **El freno se quedaba puesto PARA SIEMPRE en un dispositivo nuevo** | brazo A | Su reloj local nace por delante del de la nube, así que la rama «la nube es más nueva» no dispara jamás: en cuanto el operador tocaba algo, liberar espacio ya no servía y sólo lo destrababa OTRO dispositivo | El freno gana al reloj: con el freno puesto la bajada **reintenta**, sin mirar horas (`reintento-del-freno`) |
| **Freno permanente, segunda vía: el reloj local perdido** | revisión + brazo A | Con META corrupta, `marcaDeGuardado` sellaba un cero y el juez decía «reloj-desconocido» para siempre | El mismo arreglo: el reintento no depende del reloj |
| **Freno permanente, tercera vía: la nube se queda sin documento** | brazo A | El único levantador era aplicar con éxito; sin documento no hay nada que aplicar, y la pantalla seguía afirmando «la nube trae 42 operaciones» con la nube vacía | `soltarFreno()`: el freno cae en cuanto una bajada demuestra que **no hay nada pendiente que aterrizar** |
| **«Todo-o-nada» era falso: la memoria quedaba con el libro vacío** | brazo A | Con el libro local ilegible, la reparación levanta su cerrojo en cuanto SU escritura va bien; al fallar el resto, el disco quedaba con 42 operaciones y la memoria con 0 — y el siguiente guardado las escribía encima **en verde** | Al fallar, `applySyncPayload` **relee el disco**: memoria y disco vuelven a coincidir |
| **Claves huérfanas escritas aunque el libro no quepa** | brazo A | Las filas de las carteras de la nube se escribían igual, con identificadores que la lista local no referencia, consumiendo justo la cuota que falta | Si el libro no aterriza, **no se escribe nada más** |
| **El aviso culpaba SIEMPRE al libro** | revisión del diff | En el caso mixto la pantalla decía «la nube trae 42 operaciones y no caben» con el libro ya aterrizado: mandaba al operador a podar el libro por un problema que estaba en las filas. El mensaje es lo que dirige la mano (§4.4) | El motivo se compone de `faltan`, con una constante compartida para que los dos predicados sobre la misma clave sean **el mismo** (§5.16) |

**Lo que estaba MAL en el aparato de medición:**

| Hallazgo | Quién | Qué pasaba | Arreglo |
|---|---|---|---|
| **Cinco formas de pintar VERDE sobre un fallo pasaban la puerta ENTERA y el banco completo** | brazo C | La ventana de pintura sustituye el reloj por uno que **apunta y nunca dispara**, así que un `setTimeout(setSyncUI, 0, estadoSync('ok'))` no se ejecutaba dentro de la ventana: el oráculo medía el INSTANTE, no el estado final (§5.12) | La ventana conserva los argumentos del temporizador y las AC-6 **disparan los aplazados** antes de afirmar. Mutante propio (**B2**) |
| **Un fallo del producto que LANZA daba `rc=2`, no `rc=1`** | brazo B | El ciclo había cerrado esa clase para las filas y la dejó abierta para el libro y para los cinco llamantes de carteras: el mensaje mandaba a mirar la herramienta en vez del código | `sinLanzar` / `sinLanzarAsync` en los dos caminos de bajada y en el banco de carteras |
| **Las ramas «a propósito no se escribe nada» sólo existían en un comentario** | brazo B | Si cualquiera devolviera `false`, el freno se armaría con un libro que NUNCA puede aterrizar. Un comentario no cablea nada (§5.1) | Una fila por rama: libro vacío y cerrojo sin reparación posible |
| **El historial y el contador por cartera se quedaron sin red al trocear** | brazo B | Borrar la escritura del historial dejaba la puerta verde | Dos asertos nuevos, con sus mutantes |
| **`--update` seguía amnistiando el silencio: borrando la foto** | brazo C | Sellaba desde cero con la boca cerrada dentro, los motivos en blanco y todo verde. El REMEDIO que el propio instrumento imprime era su puerta de atrás | `--check` exige motivos de verdad, **el mismo predicado que `sumideros.py`** (§5.16). Control propio en el banco |
| **El control de vacuidad de la RED C era código muerto** | revisión del diff | El contador se incrementaba ANTES del filtro de la declaración, que casa siempre: el instrumento que existe para decir «no medí nada» no podía hablar (§5.4) | El contador va después del filtro, y hay un control que **quita todas las llamadas** y exige `rc=2` |
| **El banco ESCRIBÍA la foto sellada real** | revisión del diff | El control de D-61 corría `--update` sobre el árbol; si el proceso muriera a mitad, quedaría una foto sellada desde un fichero saboteado y la puerta verde | Ese control corre **sobre una copia**: no hay ventana |
| **`texto_esperado` era un prefijo desnudo** | brazo C | `"AC-1"` casa con 92 líneas: el oráculo no distinguía «murió lo que mido» de «murió todo» | Los 19 casos exigen ahora el **texto completo** de su aserto |

**Lo que los brazos SOSTUVIERON** (no todo se refutó): que una escritura fallida no puede
adelantar la marca de tiempo; que el freno impide exportar; que los rollbacks de los cinco
llamantes son correctos; que ninguna prueba nueva pasa por accidente ni deja el `localStorage` del
operador tocado; y que los 19 sabotajes mueren **por el oráculo que dicen medir**, no por accidente
ni por ancla rota.

**Nota de proceso, escrita en vez de callada:** la revisión del diff avisó de que el árbol **no
estaba en exclusiva** — apareció un fichero sin seguimiento mientras medía, porque yo estaba
escribiendo esta acta. `index.html` no cambió y sus mediciones se sostienen, pero la regla es la
regla (§5.13).

## 5. El banco cazó DOS defectos de mis propias pruebas

No teóricos: los dos convertían un **hallazgo real (`rc=1`) en «instrumento roto» (`rc=2`)**, que es
el mensaje que manda a mirar la herramienta en vez del código.

1. **M4a daba `rc=2`.** El aserto del cableado hacía `depsDeSubida().pendiente().ops` y el mutante
   devuelve `null`: el aserto **lanzaba** en vez de fallar, y se llevaba por delante el veredicto de
   las demás suites. Arreglado con `|| {}`; re-verificado sobre copia aislada: `rc=1`, «esperaba
   4242, obtuve undefined».
2. **T1 daba `rc=2`.** La prueba del caso mixto llamaba a aplicar **sin `try`**, así que el mutante
   que devuelve las escrituras sin captura hacía escapar la excepción. Arreglado; re-verificado
   sobre copia aislada: `rc=1`, con «AC-2 con la cuota llena del todo, aplicar NO lanza: esperaba
   false, obtuve true».

Las dos re-verificaciones se hicieron **sobre una COPIA**, con el directorio fijado en absoluto y
afirmado, y con la unicidad del ancla afirmada antes de mutar. Sobre el árbol real sólo se leyó.

## 6. Cambios de la REGLA DE MEDIDA, dichos en voz alta

Los dos son **aprietes**, y los dos obligaron a resellar a propósito. Quedan en el diff.

- **`avisos.py` v1 → v2.** Entra la **RED C** (`setSyncUI` como receptor vigilado: cada llamada
  viaja en la huella con su argumento normalizado) y la dirección «ambas» pasa a valer también en
  `--update`. El instrumento dio **`rc=3` (deriva)** y se **negó también a resellar**, que es lo
  correcto: hubo que escribir la nueva semántica en la foto a mano, conservando los 40 motivos ya
  escritos, y sellar con `--amnesty` **enumerando** cada clave. Motivos escritos uno a uno: cero
  claves con «SIN MOTIVO ESCRITO». Censo final: **59 avisos en 57 claves**.
- **`sumideros.py`**: tres sumideros nuevos sellados con amnistía y su motivo —uno de producto
  (`guardarListaDeCarteras` anuncia el fallo, que ES el arreglo) y dos de pruebas—. Total **37 en
  19 claves**.

## 7. Re-anclaje del banco (T10), re-derivado al terminar

- **126 anclas** sobre `index.html`, en **141 casos** del banco (eran 97 y 112 al empezar).
- **81 anclas** caen dentro de las funciones que este ciclo toca (el plan había derivado 44 con una
  lista más estrecha; la cifra se **re-deriva**, no se hereda).
- **8 anclas hubo que re-anclarlas** porque el ciclo movió su código: la precedencia de las dos
  guardas del cruce, el aviso sembrado en el guardado por sincronización, el reloj del sync puesto
  a cero, el repintado tras aplicar en la escucha, el sellado del reloj con la hora actual, el reloj
  falso del arnés de pintura, y los dos que apuntaban al retorno del aterrizaje fallido.
- **Cero casos cazados por ancla rota** en la corrida final.
- La colisión que el plan anticipaba (`if (saveMeta()) {` duplicado en cinco llamantes) **no llegó
  a producirse**: los cinco pasan por `guardarListaDeCarteras()`, precisamente para no duplicarla.

## 8. Desviaciones respecto al plan, con su motivo

- **`switchPortfolio` también deshace su cambio en memoria** si la lista no se guarda. El plan sólo
  pedía que no cantara victoria; dejar la cartera activa cambiada en memoria y vieja en disco es
  divergencia silenciosa, que es la otra mitad del daño de D-48. Regla uniforme para los cinco.
- **`armarFreno` no inventa una META que no existía**: si en disco no hay lista de carteras, no
  escribe (y lo dice). Escribir `{pendiente}` a secas habría dejado el disco con la lista vacía:
  daño nuevo por un camino de reparación.
- **Se troceó `pruebasPuertaDeSubida`** (cruces con nombre propio a `crucesDeLaPuertaDeSubida`)
  porque añadir la dimensión del freno la sacaba del presupuesto de 60 líneas. Sujeto del troceo
  explícito. La matriz pasa de **84 a 168 filas**.
- **Coste no declarado en el plan que sí apareció**: `applySyncPayload` no se «trocea» en dos, sino
  en seis piezas con nombre (`escribirClave`, `aterrizaElLibro`, `nextIdDelDocumento`,
  `metaDelDocumento`, `aterrizaDocumento`, `armarFreno`). El trinquete quedó **verde sin resellar**.

## 9. Deudas

Las cuatro que abría el ciclo quedan **CERRADAS** con su evidencia en `.paul/DEUDAS.md`: **D-58,
D-59, D-48 y D-61**.

Se abren las que el plan **firmó por adelantado**, más la que se midió al construir:

- **D-70** · con el freno puesto, ese dispositivo no tiene copia en la nube (familia de D-23 y
  D-35, pero **con criterio de muerte medible**, que es lo que a aquéllas les falta).
- **D-71** · lo que se teclee con el freno puesto se sustituirá cuando la nube aterrice (es fusión:
  Fase 3).
- **D-72** · el caso MIXTO deja el disco desparejado (libro nuevo, filas viejas) hasta el siguiente
  reintento. **Medido, no supuesto.** Su mitad peor —la memoria con el libro viejo mientras el disco
  tenía el nuevo, y el siguiente guardado escribiéndolo encima en verde— **la encontró un brazo
  adversario y se cerró dentro del ciclo**.
- **D-73** · cada aviso nuevo obliga a resellar el censo con amnistía.

## 10. Lo que este ciclo NO hace, y sigue sin hacer

D-60, D-65 y la clase general «subir sin haber firmado lo que hay arriba» (D-50) siguen abiertas y
fuera del alcance, como decía el plan. **No hay camino de remediación en pantalla** para liberar
espacio: es Fase 5.

**Y lo que la puerta no puede ver:** esto toca pantalla, así que el ciclo **no está verificado**
hasta abrir `https://californiakid91.github.io/food/` y mirarlo, recargando dos veces, y confirmar
antes que el navegador tiene el código nuevo por una función y no por el aspecto.
