# Libro de deudas — food

> **Lista VIVA, no un acta.** Se lee al arrancar cada sesión. Toda deuda diferida en un UNIFY sube
> aquí en el MISMO commit, con su origen citado. Si una deuda sólo existe en un SUMMARY, es como
> si no existiera. Norma completa en `CLAUDE.md` §8.
>
> Cada ficha dice: **qué es · cómo se midió · estado · qué la reabre.**

**Ciclo 01-07 (2026-09-01): la bajada de la nube y los sumideros del daño.** Cierra **D-45,
D-46, D-27, D-29 y D-30**; abre **D-48 a D-53**. **CINCO brazos adversarios disjuntos demolieron el
ciclo ya escrito y con la puerta en verde**, y ninguno vio lo mismo que otro: 13 mutantes que
rompen comportamiento real dejaban las seis piezas de la puerta en `rc=0`. El peor —y el que da
nombre a **D-49**— es estructural: **hacer inyectable una función crea POR CONSTRUCCIÓN un cableado
por defecto que corre en el navegador y que ninguna prueba toca**, porque todas inyectan el suyo;
cambiar `ops: () => ops` por `ops: () => []` reabría **D-45 entera en producción** con la puerta
verde. El segundo peor: el arreglo de D-45 **no habría protegido a nadie el día del despliegue**,
porque todos los dispositivos ya sincronizados tienen META sin marca de tiempo (D-30) y «lo
desconocido vale cero» hace ganar a cualquier documento — control en verde y daño vivo (§5.10).
Acta: `.paul/phases/01-guardado-fiable/01-07-SUMMARY.md`.

**QUINTA transición de fase (2026-09-05): la fase NO cierra, abre el ciclo 01-08.** Cinco brazos
adversarios disjuntos, **cada uno sobre su propia copia del proyecto**, y **los cinco demolieron su
frase**. Abre **D-58 a D-69**. Lo decisivo: un libro de la nube que **no cabe** en el almacenamiento
adelanta el reloj y el siguiente guardado lo **exporta encima** (42 operaciones → 2, en verde), y la
capa de aviso del camino de NUBE deja pintar **verde sobre un fallo de sincronización** con la
puerta entera en `rc=0`. Las cinco deudas que cerró el 01-07 se re-midieron revirtiendo su arreglo:
**las cinco están bien cerradas**. Acta:
`.paul/phases/01-guardado-fiable/01-TRANSICION-5.md`.

**CUARTA TRANSICIÓN de la Fase 1 (2026-09-01): la fase NO cierra, abre el ciclo 01-07.** Cuatro
brazos adversarios disjuntos; por primera vez uno —el del aparato de medición— **no demolió su
frase**, y por primera vez **ninguna cifra publicada era falsa**. Pero la META sigue sin cumplirse:
al arrancar, una nube más vieja empobrece el libro con la pantalla en verde (**D-45**), y quitar la
lista de carteras del veredicto de guardado deja la puerta en `rc=0` (**D-46**). Se cerró **D-15**
re-midiéndola en vez de heredarla. Acta: `.paul/phases/01-guardado-fiable/01-TRANSICION-4.md`.

Último ciclo cerrado: **01-06** (2026-08-31), la capa de aviso. **Cerró D-38** por la clase y
abrió **D-44**. Los TRES brazos adversarios del diff demolieron el ciclo ya escrito, cada uno
viendo algo que los otros dos no: diez hallazgos, el peor de ellos **un fallo de guardado pintado
en VERDE que salía `rc=0`** dentro del ciclo escrito para impedirlo.
Acta: `.paul/phases/01-guardado-fiable/01-06-SUMMARY.md`.

Ciclo anterior: **01-05** (2026-08-31), la vara de medir. Cerró **D-39, D-40 y D-41**,
abrió **D-42** (y **D-43** al cerrarlo) y re-midió **D-26** (186 sellado vs **190** derivadas: se ha vuelto a desfasar y la
puerta sigue verde). La revisión adversaria del diff destapó **dos falsos verdes del propio
arreglo** —un enganche sin bit de ejecución que git ignora dejando pasar el push, y suponer
`.git/hooks` con `core.hooksPath` puesto— y **un daño colateral**: cablear el vigilante del
enganche antes del banco dejaba sin correr el banco en cualquier máquina sin instalar.
Acta: `.paul/phases/01-guardado-fiable/01-05-SUMMARY.md`.

Última medición contra el código: **2026-08-31**, **TERCERA transición de la Fase 1**
(cuatro brazos adversarios disjuntos: caminos de pérdida, calidad del oráculo, cableado, y
documentos contra evidencia). Abrió **D-38, D-39, D-40 y D-41**, marcó **D-15 y D-03 a
re-medir**, y **NO cerró la fase**: acta `.paul/phases/01-guardado-fiable/01-TRANSICION-3.md`.
La revisión adversaria del PLAN 01-05 (2026-08-31) amplió **D-38** con un segundo pintor que
decide (`setSyncUI`) y con el reloj de la duración, y partió el trabajo en dos ciclos: **01-05**
(instrumental) y **01-06** (la capa de aviso entera).
Medición anterior: **2026-08-30**, ciclo **01-04** (cuatro brazos adversarios
disjuntos —correctness, falsos verdes, calidad del oráculo y cableado— sobre el diff del ciclo).
Cerró D-33, D-34 y D-31; abrió D-35, D-36 y D-37, y añadió `onScreenshotPicked` a D-09. Acta del
ciclo: `.paul/phases/01-guardado-fiable/01-04-SUMMARY.md`. La medición anterior (SEGUNDA
transición de la Fase 1) está en `.paul/phases/01-guardado-fiable/01-TRANSICION-2.md`.
D-12 y D-13 vienen de la revisión adversaria del plan 01-01, no de la auditoría inicial.

> ### ⚠️ Los números de línea de este libro son de la revisión en que se MIDIÓ, no de HEAD.
> `index.html` crece en cada ciclo y las citas de línea se desfasan al día siguiente: la auditoría
> de documentos del 2026-08-30 encontró que **casi todas** las de este fichero ya apuntaban mal.
> Se cierra la CLASE en vez del caso (`CLAUDE.md` §5.15): **para localizar el código se usa el
> NOMBRE de la función y `grep`, nunca el número de línea.** Las cifras derivadas de instrumentos
> (tamaños de función, controles de sabotaje, hashes) sí son fiables **cuando un script las
> vuelve a derivar**. Las copiadas a mano, no — y **`funciones_vistas` de `baseline-funcs.json`
> es una de las copiadas a mano**: dice 186 y hoy se derivan 190 sobre un `index.html` que no ha
> cambiado desde el sellado. Es munición de **D-26**, no una cifra fiable.

---

## Abiertas — riesgo de pérdida de datos

### D-58 · Un libro de la nube que NO CABE adelanta el reloj, y el siguiente guardado lo exporta encima
- **Qué es:** en `applySyncPayload`, si `saveOpsAll(entrante)` falla —almacenamiento lleno; el
  libro de la nube es más grande que el local— la función **lo cuenta sólo por `console.error` y
  sigue**: escribe META con el `savedAt` del documento, recarga el libro VIEJO del disco y devuelve
  `true`. El dispositivo queda **con el reloj de la nube y el libro pobre**, o sea creyéndose al
  día sin estarlo. En el primer guardado, `decidirSubida` no ve motivo para frenar (el libro local
  no está vacío) y **sube el libro pobre encima del rico**: la pérdida ocurre en la NUBE, que es de
  donde sale la declaración de la renta. Y el otro dispositivo, al arrancar, verá ese documento
  como más nuevo y adoptará el libro pobre.
- **Cómo se midió:** brazo A de la quinta transición (2026-09-05), reproducido ejecutando en copia
  aislada y **re-verificado por el orquestador**: nube con 42 operaciones y cuota simulada →
  `disco=["o1","o2"] META.savedAt=9000`, `guardarTodo=true save="Guardado ✓" var(--green)`,
  `subida={"subido":true} nube ahora tiene 2 ops (tenía 42)`, `dotTitle:"Sincronizado"`.
- **Estado:** **abierta y GRAVE. Abre el ciclo 01-08.** Es la meta literal de la Fase 1 viva: fallo
  de arranque que empobrece el libro con estado tranquilizador. La puerta entera sale `rc=0` sobre
  el código con el defecto; lo único vigilado es el TEXTO de la consola, no el mecanismo.
- **Qué la reabre:** se cierra cuando una escritura fallida durante la aplicación impida adelantar
  la marca de tiempo y se vea en pantalla, con oráculo que ejerza ese cruce.

### D-59 · La capa de aviso del camino de NUBE no tiene oráculo: ocho mutantes vivos
- **Qué es:** `subirALaNube` es la única función que escribe a la nube y **nada mide lo que
  PINTA**. Sobreviven a la puerta entera: pintar **verde** tras una escritura que falla (U8);
  pintar **verde** una subida omitida por el juez (U3); el aviso naranja sin su motivo en la subida
  y en la escucha (U2, E2 — es **D-56** medida, no heredada); la escucha de Firestore que **muere**
  pintada en verde (E7); el texto del estado de error diciendo «Sincronizado con tu cuenta.» con el
  punto rojo (T5); y un documento con `portfolios: []` declarado sincronizado sin aplicar nada
  (B5). Se suman los cuatro que la puerta sólo caza **por accidente del banco** («BANCO ROTO:
  ancla no única»), entre ellos perder `okRows` del veredicto de `guardarTodo`, que no tiene
  autoprueba propia. Causa común: las pruebas del camino de subida **cuentan escrituras, no
  pintadas**; el espía del pintor se montó para el arranque y la escucha, nunca para la subida.
- **Cómo se midió:** brazo B de la quinta transición (2026-09-05), 79 mutantes semánticos con
  ancla única afirmada; 67 mueren con mensaje nominal y 12 no. **Re-verificados por el orquestador
  U8 y U3 (`rc=0`, «VERDE — todo ejercido y en verde») y U9**, que el brazo daba por vivo y **no lo
  está** (`rc=1`, «AC-3 una escritura que lanza no acaba en verde: esperaba error, obtuve ok»): lo
  que sobrevive es PINTAR, no devolver. El control existente mira el valor devuelto; el operador
  mira la pantalla.
- **Estado:** **abierta y GRAVE. Abre el ciclo 01-08.** Un fallo pintado en verde ES, para el
  operador, el silencio que esta fase existe para impedir — la misma lectura que abrió el 01-06.
- **Qué la reabre:** se cierra por RECEPTOR, no enumerando los casos conocidos (§5.15): todo
  pintado del camino de nube afirmado por su color Y su texto, en todas las ramas de fallo.

### D-60 · El cable del guardado a la subida puede cortarse en VERDE
- **Qué es:** `schedulePush` puede dejar de llamar a `subirALaNube` sin que nada se ponga rojo: las
  pruebas **reasignan** `schedulePush` para contar llamadas, así que su cuerpo nunca se ejerce. Es
  §5.6 —cubrir el mecanismo no cubre su cable—, el mismo hallazgo que el cierre del 01-07 encontró
  para el pintor del motivo, aquí en el eslabón que sincroniza. Daño: la app deja de subir a la
  nube en silencio, con el punto verde tras cada guardado.
- **Cómo se midió:** brazo B de la quinta transición (2026-09-05), mutante T7: `rc=0`, «VERDE —
  todo ejercido y en verde». `tools/sumideros.py` tampoco lo ve: el sumidero que desaparece se
  atribuye a la flecha y por dominación pasa como «menos superficie de daño».
- **Estado:** abierta. Fuera del alcance del 01-08 salvo que el cierre de D-59 lo arrastre.
- **Qué la reabre:** nada la cierra sola. Se cierra cuando el cuerpo de `schedulePush` se ejerza de
  verdad, con reloj falso, en vez de reasignarse.

### D-48 · Cambiar o crear una cartera pinta «Guardado ✓» en VERDE con la escritura fallida
- **Qué es:** cinco llamantes ignoran el booleano de `saveMeta`: `createDefaultPortfolios`,
  `switchPortfolio`, `addPortfolio`, `deletePortfolio` y `renamePortfolio`. **Su ficha original
  decía que «ni suben ni anuncian», y eso es falso**: `switchPortfolio` y `addPortfolio` llaman
  antes a `saveRows()` con anuncio, así que **pintan «Guardado ✓» en VERDE** con la lista de
  carteras sin escribir. Es la categoría exacta de **D-27**, que el 01-07 cerró para el libro y
  quedó viva aquí. Ninguno de los cinco sube a la nube, así que el libro de operaciones no se
  pierde por este camino: el daño es **pantalla que miente**, no pérdida.
  **El peor sigue siendo `deletePortfolio`**: borra los activos ANTES de guardar la lista, así que
  si la escritura falla los activos ya no están y la cartera sigue listada, apuntando a datos que
  no existen. Medido: `rows-B` borrado del disco y META en disco todavía listando B.
- **Cómo se midió:** brazo E de la quinta transición (2026-09-05), reproducido ejecutando y
  **re-verificado por el orquestador**: con `saveMeta` lanzando, `switchPortfolio` →
  `pintado: [{"t":"Guardado ✓","ok":true}] | subidas: 0`, memoria B / disco A; `addPortfolio` →
  ídem. `renamePortfolio`, `deletePortfolio` y `createDefaultPortfolios` no pintan nada.
  **Sin oráculo**: quitar el `saveMeta()` de `switchPortfolio` deja la puerta en `rc=0`.
- **Estado:** abierta, **RECLASIFICADA de «cambio silencioso» a VERDE FALSO** el 2026-09-05.
  **Entra en el ciclo 01-08** por ser la misma clase que D-27 y D-46.
- **Qué la reabre:** se cierra cuando el anuncio de éxito de los cinco dependa del resultado de su
  escritura, y `deletePortfolio` además invierta el orden o repare si falla. Con oráculo propio:
  hoy no lo tiene ninguno.

### D-49 · El censo de sumideros y el de escrituras a la nube son ESTÁTICOS y por NOMBRE
- **Qué es:** `tools/sumideros.py` cuenta llamadas (`f(`, `f?.(`) y referencias por nombre. Una
  llamada indirecta —`const g = schedulePush; g();`, `schedulePush.call(null)`, o el nombre llegado
  por un parámetro— le es invisible. `tools/cloudwrites.py` tiene el gemelo: no ve el alias
  `const r = d.ref; r.update(...)`. Cerrar la clase exigiría análisis de flujo, que este proyecto
  no tiene.
- **Cómo se midió:** brazo del aparato de medición del 01-07 (2026-09-01), reproducido ejecutando:
  `schedulePush?.()` sembrado en `isMobile` daba `rc=0` antes del arreglo de este ciclo (ahora
  muerde, con caso propio en el banco); `schedulePush.call(null)` **daba** `rc=0`.
  **CORREGIDO el 2026-09-05 (quinta transición, brazo C, reproducido):** hoy `.call`, `.apply`,
  `window['schedulePush']` y la desestructuración `{ ref }` SÍ muerden (`rc=1`). La ceguera real es
  otra: **el nombre partido o calculado** (`window['schedule'+'Push']()`), un pintor por
  `document.querySelector` o con la id en una variable, `innerHTML +=` con el marcado del aviso, y
  una subida por REST (`fetch` a la API de Firestore) — todos pasan los tres censos con `rc=0`. El
  alias de la referencia (`const r = d.ref; r.update()`) sigue invisible, como decía la ficha.
- **Estado:** abierta como **ceguera declarada**, no como falso verde: está escrita en la cabecera
  de los dos instrumentos. Lo que este ciclo SÍ cerró es la llamada opcional y la referencia como
  valor, que no estaban declaradas y por las que se escapaba el sumidero real del arranque.
- **Qué la reabre:** que aparezca en el código una llamada indirecta a un sumidero, o un alias de
  la referencia de Firestore. Entonces el censo mide una ficción.

### D-50 · Tras desplegar el 01-07, un dispositivo ya sincronizado no acepta la nube hasta guardar una vez
> **RE-MEDIDA el 2026-09-05 (quinta transición, brazo E): la ficha está incompleta en «qué la
> cierra».** Decía que se cierra sola al guardar una vez. No: tras guardar, el mismo documento pasa
> a `nube-no-mas-nueva` y **gana lo local, que sube encima**. Sólo entra una nube escrita DESPUÉS.
> El texto que se pinta, en cambio, ya dice la verdad (D-54 cerrada).
- **Qué es:** el juez de bajada se niega a aplicar cuando **no hay marca de tiempo** en alguno de
  los dos lados y hay datos locales que proteger (rama `reloj-desconocido`). Es lo que impide que
  el arreglo de D-45 sea ficticio. Pero **todos los dispositivos ya sincronizados llegan al
  despliegue con META sin marca**, porque hasta este ciclo `applySyncPayload` la borraba (D-30):
  en su primer arranque quedan en NARANJA («cambios sin subir») y **no reciben datos de la nube
  hasta que el operador guarde algo en local una vez**, que es lo que vuelve a poner el reloj en
  hora. Los datos locales están intactos; lo que no llega es lo de fuera.
- **Cómo se midió:** brazo de correctness del 01-07 (2026-09-01), reproducido ejecutando sobre
  copia aislada: con META sin `savedAt`, un documento de la nube con `savedAt: 500` y un libro
  local de 2 operaciones, el veredicto es `reloj-desconocido` y el libro se conserva.
- **Estado:** abierta como **coste declarado**, no como defecto. Se prefiere quedarse quieto y
  naranja a perder libro en verde. El texto del naranja dice «este dispositivo no tiene operaciones
  y no se pisa el libro de la nube», que en este caso **no describe bien la causa**.
- **Qué la reabre:** nada; se cierra sola en cuanto el operador guarde algo. Lo que sí queda
  pendiente es el TEXTO del aviso, que miente sobre el motivo.
- **VISTA EN PRODUCCIÓN el 2026-09-05**, no en laboratorio: es lo PRIMERO que el operador se
  encontró al abrir la app desplegada, y preguntó si era normal. La parte de comportamiento es la
  prevista; la del texto se separa a **D-54**, que ya no es un apunte al pie de esta ficha.

### D-51 · El desempate es «gana el último reloj», y los relojes de dos dispositivos no coinciden
- **Qué es:** al conservar la marca del documento aplicado (D-30 cerrada), un dispositivo adopta el
  reloj del que escribió. Si ese reloj iba adelantado, una edición legítima posterior hecha en un
  dispositivo con el reloj en hora parece MÁS VIEJA y se rechaza. Antes del ciclo esto «funcionaba»
  sólo porque el bug de D-30 hacía que se aplicara todo.
- **Cómo se midió:** brazo de correctness del 01-07 (2026-09-01), ejecutado: local `savedAt=2000`
  (adoptado), documento posterior con `savedAt=1500` → `aplicar: false`.
- **Estado:** abierta. Es inherente a resolver por reloj de pared y **la meta declarada de la Fase
  3** es sustituirlo por fusión por `id` y marca por sección.
- **Qué la reabre:** nada; va con la Fase 3.

### D-47 · No hay volcado al cerrar la pestaña: una ventana de 600 ms sin guardar
- **Qué es:** apuntar una operación llama a `schedSave()`, que aplaza el guardado 600 ms. **No
  existe ningún manejador `beforeunload`, `pagehide` ni `visibilitychange` en todo `index.html`**
  (grep: cero resultados). Cerrar la pestaña dentro de esa ventana pierde la operación que el
  operador ya ha visto en pantalla.
- **Cómo se midió:** brazo de caminos de pérdida de la CUARTA transición (2026-09-01): tras
  `schedSave()`, memoria = 1 operación, disco = 0.
- **Estado:** abierta. **No abre ciclo por sí sola:** es pérdida sin fallo declarado —el guardado no
  llegó a intentarse, así que no hay nada que avisar— y su arreglo es independiente del resto.
- **Qué la reabre:** nada; se decide aparte. El arreglo natural es volcar en `pagehide`.

### D-35 · Un paquete incompleto bloquea TODAS las subidas y no hay salida en pantalla
- **Qué es:** desde el ciclo 01-04, si una sola clave del almacenamiento no se puede leer o
  parsear, `buildSyncPayload` marca el paquete como incompleto y **la subida se rechaza entera**,
  incluido el libro de operaciones. Mientras dure el fallo el dispositivo queda sin copia en la
  nube, y **no hay ninguna salida en la interfaz**: el operador ve el punto en rojo con «No se
  pudo sincronizar» y nada más. Es el gemelo exacto de **D-23**: mejor para el dato y peor para el
  operador. La primera versión del PLAN 01-04 afirmaba que el arreglo «no introduce un modo de
  fallo nuevo peor»; era falso, y lo destapó la revisión adversaria del plan.
- **Cómo se midió:** razonado sobre el código y ejercido en las autopruebas
  (`pruebasTuberiaDeSubida`: con el paquete incompleto no se escribe). **No reproducido con un
  almacenamiento corrupto real en el navegador.**
- **Estado:** ABIERTA y aceptada a sabiendas. Rechazar es lo correcto para el dato: `ref.set`
  reemplaza el documento entero, así que subir un paquete a medias borra de la nube lo que falte.
- **Qué la reabre:** nada la cierra sola. Se cierra cuando la pantalla diga QUÉ clave falló y
  ofrezca una salida sin abrir la consola. Es Fase 5 (interfaz) y arrastra a D-18 y a D-23: las
  tres son el mismo agujero —un bloqueo correcto que el operador no puede ni ver ni resolver—.

### D-36 · El veredicto de las autopruebas puede imprimirse antes que sus fallos
- **Qué es:** `runSelfTests` es asíncrona desde el 01-04. Si una suite quedara sin `await`, sus
  checks llegarían por microtarea **después** del mensaje de veredicto pero antes del código de
  salida: la consola imprimiría «✅ Autopruebas OK» y el proceso saldría con rc=1 **sin listar ni
  un fallo**, mandando a mirar a ciegas.
- **Cómo se midió:** brazo adversario de falsos verdes del ciclo 01-04 (2026-08-30), ejecutado en
  una copia del repo, 3 corridas de 3.
- **Estado:** ABIERTA, pero acotada. El `await` que falta lo caza ahora un control propio (una
  suite que no ejerce ni un solo check es una suite que no corrió) y su sabotaje. Lo que queda sin
  cerrar es la carrera del MENSAJE, no la del veredicto: el rc siempre es correcto.
- **Qué la reabre:** se cierra cuando el veredicto se calcule y se imprima después de haber
  drenado todas las promesas, o cuando `check` deje de poder ejecutarse tras el resumen.

### D-37 · Cambiar de cuenta de Google en el mismo navegador sube el libro de la cuenta anterior
- **Qué es:** los datos locales no están separados por usuario. Si se cierra sesión con la cuenta
  A y se entra con la B en el mismo navegador, el libro de A sigue en el almacenamiento local y el
  juez de subida lo aprueba —ninguno de los dos lados está vacío— y lo escribe en el documento
  de B.
- **Cómo se midió:** brazo adversario de correctness del ciclo 01-04 (2026-08-30), leyendo el
  código. **No reproducido.**
- **Estado:** ABIERTA, prioridad baja: la app es personal y de un solo usuario. Se ficha porque no
  estaba dicho en ningún sitio, y porque el juez de subida no puede protegerla — el problema es
  que las claves de almacenamiento no llevan el identificador de la cuenta.
- **Qué la reabre:** que se use la app con más de una cuenta, o que se comparta el dispositivo.

### D-39 · Los trinquetes revientan con `rc=1` y traceback en vez de fallar CERRADO
- **Qué es:** `cargar_baseline()` de `tools/funcsize.py` valida que la clave `excede` exista, pero
  no su TIPO. Con `"excede": null` (JSON válido y aceptado por su propio chequeo de forma),
  `--check` muere con `TypeError: 'NoneType' object is not iterable` y **rc=1**. La puerta lo
  rotula entonces «FALLO trinquete de tamaño de funciones → HALLAZGOS (rc=1)»: **un instrumento
  roto sale clasificado como código que ha engordado**, y manda a mirar el sitio equivocado.
  Mismo agujero de clase en `tools/emptycatch.py` (`tolerados` sin validar tipo, y `--update`
  leyendo `['motivos']` sin validarlo).
- **Cómo se midió:** TERCERA transición (2026-08-31), brazo de cableado; **re-verificado a mano**
  por el orquestador sobre copia aislada: rc obtenido **1**, rc debido **2**.
- **Estado:** **CERRADA** en el ciclo **01-05** (2026-08-31). `cargar_baseline()` de los dos
  instrumentos valida ahora **el TIPO de cada clave**, y `emptycatch` valida además `motivos`, que
  sólo lee `--update`: antes `--check` salía **VERDE** con una foto que `--update` no podía leer —
  la forma que validaba el chequeo no era la forma que el instrumento necesita (§5.16). Rojo
  literal reproducido antes y después:
  - antes: `TypeError: 'NoneType' object is not iterable` + **rc=1**, rotulado por la puerta como
    «el monolito ha engordado»
  - después: `rc=2 INSTRUMENTO ROTO: funcsize: la foto sellada baseline-funcs.json: la clave
    'excede' es NoneType, se esperaba un objeto` + **rc=2**
  Dos sabotajes permanentes en el banco (uno por instrumento). El `except` de la comparación es
  **estrecho a propósito**: comprobado que un hallazgo real sigue en **rc=1** (`EL MONOLITO HA
  ENGORDADO`, `CATCH VACIO EN EL CAMINO DE SUBIDA`), no tapado por el aviso.
- **Qué la reabre:** cualquier instrumento nuevo que lea una foto sellada sin validar sus tipos.

### D-40 · `VERIFY_INNER=1` deja la puerta en `rc=0` con el banco de sabotaje sin correr
- **Qué es:** con esa variable puesta, `verify.sh` imprime «OMITIDO banco de sabotaje» y «VERDE,
  PERO EL BANCO NO CORRIÓ», pero **sale con 0**. El enganche `pre-push` hereda el entorno y sólo
  bloquea con rc≠0: esa variable exportada en un perfil, un wrapper o un CI deja pasar todos los
  push con el banco apagado, indefinidamente. **El veredicto de una puerta es un exit code, no una
  línea de texto que alguien tiene que leer** (§4.1).
- **Cómo se midió:** TERCERA transición (2026-08-31); **re-verificado a mano**: `VERIFY_INNER=1
  bash tools/verify.sh` sobre copia aislada → `rc=0`.
- **Estado:** **CERRADA** en el ciclo **01-05** (2026-08-31), con **las DOS capas, no una**:
  1. La puerta corrida con `VERIFY_INNER=1` devuelve ahora **rc=4** («verde, pero el banco no
     corrió»), nunca 0. Un 4 es verde para **un solo consumidor**, `sabotage.py::puerta()`; para
     el operador y para el enganche es no-verde. La tabla de códigos está escrita en la cabecera
     de `verify.sh`.
  2. El enganche **limpia la variable** (`unset VERIFY_INNER`) antes de llamar a la puerta, así
     que un perfil contaminado no la hereda.
  Con una sola capa el agujero seguía abierto por el otro lado. **Medido con la variable
  exportada:** a mano `rc=4`; por el enganche, puerta COMPLETA con el banco corrido, `rc=0` con
  código sano y **`rc=1` PUSH BLOQUEADO** con una regresión real.
  Cambiar este contrato tenía un **consumidor vivo**: el control de vacuidad del banco exigía que
  esa corrida fuera verde. Se cambió el consumidor en el mismo commit, y hay **control positivo**:
  revertido el `exit 4`, la puerta interior vuelve a dar 0 y la vacuidad lo caza.
- **Qué la reabre:** cualquier interruptor nuevo que reduzca lo que se ejerce sin cambiar el rc.

### D-41 · Nada vigila que el enganche `pre-push` exista ni que esté al día
- **Qué es:** la variante automática de la puerta es el enganche que instala
  `tools/install-hooks.sh`. Hoy el instalado es byte a byte el del instalador, pero **ningún paso
  de la puerta lo comprueba**. En una máquina nueva la variante automática sencillamente no
  existe, y nada se pone rojo; si el instalador cambia, el instalado queda rancio en silencio. Es
  la definición del propio proyecto de instrumento no cableado (§4.1), y el escenario exacto que
  §4.2 manda vigilar: «verifica AMBAS variantes».
- **Cómo se midió:** TERCERA transición (2026-08-31), brazo de cableado: comparó el enganche
  instalado contra el heredoc del instalador (idénticos) y comprobó que ni `verify.sh` ni
  `sabotage.py` lo miran.
- **Estado:** **CERRADA** en el ciclo **01-05** (2026-08-31) con `tools/hookcheck.py`, cableado
  como paso de la puerta. Distingue **seis desenlaces**, cada uno con su sabotaje sobre copias:
  **AUSENTE** · **NO EJECUTABLE** · **DISTINTO** · **FORMA** (el instalador cambió de forma, rc=2)
  · **ILEGIBLE** (rc=2) · y el positivo de que el enganche siga limpiando `VERIFY_INNER`. Más un
  **control de vacuidad**: sobre una copia sana, verde.
  El contenido esperado se **deriva del instalador** (se extrae su heredoc), no de una copia
  pegada en el comprobador: dos copias se desincronizan a la primera.
  **La revisión adversaria del diff destapó dos falsos verdes de este mismo arreglo**, los dos
  reproducidos a mano en un repo de usar y tirar antes de creérselos:
  - un enganche **sin bit de ejecución** hace que git lo **ignore** (avisa con un `hint:`
    silenciable) y **el push sale con rc=0** — la variante automática muerta con el fichero ahí;
  - suponer `.git/hooks` es falso con `core.hooksPath` puesto o en un `git worktree`: el enganche
    se ignora entero. Ahora la ruta **se le pregunta a git** (`git rev-parse --git-path hooks`),
    en el comprobador **y** en el instalador.
- **Nota de diseño:** el paso va **después del banco y fuera de la corrida interior**, a propósito.
  Mide la MÁQUINA, no el código. Cableado antes, un clon recién hecho o un CI ponía la puerta en
  rojo por el enganche y **el banco no llegaba a correr**: en esa máquina nada demostraba que
  ninguno de los otros controles muerde. Lo destapó la revisión del diff.
- **Qué la reabre:** que aparezca otro enganche de git sin su fila en `hookcheck.py` (la lista de
  enganches es enumerada, no derivada), o que el instalador cambie de forma sin reinstalar.

### D-42 · `comparar_o_roto` es una red SIN ORÁCULO: pasa con y sin ella
- **Qué es:** el envoltorio que hace fallar cerrado la comparación de los dos trinquetes es hoy
  **inalcanzable por construcción**. `cargar_baseline()` ya valida los tipos de todo lo que le
  llega, así que `comparar` no puede lanzar ninguna de las excepciones que captura. Los dos
  sabotajes de la foto malformada **miden la validación, no el envoltorio**: dan el mismo rc y el
  mismo mensaje con él y sin él. Es §5.9 en pequeño, y está **escrito en su propio docstring** en
  vez de contarse como control medido.
- **Cómo se midió:** revisión adversaria del diff del ciclo 01-05 (2026-08-31), hallazgo #3,
  reproducido revirtiendo las dos llamadas a `comparar(...)` a pelo: mensaje y rc **idénticos**.
- **Estado:** ABIERTA, y **deliberadamente no se arregla ahora**. Quitarlo devolvería el rc=1 con
  traceback en cuanto alguien añada una clave sin validarla, que es justo D-39. Se queda como red
  declarada.
- **Qué la reabre:** que se añada a una foto sellada una clave que `cargar_baseline` no valide;
  entonces el envoltorio pasa a ser alcanzable y hay que darle sabotaje propio.

### D-43 · Un mutador del banco sustituye texto SIN afirmar que su ancla sea única
- **Qué es:** de los seis mutadores del bloque de `hookcheck` en `tools/sabotage.py`, cinco no
  necesitan ancla (borran el fichero, le quitan el bit de ejecución, le añaden una línea, le
  cambian los permisos) y `sin_unset` **sí** afirma la unicidad de la suya. El sexto,
  `sin_heredoc`, sustituye `<<'HOOK'` **sin afirmar que aparezca exactamente una vez**. La doctrina
  lo exige explícitamente (§4.5.5 y §5.4): el sabotaje afirma la unicidad de su ancla **antes** de
  mutar, porque un meta-instrumento falla inventando agujeros, no ignorándolos.
- **Cómo se midió:** UNIFY del ciclo 01-05 (2026-08-31), leyendo los seis mutadores uno a uno
  contra el texto del AC-7 del propio plan, que dice «cada caso afirma la UNICIDAD DE SU ANCLA
  antes de mutar».
- **Estado:** ABIERTA, y **no es un falso verde**: si el ancla dejara de casar, la copia quedaría
  intacta, `hookcheck` daría rc=0 en vez del rc=2 esperado y el caso gritaría **NO MUERDE**. O sea
  que falla **ruidosamente**, que es la propiedad que importa. Es una desviación **nominal** del
  AC-7, escrita en vez de callada, no un agujero medido.
- **Qué la reabre:** que `install-hooks.sh` pase a contener más de un heredoc, momento en el que el
  mutador mutaría los dos y el caso dejaría de medir lo que dice medir. Se cierra con dos líneas:
  la misma afirmación que ya tiene `sin_unset`.

### D-44 · El censo de avisos es ESTÁTICO y su ámbito se exime a mano
- **Qué es:** `tools/avisos.py` mide leyendo el texto de `index.html`, no ejecutándolo. De ahí
  salen tres cegueras, escritas también en la cabecera del propio instrumento:
  1. **Presencia no es precedencia (§5.11).** Un literal escrito dentro de una CADENA cuenta como
     cobertura. Los comentarios sí se borran antes de medir, así que un comentario no cuela.
  2. **La red por RECEPTOR sólo ve `getElementById` con un literal.** Un `getElementById(variable)`
     que acabara resolviendo a un elemento de aviso le es invisible. No se cierra por lista blanca
     de variables porque el fichero tiene decenas de identificadores compuestos legítimos
     (`'bar-' + id`), y una lista blanca sólo protege de lo que ya conoce.
  3. **El ámbito exime `runSelfTests` a mano.** Es el único CORTE, nombrado con su motivo (sus
     avisos son el veredicto de la propia suite, y ya tienen juez: el código de salida de la
     puerta). Quitarlo o cambiarlo es DERIVA (rc=3).
- **Cómo se midió:** revisión adversaria del diff del 01-06 (2026-08-31), **dos brazos disjuntos
  llegaron al mismo sitio por caminos distintos**, y el hallazgo se re-verificó a mano sobre copia
  aislada. El ámbito se intentó acotar **dos veces** y las dos perdió avisos reales:
  - con **ocho raíces escritas a mano**, escapaban **nueve avisos** del camino de la fase
    (`applySyncPayload` ×5, `pullFromFirestore`, `listenFirestore`, `repararLibroIlegible`,
    `migrateOpsToGlobal`): sembrar un aviso nuevo en el guardado por sincronización daba `rc=0`;
  - con **raíces derivadas y cierre transitivo**, se perdió **`guardarTodo`** —el guardado en
    persona— porque sólo se alcanza como ARGUMENTO (`setTimeout(guardarTodo, 600)`).
  Un cierre transitivo sobre JavaScript tiene más formas de escaparse de las que uno puede
  enumerar. **Por eso hoy se mide TODO el `<script>` y se exime por nombre**: el instrumento MIDE,
  y quien EXIME es el criterio.
- **Consecuencia aceptada:** el censo incluye avisos que NO son de guardado ni de arranque (borrar
  carteras y operaciones, vaciar activos, el texto reconocido de una captura). No se excluyen: se
  sellan con su motivo. Es más ancho que el alcance declarado del ciclo 01-06, **en la dirección
  segura**, y se dice por escrito en vez de recortarlo.
- **Estado:** ABIERTA como ceguera declarada. **No es un falso verde**: es un límite del método,
  escrito en la cabecera del instrumento y aquí, no un agujero que se descubra mañana.
- **Qué la reabre:** que aparezca en `index.html` un `getElementById` con identificador calculado
  que resuelva a un elemento de aviso; que un aviso se emita por un canal que no sea
  `console.error`, `console.warn`, `alert` ni `confirm`; o que haga falta un segundo CORTE — el
  segundo corte es la señal de que el criterio está empezando a doblarse.

### D-61 · El censo de avisos AMNISTÍA en silencio una alarma que desaparece
- **Qué es:** `tools/avisos.py --check` caza que una boca se cierre (`rc=1`, «han DESAPARECIDO
  avisos») y hasta imprime «No se resella de trámite». Pero **`--update`, SIN `--amnesty`, la sella
  igualmente, en silencio, sin nombrarla y con `rc=0`** — y a partir de ahí queda verde para
  siempre. La causa es una asimetría (§5.16): `comparar()` clasifica la desaparición como `mejor`,
  `--check` la trata como hallazgo y `sellar` sólo se niega ante `peor`. El ciclo 01-06 decidió por
  escrito que «un aviso que DESAPARECE es un HALLAZGO, no una mejora» y lo cerró **sólo por el lado
  de `--check`**. `tools/sumideros.py` NO tiene el defecto: allí la boca cerrada va a `peor`.
- **Cómo se midió:** brazo C de la quinta transición (2026-09-05) y **re-verificado por el
  orquestador** con ancla única afirmada, cerrando `console.error('No se sincroniza: el guardado
  local falló.')`: `--check` → `rc=1` nombrando la clave; `--update` → `rc=0` «Foto sellada: 39
  aviso(s)»; `--check` después → `rc=0` verde.
- **Estado:** abierta y grave: es un hueco del aparato de medición que **dirige la mano del
  operador a amnistiar el silencio**. **Entra en el ciclo 01-08.**
- **Qué la reabre:** se cierra cuando `avisos.py` trate la desaparición como empeoramiento, igual
  que `sumideros.py`, con sabotaje propio que lo demuestre.

### D-62 · Un `index.html` que no decodifica sale como `rc=1` «hallazgo del código», no `rc=2`
- **Qué es:** los **siete** instrumentos Python que leen `index.html` (`check_syntax`,
  `run_selftests`, `funcsize`, `cloudwrites`, `emptycatch`, `avisos`, `sumideros`) mueren con
  `UnicodeDecodeError` sin capturar: traceback y **`rc=1`**. Es §4.3 literal: instrumento roto
  disfrazado de hallazgo, que manda a mirar el código en vez de las herramientas. Las fotos
  selladas sí fallan cerrado ante el mismo byte (`rc=2` con nombre).
- **Cómo se midió:** brazo C de la quinta transición (2026-09-05), con `printf '\xff\xfe<html>'`.
  No re-verificado por el orquestador.
- **Estado:** abierta. Fuera del alcance del 01-08.
- **Qué la reabre:** se cierra cuando los siete lean dentro de un `try` y devuelvan `rc=2` con
  nombre, con sabotaje propio.

### D-63 · Reglas de medida que viven FUERA de la semántica sellada cambian sin deriva ni sabotaje
- **Qué es:** quitar `'delete'` de los mutadores de `cloudwrites.py`, o dejar que el patrón de
  `emptycatch.py` no vea un `catch {}` desnudo, deja pasar el daño correspondiente con **`rc=0`**:
  no hay foto que lo selle, no salta la deriva (`rc=3`) y el banco no siembra ese caso. La regla de
  medida es parte de la vara, y una vara que se puede acortar sin decirlo no es un trinquete.
- **Cómo se midió:** brazo C de la quinta transición (2026-09-05), sembrando `r.delete()` y
  `catch {}` tras mutar cada instrumento. No re-verificado por el orquestador.
- **Estado:** abierta. Fuera del alcance del 01-08.
- **Qué la reabre:** se cierra cuando esas listas entren en la semántica sellada, o cuando el banco
  siembre un caso por cada entrada.

### D-64 · `hookcheck` da verde a un enganche con CRLF que git no puede ejecutar
- **Qué es:** `hookcheck.py` compara con `read_text()`, que normaliza los saltos de línea. Un
  `pre-push` guardado con CRLF sale «idéntico» y `git push` falla con
  `/usr/bin/env: 'bash\r': No such file`. El push queda bloqueado —falla cerrado, que es lo
  bueno— pero **el instrumento certifica lo contrario de lo que ocurre**.
- **Cómo se midió:** brazo C de la quinta transición (2026-09-05). No re-verificado por el
  orquestador.
- **Estado:** abierta, menor. Fuera del alcance del 01-08.
- **Qué la reabre:** se cierra comparando bytes en vez de texto.

### D-65 · Carrera de arranque: si la sesión gana al evento `load`, una nube más vieja pisa el libro
- **Qué es:** `auth.onAuthStateChanged` se registra al evaluar el script, pero `initPortfolios`
  —que carga `ops` y las carteras— corre en el evento `load`. Si el callback de sesión llega
  primero, el juez de bajada ve el libro vacío, concluye `sin-datos-locales` y **aplica cualquier
  documento**, por viejo que sea. Es D-45 por una puerta que su arreglo no cubre.
- **Cómo se midió:** brazo A de la quinta transición (2026-09-05): el MECANISMO está reproducido
  ejecutando (invirtiendo el orden se pierde una operación; con el orden normal resiste). **El
  orden REAL en el navegador NO está medido**, y el reproductor se colgó al re-verificarlo.
- **Estado:** abierta, **pendiente de medir antes de decidir**. Fuera del alcance del 01-08 hasta
  que se sepa si la carrera ocurre de verdad.
- **Qué la reabre / qué la cierra:** primero, medir el orden en la app desplegada (una marca de
  tiempo al entrar en el manejador de sesión y otra en el de `load`, recargando dos veces). Si la
  sesión puede ganar, es un ciclo; si no, se documenta como imposible y se cierra.

### D-66 · Los activos ilegibles se leen como VACÍOS, sin rescate, y el primer guardado los sobrescribe
- **Qué es:** `loadRows` se traga el error y devuelve `[]` sin consola ni copia de rescate, al
  revés que `loadOpsAll`, que sí rescata y pone cerrojo. El primer guardado escribe `[]` encima del
  blob ilegible. No es el libro de operaciones —títulos y coste se rederivan del FIFO— pero sí se
  pierden objetivo, precio manual y moneda. **La asimetría entre los dos lectores ES el defecto**
  (§5.16), la misma forma que el 01-04 cerró en el otro lado.
- **Cómo se midió:** brazo A de la quinta transición (2026-09-05), reproducido ejecutando: el blob
  pasa de contener activos a `{"rows":[],"nextId":1}`, claves de rescate: ninguna, pantalla en
  verde. No re-verificado por el orquestador.
- **Estado:** abierta. Fuera del alcance del 01-08.
- **Qué la reabre:** nada la cierra sola.

### D-67 · El naranja de empate sale tras CADA sincronización correcta
- **Qué es:** al aplicar, META adopta el `savedAt` del documento; la escucha en vivo recibe ese
  mismo documento (Firestore siempre entrega el estado inicial) y el empate cae en `pendiente` →
  «Cambios sin subir», sin que haya ninguno. **Es el mismo texto con el que D-58 disfraza una
  pérdida real.** Un aviso que salta en cada sincronización correcta enseña a ignorar el único
  aviso que hay.
- **Cómo se midió:** brazo A de la quinta transición (2026-09-05), reproducido ejecutando. No
  re-verificado por el orquestador.
- **Estado:** abierta. Fuera del alcance del 01-08, pero conviene atacarla junto a D-59: es la
  máscara que hace invisibles a las otras.
- **Qué la reabre:** nada la cierra sola.

### D-68 · Dos pestañas del mismo navegador sin sesión se pisan el libro
- **Qué es:** no hay manejador `storage`, así que la última pestaña en guardar escribe su `ops` de
  memoria sobre el disco, con «Guardado ✓» en las dos. **Con sesión y red resiste**, porque el eco
  de la subida repara a la otra pestaña: la pérdida queda confinada al modo sólo-local y a los
  estados con la subida bloqueada (cerrojo, paquete incompleto, sin red).
- **Cómo se midió:** brazo A de la quinta transición (2026-09-05), reproducido ejecutando, con su
  control (con sesión y red) que resiste. No re-verificado por el orquestador.
- **Estado:** abierta. Fuera del alcance del 01-08.
- **Qué la reabre:** nada la cierra sola.

### D-69 · El punto de sincronía sigue en VERDE tras un guardado local fallido
- **Qué es:** `guardarTodo` pinta «No se pudo guardar» en rojo durante 5 segundos y **no toca el
  indicador durable**, que sigue diciendo «Sincronizado con tu cuenta.» con memoria y disco ya
  divergentes. El aviso existió cinco segundos; el estado que queda en pantalla miente.
- **Cómo se midió:** brazo A de la quinta transición (2026-09-05), reproducido ejecutando. No
  re-verificado por el orquestador.
- **Estado:** abierta. Adyacente a D-18 y D-23. Fuera del alcance del 01-08.
- **Qué la reabre:** nada la cierra sola.

### D-01 · El sync reemplaza el libro de operaciones en vez de fusionarlo
> **RE-MEDIDA el 2026-09-05 (quinta transición, brazo A): pasa de «no reproducida en vivo» a
> REPRODUCIDA.** Un documento más nuevo con 1 operación sobre 4 locales deja el disco en `["o1"]`
> con el punto en **verde «Sincronizado»**. Y tiene **dos puertas de entrada nuevas**, D-58 y D-65,
> que la cota parcial de `vaciariaElLibro` no cubre. Sigue siendo Fase 3 por su arreglo (fusionar
> por `id`), pero su daño ya no es hipotético.
- **Qué es:** `applySyncPayload` sustituye `ops` entero por lo que venga de la nube, con
  last-write-wins por un único `savedAt` de documento. Importar operaciones en el móvil sin red y
  abrir luego el portátil puede borrarlas sin aviso.
- **Cómo se midió:** lectura del código en la auditoría del 2026-08-29 (`index.html:2874`,
  `2911`). **No reproducido en vivo**: el comportamiento de Firestore con escrituras encoladas
  offline está razonado sobre la semántica documentada de `set()`, no observado.
- **Estado:** planificada como Fase 3 del roadmap. Depende de tener backup antes (D-02).
  **Cota parcial YA PUESTA** en el ciclo 01-02 (`77f8cef`): un único juez, `vaciariaElLibro`,
  cablea las dos guardas e impide el caso destructivo en los dos sentidos. La fusión real sigue
  siendo Fase 3. Ojo: la guarda de subida omite el push ENTERO, así que mientras el libro local
  esté vacío y la nube tenga operaciones, los cambios de activos tampoco suben. Es deliberado —
  fusionar es Fase 3— pero no es gratis.
- **Qué la reabre:** cualquier cambio en `buildSyncPayload`/`applySyncPayload` antes de la Fase 3.

### D-02 · No existe copia de seguridad fuera de Firestore
- **Qué es:** todo el estado vive en localStorage y en un único documento de Firestore que se
  pisan mutuamente. No hay exportación ni restauración.
- **Cómo se midió:** búsqueda de código de backup/restore en `index.html` — no hay ninguno.
- **Estado:** planificada como Fase 2. Arrastrada desde 2026-05-30.
- **Qué la reabre:** nada; está en cola.

### D-03 · El documento de Firestore crece hacia el límite de 1 MB

> **⚠️ A RE-MEDIR (2026-08-31, tercera transición).** La mitad del daño que describe —«el fallo
> de `set()` falla en silencio mientras el indicador sigue verde»— la cerró el ciclo 01-04, y se
> vio el ROJO en el navegador el 2026-08-31. El núcleo (el documento hacia 1 MB, el tamaño del
> paquete jamás medido) sigue abierto. Detalle: `01-TRANSICION-3.md`, hallazgo T3-7.
- **Qué es:** `buildSyncPayload` mete todos los snapshots mensuales de todos los activos en UN
  documento. Firestore corta en 1 MB, y el fallo de `set()` sólo hace `console.error`
  (`index.html:2945`) mientras el indicador de sync sigue verde.
- **Cómo se midió:** lectura del código. **El tamaño real del payload NO se ha medido nunca.**
- **Estado:** abierta, sin fase asignada.
- **Qué la reabre:** medir el payload. Si pasa de ~500 KB, sube a fase propia.

### D-13 · Las ramas de legado siguen colapsando compras idénticas del mismo día
- **Qué es:** `dedupeOps` por huella, que se conserva en `migrateOpsToGlobal` y en la rama `opsData`,
  no distingue dos compras legítimamente idénticas del mismo día dentro de la misma cartera.
- **Cómo se midió:** lectura del código, confirmada por la revisión adversaria del 2026-08-29
  (`index.html:988`, `1010`, `2877`).
- **Estado:** **límite aceptado a propósito**, vigente desde el ciclo 01-02 (`77f8cef`). La
  migración corre una sola vez y `opsData` sólo llega de un dispositivo sin actualizar. La rama
  moderna (`opsAll`) ya NO tiene este problema: deduplica por identificador Y huella, con
  autoprueba y sabotaje permanentes.
- **Qué la reabre:** que aparezca un dispositivo antiguo sincronizando de verdad, o que la migración
  tenga que volver a correr.

### D-18 · Que el aviso de guardado se PINTE de rojo no lo ejerce nadie
> **RE-MEDIDA el 2026-09-05 (quinta transición, brazo E): el mecanismo que describe YA NO EXISTE.**
> Desde el 01-06, `pruebasPintorDelGuardado` ejecuta el cuerpo del pintor y afirma `var(--red)`
> **por su valor**, y el banco tiene el sabotaje «colores INTERCAMBIADOS», que muerde con `rc=1`.
> Lo único que queda vivo de esta ficha es **que nunca se ha visto en un navegador real**. No
> confundir las dos cosas: el oráculo existe, la prueba humana no.
- **Qué es:** cuando el guardado falla, la app debe avisar en rojo en vez de decir «Guardado ✓».
  La DECISIÓN de avisar como error está cubierta: los invariantes sustituyen `showSaveIndicator`
  y comprueban que recibe `ok === false`, incluido el camino de éxito PARCIAL (los activos se
  guardan y el libro no). Lo que nadie ejerce es el último eslabón, dentro del cuerpo de
  `showSaveIndicator`: `el.style.color = ok ? 'var(--green)' : 'var(--red)'`. Al interceptar la
  función, el invariante nunca corre su cuerpo. Es exactamente la trampa de `CLAUDE.md` §5.6:
  cubrir el mecanismo no cubre su aviso.
- **Cómo se midió:** verificación manual de la Fase 1 en la app desplegada, 2026-08-30. Tres de
  los cuatro puntos se confirmaron en el navegador real (aviso verde al guardar; el naranja no
  aparece en uso normal; `?selftest=1` deja los datos intactos — 90 operaciones y 4 carteras,
  idénticas antes y después). El cuarto NO se comprobó: provocar un fallo real de guardado exige
  agotar el almacenamiento del navegador, y no se improvisó con 90 operaciones reales delante.
- **Estado:** abierto y acotado. Riesgo bajo —es un operador ternario de una línea— pero el
  eslabón no está ejercido y no se blanquea como comprobado. Hereda del ciclo 01-01, donde el
  aviso rojo se construyó y nunca se vio en pantalla.
- **NO la cierra la verificación del 2026-08-31.** Ese día se vio en el navegador el punto ROJO
  «No se pudo sincronizar», y es **otro indicador**: ése es `setSyncUI`, el de la SUBIDA a la nube,
  y se provoca inyectando una escritura que rechaza (receta en `01-04-VERIFICACION-NAVEGADOR.md`).
  D-18 habla del cuerpo de `showSaveIndicator`, el aviso del GUARDADO LOCAL. Confundirlos cerraría
  la ficha con la categoría equivocada, que es peor que dejarla abierta (§5.10).
- **Qué la reabre:** cualquier cambio en `showSaveIndicator` o en el tema de colores; y se cierra
  cuando exista una forma segura y repetible de provocar un fallo de guardado real.

### D-16 · La guarda de subida deja de sincronizar los activos, no sólo el libro
- **Qué es:** cuando la guarda salta, `schedulePush` abandona el push ENTERO. Mientras el libro
  local esté vacío y la nube tenga operaciones, tampoco suben carteras, activos, histórico ni
  precios. Es deliberado —fusionar es Fase 3— pero no es gratis: un usuario que borre todas sus
  operaciones a propósito deja de sincronizar lo demás indefinidamente.
- **Cómo se midió:** revisión del diff del ciclo 01-02, sobre `77f8cef`.
- **Estado:** aceptado a propósito, ya NO en silencio: desde este ciclo el indicador se pone
  naranja («Cambios sin subir») en vez de quedarse verde, que era el defecto de verdad.
- **Qué la reabre:** la Fase 3, que al fusionar libros hace innecesaria la guarda entera.

### D-17 · Sin conexión y sin caché, un dispositivo sin operaciones no sube nada
- **Qué es:** la guarda de subida necesita leer la nube, y `enablePersistence` es best-effort
  (falla con varias pestañas abiertas y en navegadores que no lo soportan). Sin caché y sin red, esa
  lectura falla. Se ha decidido fallar CERRADO: no se sube y se avisa en naranja.
- **Cómo se midió:** revisión del diff del ciclo 01-02. El comentario del propio código ya advertía
  de esto para las transacciones; la guarda nueva reintrodujo una lectura en ese camino.
- **Estado:** abierto y acotado. Sólo afecta a dispositivos SIN operaciones locales; el usuario con
  libro sigue subiendo directo, sin lectura previa. Se elige perder sincronía antes que perder el
  libro.
- **Qué la reabre:** que el modo avión se vuelva un caso de uso principal, o la Fase 3.

### D-19 · La lectura previa a subir puede contestarla la caché, no el servidor
- **Qué es:** antes de subir, un dispositivo con el libro local vacío pregunta a la nube si está
  vacía (`ref.get()` en `schedulePush`). Firestore tiene la persistencia activada
  (`db.enablePersistence({ synchronizeTabs: true })`), así que esa lectura puede resolverse desde
  la caché local. Con una caché anticuada, el dispositivo A cree que la nube sigue vacía, la
  guarda le deja pasar, y el `set()` machaca las operaciones que el dispositivo B ya había subido.
  La guarda hermana ya falla CERRADO cuando la lectura RECHAZA (D-17); lo que no cubre es que la
  lectura RESPONDA, y responda algo rancio.
- **Cómo se midió:** brazo de seguridad de la transición de la Fase 1, 2026-08-30, sobre el diff
  `69f728e..abe5e80`. Verificado en el código: la persistencia se habilita en `index.html:2855` y
  la lectura de la guarda no pasa `{ source: 'server' }`.
- **Estado:** abierto y acotado. **No es una regresión**: antes de esta fase no había guarda
  ninguna y ese dispositivo machacaba la nube SIEMPRE. Es el residuo que la guarda no alcanza.
  El arreglo obvio —forzar lectura de servidor— reintroduce y agrava D-17: sin red esa lectura
  rechaza y el dispositivo deja de sincronizar. El equilibrio pertenece a la Fase 3, que sustituye
  la guarda entera por una fusión y ya no necesita preguntar quién gana.
- **Qué la reabre:** la Fase 3; o que aparezca un caso real de dos dispositivos con la caché
  desincronizada.

### D-20 · El payload de la nube sólo está validado en el bloque del libro
- **Qué es:** el ciclo 01-02 blindó el tramo de `opsAll` de `applySyncPayload` (comprueba que sea
  un array, tolera entradas nulas). El tramo anterior, el de `portfolioData`, sigue sin validar:
  un documento con `portfolioData: { "1": null }` lanza una excepción al leer `pd.nextId` cuando
  `portfolios`, `currentPortId` y `nextId` YA se han reasignado a los valores de la nube y parte
  de las claves de activos ya se han escrito. Queda un estado a medias en memoria y en disco. Y un
  `nextId` no numérico deja `nextId = NaN`, con lo que todas las filas nuevas nacen con
  identificador `NaN`.
- **Cómo se midió:** brazo de seguridad de la transición de la Fase 1, 2026-08-30. Preexistente:
  el diff de la fase no tocó ese tramo.
- **Estado:** abierto. Zona ligada: una operación con campos absurdos que pase `dedupeOpsById`
  llega hasta el cálculo del FIFO —base de la renta— sin validación de forma.
- **Qué la reabre:** la Fase 3 reescribe `applySyncPayload`; la Fase 4 toca el FIFO. Lo que llegue
  antes.

### D-21 · La migración del formato antiguo con el libro ilegible no la ejerce nadie
- **Qué es:** `migrateOpsToGlobal` convierte el formato antiguo por cartera al libro único. El
  ciclo 01-01 le añadió un camino nuevo —saltar la cartera ilegible y rescatar su contenido— que
  ninguna autoprueba ejecuta. Es un camino de UNA SOLA OPORTUNIDAD: corre en la primera apertura
  tras actualizar un dispositivo viejo, y si pierde o duplica operaciones históricas no hay
  segunda ocasión de notarlo.
- **Cómo se midió:** brazo de radio de impacto de la transición de la Fase 1, 2026-08-30.
  `grep -n "migrateOpsToGlobal(" index.html` devuelve sólo su definición (1075) y su único
  llamante de producción (3420): cero llamantes en la zona de autopruebas.
- **Estado:** abierto. La función entera tiene llamante de producción, así que no es código
  muerto; lo que no está ejercido es su rama nueva.
- **Qué la reabre:** que se toque `migrateOpsToGlobal` o el formato antiguo `opsData`; y se cierra
  con una autoprueba que siembre una cartera antigua con blob ilegible.

### D-25 · Una reparación desde la nube descarta en silencio lo tecleado con el cerrojo puesto
- **Qué es:** con el cerrojo puesto, `saveOpsAll` lleva rato negándose, así que todo lo que el
  operador haya apuntado desde que abrió la app vive **sólo en memoria y en la pantalla**. Cuando
  llega de la nube un documento con operaciones, la reparación escribe **únicamente la lista de la
  nube** y el `loadOpsAll` final sustituye la memoria por ella: lo tecleado desaparece de la
  pantalla y del disco **sin ningún aviso**. La guarda de no-vaciado no protege aquí, porque la
  nube no viene vacía.
- **Cómo se midió:** revisión ligera del diff del ciclo 01-03 (2026-08-30). **No es una regresión**:
  el código anterior al ciclo también pisaba. Lo que cambia es que ahora sabemos que existe.
- **Estado:** ABIERTA, diferida por escrito. Es la misma familia que **D-01** (el sync reemplaza en
  vez de fusionar) y se cierra con ella en la Fase 3: fusionar local y nube es exactamente lo que
  este ciclo declaró fuera de alcance. Distinta de **D-23**, que se dispara al recargar; ésta se
  dispara al sincronizar. `pruebasPrecedenciaDeGuardas` construye justo ese estado (cerrojo puesto
  + memoria poblada) pero sólo ejercita la mitad de la nube vacía.
- **Qué la reabre:** nada la cierra sola. Si la Fase 3 fusiona y esta ficha sigue abierta, es que
  la fusión no cubrió el caso del cerrojo puesto.

### D-24 · La rama moderna del sync decide el cerrojo con memoria rancia y puede pisar un blob ilegible sin rescatarlo
- **Qué es:** `applySyncPayload` decide por `opsIlegible` **en memoria**, que sólo es tan fresco
  como la última `loadOpsAll()`. Si el libro se corrompe en disco **después** de que la app haya
  cargado (otra pestaña, corrupción del almacenamiento), la rama moderna cree que el cerrojo está
  bajado y `saveOpsAll` **pisa el blob corrupto sin hacerle copia de rescate**. La rama del formato
  antiguo NO tiene el problema: llama a `loadOpsAll()` dentro, así que re-deriva el cerrojo del
  disco y sí rescata. Mismo estado de disco, resultado distinto según el formato del payload.
  Arrastra dos asimetrías menores de aviso: una nube en formato antiguo vacía no emite ni el
  `[SYNC] libro recibido vacío` ni el «no llega nada con que repararlo»; calla donde la moderna
  es ruidosa.
- **Cómo se midió:** brazo adversario de correctness sobre el diff del ciclo 01-03 (2026-08-30),
  censando **todas** las asignaciones de `opsIlegible` del fichero, no sólo las del diff. Es un
  defecto **anterior al ciclo**: el 01-03 no lo introdujo, lo destapó al preguntarse si las dos
  ramas eran simétricas. **No reproducido en vivo**: exige corromper el almacenamiento entre la
  carga y la sincronización.
- **Estado:** ABIERTA, diferida por escrito. Cerrarla exige releer el disco antes de escribir —en
  cada guardado, no sólo en el sync— o mover el rescate dentro de la escritura cruda. Las dos
  opciones cambian el coste de `schedSave` y el contrato de `escribirOpsAll`, que este ciclo
  acababa de fijar; hacerlo aquí sería rediseñar la pieza recién puesta sin plan. Va con **D-01**
  (Fase 3), que ya tiene que revisar la semántica entera de `applySyncPayload`.
- **Qué la reabre:** nada la cierra sola. La frase «las dos ramas son simétricas» queda REFUTADA
  y no debe volver a escribirse hasta que exista una prueba que la sostenga. Si alguien afirma la
  simetría en un acta o un comentario, esta ficha es la refutación.

### D-23 · El cerrojo del libro ilegible no tiene salida visible para el operador
- **Qué es:** el ciclo 01-03 arregló que el cerrojo `opsIlegible` se levantase antes de confirmar
  la reparación. El precio es que ahora, con el libro local ilegible y una nube **vacía o
  ausente**, el cerrojo queda puesto **indefinidamente**: nada fuera de `loadOpsAll` y
  `repararLibroIlegible` lo baja, no hay interfaz para resolverlo, y el único aviso es un
  `console.error` que el usuario no ve. Y encadena: `saveOpsAll` devuelve `false` → `guardarTodo`
  devuelve `false` → no hay subida → **las operaciones nuevas viven sólo en memoria y se pierden
  al recargar**. Antes del ciclo, ese mismo caso se «resolvía» escribiendo `[]` encima con la copia
  de rescate a salvo: un reinicio con pérdida acotada. Ahora es un bloqueo silencioso. Es mejor
  para el dato y peor para el operador, y por eso se escribe en vez de esconderse.
- **Cómo se midió:** leyendo el código en la revisión adversaria del PLAN 01-03 (2026-08-30). Lo
  encontró Fable atacando la frase «el arreglo no empeora nada»; no salió de ejecutar nada.
- **Estado:** ABIERTA y aceptada a sabiendas. Construir la salida en pantalla es UX (Fase 5) y
  arrastraría a **D-18**, así que el ciclo 01-03 la declaró fuera de alcance por escrito.
  **Salida manual mientras tanto:** en las herramientas del navegador, comprobar primero que
  existe una clave `balance-ops-rescate-*` con el contenido original y **sólo entonces** borrar la
  clave `balance-ops`; al recargar, `loadOpsAll` leerá «no hay nada» en vez de «ilegible» y bajará
  el cerrojo. Ligada a **D-18** (el aviso en rojo no se pinta en ninguna prueba), a **D-15** y,
  desde el 01-04, a **D-35**: son la misma familia —un bloqueo correcto para el dato que el
  operador no puede ni ver ni resolver—. **Revisada en el 01-04 y NO cambia de forma:** el cerrojo
  pasó a ser entrada explícita del juez de subida (`libroIlegible`), lo que hace el bloqueo más
  visible en el código y le añade un aviso naranja en pantalla, pero **no le da salida**. Sigue
  igual de abierta y por el mismo motivo.
- **Qué la reabre:** nada la cierra sola. Se cierra cuando exista un aviso en pantalla que diga al
  operador que el libro está bloqueado y le ofrezca la salida sin abrir la consola. Si alguien
  quita el `if (opsIlegible)` de `saveOpsAll` para «desatascarlo», el sabotaje «saveOpsAll deja de
  consultar el cerrojo» se pone rojo: esta deuda se paga con interfaz, no aflojando el cerrojo.

### D-28 · La migración del formato antiguo se declara exitosa aunque su escritura falle
- **Qué es:** la Fase 1 cambió el contrato de `saveOpsAll`, que ahora devuelve `false` si no pudo
  escribir. `migrateOpsToGlobal` **ignora ese booleano** y devuelve `migrated: true` igualmente. Si
  la escritura falla, el arranque hace `ops = loadOpsAll()` → `[]` y el `schedSave()` siguiente
  puede sellar un libro vacío —una escritura pequeña sí cabe donde no cabía la grande—. A partir de
  ahí la clave ya no está ausente, la migración devuelve `migrated: false` **para siempre**, y las
  operaciones históricas quedan varadas en las claves antiguas. Es un camino de **una sola
  oportunidad**.
- **Cómo se midió:** brazo de radio de impacto de la segunda transición (2026-08-30), censando los
  llamantes de `saveOpsAll` tras el cambio de contrato. El dato no se destruye —las claves antiguas
  sobreviven— pero sale del libro vivo sin más rastro que la consola. **No reproducido en vivo:**
  exige la cuota agotada justo en la primera apertura tras actualizar.
- **Estado:** abierta. Distinta de **D-21**, que ficha la rama ilegible sin ejercer, no este
  contrato roto.
- **Qué la reabre:** nada la cierra sola. El arreglo es propagar el booleano al resultado; hace
  falta además una autoprueba que falle la escritura y exija `migrated: false`.

## Abiertas — corrección fiscal

### D-04 · El orden de operaciones del mismo día lo decide el azar
- **Qué es:** el desempate del FIFO es lexicográfico por `id`, y `genOpId` lleva un sufijo
  aleatorio, así que una compra y una venta del mismo día pueden procesarse al revés.
- **Cómo se midió:** lectura del código (`index.html:1015`, `1042`).
- **Estado:** Fase 4, plan 04-01. **Reducida a medias, sin querer, por el ciclo 01-02**
  (`77f8cef`): los identificadores NUEVOS llevan un contador de ancho fijo delante del azar, así
  que entre ellos el desempate ya es el orden de entrada, no el azar. Pero esto NO cierra la deuda:
  (a) los identificadores YA guardados siguen siendo aleatorios y son los del histórico fiscal;
  (b) el orden de entrada tampoco es necesariamente el orden real de las operaciones dentro del
  día. Sigue haciendo falta un criterio explícito, que es lo que hace la Fase 4.
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

### D-09 · Trece funciones por encima del presupuesto de 60 líneas
- **Qué es:** deuda de tamaño declarada y congelada. Sólo pueden encoger; ninguna función nueva
  puede unirse a la lista.
- **Cómo se midió:** `tools/funcsize.py`, re-medido el 2026-08-29 tras el plan 01-01. La cifra de
  funciones vistas vive sólo en `.paul/baseline-funcs.json`, porque copiarla aquí la desactualiza
  al siguiente ciclo — ya pasó dos veces el mismo día. Los trece tamaños de abajo sí se citan porque están congelados:
  si cambiaran, el trinquete se pondría rojo. Exenciones nombradas una a una:

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
  | `onScreenshotPicked` | 67 | OCR de capturas de pantalla; se toca en la Fase 5 |

- **Estado:** congelada. El trinquete impide que empeore.
- **Añadida el 2026-08-30 (ciclo 01-04): `onScreenshotPicked`, 67 líneas.** No es código nuevo:
  ya excedía, pero el trinquete **no la veía** porque es una `async function` y su ámbito sólo
  cubría `function NOMBRE(`. El ciclo 01-04 amplió el ámbito (semántica versión 1 → 2, es un
  APRIETE de la vara) y apareció. Lo destapó el banco de sabotaje, no el razonamiento: al volver
  `runSelfTests` asíncrona, el mutante «el monolito engorda» dejó de morder porque la función
  había salido de la medida. **Sellarla sin nombrarla aquí habría sido aflojar en silencio**, y lo
  cazó el brazo adversario de cableado del propio ciclo.
- **Qué la reabre:** tocar cualquiera de esas funciones en su fase correspondiente — es la
  ocasión de bajarla del listado. Y si aparece una decimocuarta, el trinquete se pone rojo.

### D-26 · `funciones_vistas` es una cifra sellada que nadie vuelve a derivar
- **Qué es:** `tools/funcsize.py` **escribe** `funciones_vistas` en la foto al hacer `--update` y
  no la lee nunca; `--check` la ignora por completo. Es una cifra en un fichero que parece medida
  y no vigila nada. Es la misma trampa que `CLAUDE.md` §9 describe para los recuentos copiados a
  mano en un documento: se desfasan y luego se citan como si fueran ciertos.
- **Cómo se midió:** revisión ligera del diff del 01-03 (2026-08-30). En la revisión `bbb0e9c` la
  foto decía **153** cuando `index.html` tenía **162** funciones de primer nivel, **y la puerta
  estaba verde**. El resellado de este ciclo la deja en 168, que hoy sí casa; nada impide que se
  vuelva a desfasar.
- **Estado:** ABIERTA. No se toca en el 01-03: cambiar qué compara `--check` es cambiar la regla de
  medida, y eso el propio instrumento lo declara **deriva (rc=3)**. Hacerlo dentro de un ciclo que
  va de otra cosa sería mover la vara sin plan. Ligada a **D-10** y **D-14**, que son las otras
  cegueras declaradas del mismo instrumento.
- **Medición nueva, 2026-08-31 (ciclo 01-05):** la foto sella **186** y el código tiene **190**.
  Ya se ha vuelto a desfasar, como decía la ficha, **y la puerta sigue verde**. Se derivó de
  rebote al comprobar el remedio del mensaje de foto corrupta: borrar la foto y resellar produce
  un fichero que difiere del original **exactamente en esa cifra**. No se resella: el 01-05 tiene
  esto en sus límites de alcance por escrito, y resellar aquí escondería la munición de D-26.
- **Qué la reabre:** nada la cierra sola. Se cierra cuando `--check` compare la cifra —y entonces
  hace falta su sabotaje: desfasarla a mano tiene que poner la puerta roja.

### D-10 · El trinquete de tamaño no ve funciones flecha
- **Qué es:** `funcsize.py` sólo ve `function NOMBRE(...)` de primer nivel. Una función de 300
  líneas escrita como `const f = () => {…}` le es invisible.
- **Cómo se midió:** ceguera declarada a propósito en la cabecera del propio instrumento.
- **Estado:** abierta y **declarada**, no descubierta. Un límite declarado es un límite; uno
  descubierto después es un agujero.
- **Qué la reabre:** que aparezca código nuevo escrito con funciones flecha grandes.

### D-14 · La distinción entre una regex y una división es heurística
- **Qué es:** para contar llaves, `funcsize.py` decide si una barra abre una expresión regular
  mirando el carácter anterior. Es lo que hace cualquier tokenizador sin gramática completa, y
  puede equivocarse con construcciones raras.
- **Cómo se midió:** la revisión de falsos verdes del 2026-08-29 construyó el caso `throw /}/;`
  —JavaScript válido— y demostró que el instrumento medía una función de 85 líneas como si
  tuviera 2, **en silencio y sin dar rc=2**. Se añadieron `throw`, `yield` y `await` a la lista, y
  hay un sabotaje permanente que mete esa función y exige que el instrumento la vea.
- **Estado:** el caso conocido está cerrado; la clase (heurística sin gramática) sigue abierta.
- **Qué la reabre:** cualquier otra palabra clave tras la que una barra abra regex. Si aparece,
  se añade a la lista y se le pone su sabotaje.

---

## Abiertas — limpieza

### D-52 · La DERIVA (rc=3) sólo ve el diccionario de semántica, no el código que mide
- **Qué es:** los cuatro trinquetes (`funcsize`, `emptycatch`, `avisos`, `sumideros`) declaran
  DERIVA comparando un diccionario `SEMANTICA` sellado. Pero la regla de medida real vive también
  en el CÓDIGO: la expresión regular del censo, el enmascarado, el detector de declaraciones.
  Cambiar cualquiera de ésos cambia lo que se mide **sin que salga rc=3**: sale rotulado como
  hallazgo o como mejora, y el operador resella.
- **Cómo se midió:** brazo del aparato de medición del 01-07 (2026-09-01), leyendo los cuatro
  instrumentos. Ejemplo vivo del propio ciclo: al ampliar el censo de sumideros para ver
  `f?.()` y las referencias, la foto cambió de 10 a 16 claves y el instrumento lo llamó
  «sumideros NUEVOS», no deriva.
- **Estado:** abierta. Afecta a los cuatro por igual; **no es un defecto del 01-07**, es la forma
  del patrón. Se ficha porque la cabecera de `sumideros.py` vende «la dirección viaja DENTRO de la
  semántica sellada» como si el diccionario fuera la regla entera, y no lo es.
- **Qué la reabre:** nada la cierra sola. El arreglo natural es meter en la semántica una huella
  del propio código de medida (por ejemplo, de las expresiones regulares).

### D-53 · El veredicto de `verify.sh` deja que un rc=2 posterior pise un rc=1 anterior
> **RE-MEDIDA el 2026-09-05 (quinta transición, brazo C): CONFIRMADA, y en las dos direcciones.**
> `rc=1` seguido de `rc=2`, `rc=2` seguido de `rc=1` y `rc=1` seguido de `rc=3` acaban todos con el
> veredicto del último. Matiz que la ficha no decía: **el FALLO y su mensaje sí aparecen** en la
> lista de pasos; lo que se pierde es el veredicto final y el código de salida.
- **Qué es:** el bloque de veredicto imprime DERIVA, luego ROTO, luego HALLAZGOS. Si un paso da un
  hallazgo real (rc=1) y **otro posterior** da instrumento roto (rc=2) —por ejemplo `hookcheck` en
  una máquina sin el enganche, o `ruff` ausente—, el veredicto sale «DEGRADADO (rc=2)» **sin
  nombrar el hallazgo**, y manda a mirar las herramientas en vez del código. Es la misma trampa que
  §4.3 dice arreglada, arreglada sólo para el banco de sabotaje.
- **Cómo se midió:** brazo de alcance del 01-07 (2026-09-01), observado ejecutando la puerta sobre
  una copia sin `.git`: FALLO del banco + ROTO de hookcheck → rc=2 sin mencionar el hallazgo.
- **Estado:** abierta. **Preexistente**, viene del 01-05 (D-41); el 01-07 no la introduce ni la
  agrava.
- **Qué la reabre:** nada la cierra sola. Se cierra decidiendo el orden a propósito: el mensaje del
  hallazgo tiene que aparecer aunque el rc final sea 2.


### D-55 · Cambiar el interruptor de objetivos guarda EN SILENCIO, mientras el resto confirma
- **Qué es:** `onUseTargetsToggle` modifica los datos del operador, los guarda y programa la subida,
  y en el camino de ÉXITO **no pinta nada**. Sólo avisa cuando `saveMeta()` FALLA. `guardarTodo`, en
  cambio, confirma con «Guardado ✓». Dos acciones que cambian los mismos datos, una confirma y la
  otra calla.
- **Cómo se midió:** **observación del operador en producción**, 2026-09-05, durante la verificación
  del 01-07: «marco y desmarco y no pasa nada con el puntito». Contrastado contra el código y
  **comprobado que sí persiste**, en vez de suponerlo: con la casilla marcada, `balance-meta-v2`
  devuelve `{id:'p1779839499052qkfo', name:'🤖 Robótica', useTargets: true}`. O sea: guarda de
  verdad, y calla.
- **Estado:** abierta, **menor**. No hay pérdida de datos ni pantalla que mienta: hay AUSENCIA de
  confirmación. Por eso no abre ciclo ni bloquea el 01-07.
- **Por qué se escribe igual:** la meta de la fase es que el operador pueda fiarse de lo que ve. Un
  camino que cambia datos sin confirmar enseña a no mirar el aviso, y eso desarma la única capa que
  el operador realmente lee. Es la contrapartida del defecto que el 01-06 cerró para el verde falso.
- **Qué la reabre / cierra:** se cierra igualando el camino de éxito al de `guardarTodo`. Si se hace,
  necesita control propio: el 01-06 midió que un aviso puede degradarse sin poner nada en rojo.

### D-56 · Dos de los cuatro llamantes pasan el motivo SIN control que lo mate
> **RE-MEDIDA el 2026-09-05 (quinta transición, brazos B y E): la ficha mide una cosa por otra.**
> No son «dos sin control» sin más: el llamante de `subirALaNube` sin motivo **sobrevive a la
> puerta entera** (`rc=0`), mientras que el de la escucha en vivo pone la puerta roja **por un
> accidente del banco** («BANCO ROTO: ancla no única»), no porque ningún aserto lo cace — las
> autopruebas dan OK. Uno es invisible; el otro está tapado por un instrumento roto, y su mensaje
> **dirige la mano al sitio equivocado**. Los dos entran en **D-59**, que los cierra por receptor.
- **Qué es:** el motivo del veredicto llega hoy a la pantalla desde cuatro sitios —la bajada, el
  arranque, la subida (`subirALaNube`) y la escucha en vivo (`listenFirestore`)—. **Sólo los dos
  primeros tienen control positivo**: quitarles el motivo pone la puerta en `rc=1`. En los otros dos
  se puede borrar el segundo argumento y **todo sigue en verde**, con lo que su naranja volvería a
  salir sin causa.
- **Cómo se midió:** al cerrar D-54, el 2026-09-05. No es una sospecha: el mismo hueco se **midió
  ejecutando** en los otros dos eslabones —revertirlos daba `rc=0`— y por eso se les escribió
  oráculo. Los dos que quedan no se midieron uno a uno; se sabe que **ningún aserto nombra su
  motivo**, que es la condición que hace pasar el mutante.
- **Estado:** abierta, **ceguera declarada**, no falso verde. La pantalla hoy dice la verdad en los
  cuatro caminos; lo que falta es el guardián que lo mantenga mañana.
- **Por qué no se cierra ahora:** los dos caminos que faltan piden arnés propio (la subida ya lo
  tiene para otras cosas; la escucha en vivo no se ejerce entera fuera del navegador). Hacerlo
  dentro de un ciclo que iba de otra cosa sería mover la vara a mitad de partido.
- **Qué la reabre / cierra:** se cierra con un aserto por camino que nombre su motivo, y su mutante.
  Mientras tanto, cualquier `setSyncUI(estadoSync(decision.aviso))` **sin segundo argumento** en esos
  dos sitios es una regresión que hoy nadie caza.

### D-57 · Al arrancar con lo local MÁS NUEVO que la nube, no se sube: se queda naranja
- **Qué es:** en `alIniciarSesion`, si la bajada devuelve un veredicto de rechazo, el arranque
  **no intenta subir** —sólo sube cuando la lectura NO está sincronizada— y deja el indicador en
  naranja. Un dispositivo que tiene lo más reciente puede quedarse **indefinidamente sin publicarlo**
  si el operador no guarda nada: la subida sólo la dispara un guardado posterior.
- **Cómo se midió:** **en producción**, 2026-09-05, durante la verificación del 01-07. El texto que
  la app pintó sola dice: `documento NO más nuevo (1788612341197 <= 1788612344603) con 89
  operaciones locales que proteger`. Lo local es ~3,4 s más nuevo que el documento.
- **Estado:** abierta, **menor**. No hay pérdida —los datos están en local y la nube conserva los
  suyos— y el aviso **no miente**: dice «cambios sin subir», y los hay. Lo que falla es que nada los
  empuja solo.
- **Por qué no se arregla aquí:** subir tras un rechazo de bajada es una decisión de política de
  sincronización, no un fallo de aviso; toca el mismo terreno que D-51 (el desempate por reloj de
  pared) y **la meta declarada de la Fase 3**. Meterlo en un ciclo que iba de la capa de aviso sería
  mover la vara a mitad de partido.
- **Qué la reabre / cierra:** se cierra decidiendo en la Fase 3 quién gana y quién publica. Ojo al
  cruzarlo con D-51: subir automáticamente cuando lo local parece más nuevo **por un reloj
  adelantado** es exactamente cómo se machaca la copia buena de otro dispositivo.

### D-22 · El instrumento de radio de impacto no ve el producto
- **Qué es:** el brazo G7 de la transición de fase es `code-review-graph`, que construye un grafo
  del código y calcula el alcance de un cambio. **No parsea el JavaScript inline de un `.html`**,
  así que `index.html` —que ES el producto— no entra en su grafo. Corre, tarda, da rc=0 y presenta
  un panel de ahorro de tokens sobre un análisis que no ha mirado el fichero que la fase cambió.
  Es un instrumento que existe y no dispara ningún objetivo: por `CLAUDE.md` §0, no existe.
- **Cómo se midió:** transición de la Fase 1, 2026-08-30. Tras `code-review-graph build`, el grafo
  tiene 49 nodos repartidos en 10 ficheros y **ninguno es `index.html`** (consultado directamente
  contra `.code-review-graph/graph.db`, agrupando por `file_path`). `detect-changes --base 69f728e`
  reporta «25 funciones cambiadas» y «Untested: roto, main, noop, el, k», que son nombres de
  `tools/` y `sync.py`, no del producto. Es la misma ceguera que ya tenía `smart_search`.
- **Estado:** abierto. G7 queda declarado **DEGRADADO** y sustituido, en esta transición, por un
  análisis de radio de impacto hecho con grep dirigido por un revisor adversario; ese sustituto
  encontró seis huecos de cobertura reales, así que el brazo no se saltó, se reemplazó.
- **Qué la reabre:** nada la cierra por sí sola. Se cierra cuando el grafo indexe el `<script>` de
  `index.html`, o cuando el sustituto por grep se convierta en un script del repo cableado a la
  puerta —que es lo que exige `CLAUDE.md` §4.1 si el juicio se repite por tercera vez.

### D-32 · Las copias de rescate del libro no tienen tope ni caducidad
- **Qué es:** `rescatarOpsIlegible` guarda el blob ilegible en una clave `balance-ops-rescate-<marca
  de tiempo>` para no perderlo. Deduplica por contenido exacto, pero nada limita cuántas copias se
  acumulan si el contenido cambia cada vez (corrupción parcial repetida). Es un riesgo de agotar la
  cuota del navegador, que a su vez es la causa de varios de los fallos de guardado que esta misma
  fase intenta hacer visibles.
- **Cómo se midió:** brazo de seguridad de la segunda transición de la Fase 1 (2026-08-30).
  Severidad BAJA: el dato que se guarda es el que ya estaba en local, no dato externo, y no hay vía
  de explotación por un tercero.
- **Estado:** abierta. Es deuda de limpieza, no de pérdida de datos: la red de rescate existe
  precisamente para no perder nada.
- **Qué la reabre:** nada; se cierra cuando el rescate conserve las N últimas copias en vez de
  todas. Va bien con la copia rotativa de la **Fase 2**, que ya tiene que resolver ese mismo
  problema.

### D-11 · `worker.js` es un proxy obsoleto
- **Qué es:** proxy de precios de Yahoo, sin uso desde que se quitó la obtención automática de
  precios.
- **Cómo se midió:** confirmado en la auditoría del 2026-08-29.
- **Estado:** Fase 6, plan 06-04. Incluye borrar también el Worker en el panel de Cloudflare.
- **Qué la reabre:** nada; está en cola.

---

## Cerradas en el ciclo 01-07 (2026-09-01)

### D-54 · El naranja afirmaba UNA causa y se alcanza por OCHO — CERRADA 2026-09-05
> **Ubicación corregida el 2026-09-05 (quinta transición, brazo D):** esta ficha vivía bajo
> «Abiertas — limpieza» con el campo `Estado: CERRADA`. Es el mismo defecto de forma que ya se
> corrigió para D-38 en la cuarta transición: escribir la lección no la evita (§5.17).

- **Qué es:** `setSyncUI('pendiente')` pinta un texto fijo —«Cambios sin subir: este dispositivo no
  tiene operaciones y no se pisa el libro de la nube»— que **afirma un motivo concreto**. Pero el
  aviso `pendiente` lo devuelven hoy **ocho** veredictos distintos del producto (`activos`,
  `libro-ilegible`, `nube-ilegible`, `nube-no-mas-nueva`, `reloj-desconocido`, `sin-carteras`,
  `sin-documento`, `vaciaria`), y el texto sólo describe uno de ellos. El veredicto **ya lleva su
  `clave` y su `motivo` en lenguaje llano**: la información existe y **se tira antes de llegar a la
  pantalla**. Dos líneas más abajo, el estado `error` documenta en un comentario que no reutiliza el
  mensaje de `auth` «porque su mensaje mentiría sobre la causa». Aquí miente.
- **El 01-07 la agrava sin introducirla.** Antes del ciclo llegaban **cuatro** claves al mismo
  naranja (derivado de `685b44b`), así que el texto ya era falso en tres de ellas. El ciclo añadió
  cuatro más, y una —`reloj-desconocido`— es la que ve **todo dispositivo ya sincronizado** en su
  primer arranque tras el despliegue (D-50). Pasó de texto raramente falso a texto que ve todo el
  mundo el día del estreno.
- **Cómo se midió:** **en producción, el 2026-09-05**, no en laboratorio. Fue lo primero que el
  operador vio al abrir la app desplegada, con 90 operaciones en el dispositivo, y preguntó si era
  normal. Las claves se **derivan del código**, no se enumeran a mano:
  `re.findall(r"aviso: 'pendiente',\s*(?:aplicado: \w+,\s*)?clave: '([a-z-]+)'", index.html)`
  da 9 sobre el fichero entero, de las cuales `nube-mas-vieja` es un fixture de
  `pruebasArranqueTrasRechazo` y no del producto ⇒ **8**.
- **Por qué importa aquí y no es cosmética:** la meta de la Fase 1 es que la pantalla no mienta. Un
  naranja que atribuye mal la causa manda al operador a mirar donde no es, y en el caso medido le
  dice que **no tiene operaciones** a alguien que tiene noventa. Es el gemelo exacto del defecto que
  el 01-06 cerró para el verde.
- **Estado: CERRADA** el 2026-09-05, dentro del propio 01-07 (el ciclo la agravó y §3.4 prohíbe
  entrar en UNIFY con correctness sin atender).
- **Cómo se cerró:** por la CLASE. `textoPendiente(motivo)` compone el texto **a partir del motivo
  del veredicto**, que ya venía escrito en lenguaje llano y se tiraba una línea antes de la pantalla;
  y sin motivo **no se inventa causa** — fallar cerrado también en la pantalla. No hay tabla de
  textos por clave que mantener, así que un veredicto nuevo llega solo.
- **Controles, con su control positivo transcrito:** revertido el pintor, `rc=1` y mueren cuatro
  asertos («D-54 el PINTOR usa el motivo del veredicto: esperaba true, obtuve false»). **Y el CABLE
  aparte**: revertidos los dos llamantes con el pintor intacto, la primera versión de las pruebas
  daba **rc=0** —cubrir el mecanismo no cubre su cable (§5.6)—, así que `pruebasCableDelMotivo`
  ejerce la bajada y el arranque enteros y espía el segundo argumento. Revertida la bajada: `rc=1`,
  «esperaba documento NO más nuevo (…), obtuve undefined». Revertido el arranque: `rc=1`, «esperaba
  sin marca de tiempo en lo local…, obtuve undefined». **Cuatro sabotajes permanentes** en el banco,
  uno por eslabón más el del motivo ausente: un control positivo de hoy es una anécdota fechada.
- **Lo que este cierre destapó:** tres sabotajes ya existentes **dejaron de morder** porque el
  cambio movió sus anclas; la puerta lo cantó con `rc=1` y el mensaje «CONTROLES QUE NO MUERDEN (3)»
  en vez de pasar en verde. Reanclados los tres.
- **Cómo NO se arregla:** enumerando a mano las ocho claves. Una lista blanca sólo protege de lo que
  ya conoce (§5.15) y la novena nace mintiendo. Se cierra la **clase**: o el texto sale del veredicto,
  o —si la clave no se reconoce— el aviso **no afirma ninguna causa**. Fallar cerrado también en la
  pantalla.
- **Qué la reabre:** que aparezca una clave de `pendiente` cuyo texto en pantalla no proceda de su
  veredicto. Necesita control propio, derivado del código y con su mutante: sin él sería §5.1.


> Las cinco se cerraron **midiendo contra el código**, y cada arreglo tiene su control positivo en
> `tools/sabotage.py`: revertirlo pone la puerta en rojo con un mensaje propio. Las transcripciones
> literales de rc y mensaje están en el acta del ciclo.

### D-45 · Al arrancar, una nube MÁS VIEJA empobrecía el libro y la pantalla quedaba en VERDE — CERRADA 2026-09-01
- **Qué era:** `pullFromFirestore` decidía el desempate con `hasRealLocalData()`, que mira **sólo
  los activos**. Un operador que lo tuviera todo vendido —activos vacíos, libro fiscal rico— caía
  en la primera rama y **cualquier** documento de la nube ganaba, por viejo que fuera. Y al
  terminar, el punto de sync se pintaba en VERDE.
- **Cómo se cerró, por la CLASE y no por el caso:** un juez PURO `decidirBajada`, consultado por
  los **dos** caminos de bajada —el arranque y la escucha en vivo, que tenía su propio desempate
  escrito aparte—. «Hay datos que proteger» son DOS primitivos que se suman: `tieneOperaciones`
  (el juez único del 01-02, que es lo que faltaba) y los activos (lo que se miraba antes). Sumarlos
  en vez de sustituir evita abrir la mitad simétrica (§5.16). `hasRealLocalData` **conserva** su
  semántica, porque alimenta además la guarda de activos de `decidirSubida`.
- **Y hubo que arreglar tres cosas más para que el cierre no fuera FICTICIO:**
  1. **El reloj** (D-30): sin conservar la marca del documento aplicado, `localSaved` volvía a 0 y
     todo documento parecía más nuevo. La rama que cierra D-45 no habría disparado NUNCA.
  2. **El reloj DESCONOCIDO**: el día del despliegue, todos los dispositivos ya sincronizados
     tienen META sin marca. Sin la rama `reloj-desconocido`, el arreglo no protegía a nadie en su
     primer arranque — control verde y daño vivo (§5.10). Coste declarado en **D-50**.
  3. **La pantalla**: la bajada devolvía el mismo valor aplicara o rechazara, y el arranque lo
     traducía a verde. Ahora devuelve un VEREDICTO y el arranque deriva de él lo que pinta. La
     escucha en vivo también pinta el aviso de su veredicto: los dos caminos tenían que coincidir
     TAMBIÉN en lo que el operador mira, y sólo uno pintaba.
- **Controles positivos:** ocho, uno por pieza. Volver el desempate a «sólo activos», a «sólo
  libro», quitar la rama del reloj desconocido, quitar el `savedAt` al aplicar, reponer el verde
  incondicional del arranque, dejar la escucha en vivo sin consultar al juez, o dejarla rechazando
  sin pintar: **todos rc=1**.
- **Estado:** **CERRADA**.
- **Qué la reabre:** que aparezca un tercer camino por el que la nube entre sin pasar por
  `decidirBajada`, o que la Fase 3 reescriba la fusión sin traerse este juez.

### D-46 · El cruce «sólo falla el guardado de la lista de carteras» no tenía oráculo — CERRADA 2026-09-01
- **Qué era:** quitar `okMeta` del veredicto de `guardarTodo` dejaba **la puerta entera en `rc=0` y
  VERDE**. Con la cuota llena, el operador veía «Guardado ✓» en verde Y además se subía a la nube.
- **Cómo se cerró:** `pruebasCruceSoloMeta` hace fallar **únicamente** la escritura de la lista de
  carteras —no el libro, no los activos— y exige `guardarTodo() === false`, el aviso ROJO **por su
  valor** (`var(--red)`) y **cero** subidas, espiadas reasignando el lanzador (§5.9). El
  almacenamiento sustituido se restaura en `try/finally`.
- **Control positivo:** `const todoBien = okRows && okOps;` → **rc=1**, «AC-6 con SÓLO la lista de
  carteras rota, el guardado dice que no».
- **Estado:** **CERRADA**.
- **Qué la reabre:** que el veredicto del guardado vuelva a tener sumandos sin fila propia.

### D-27 · `persistOps` cantaba «Guardado ✓» antes de saber si el libro entró — CERRADA 2026-09-01
- **Qué era:** `persistOps` —borrar una operación y confirmar una importación— tiraba el booleano
  de `saveOpsAll` y `saveRows()` pintaba «Guardado ✓» en VERDE por su cuenta.
- **Cómo se cerró, por la CLASE:** el mismo reparto que `guardarTodo` (los activos se guardan sin
  anunciar y el aviso se decide al final), **y además** `persistOps` devuelve su veredicto, porque
  el panel de importación tenía su PROPIO anuncio de éxito —mucho más grande que el indicador— que
  se pintaba en verde pasara lo que pasara, después de haber vaciado la importación pendiente: el
  operador no podía reintentar y al recargar las operaciones ya no estaban. Cerrar sólo el
  indicador habría sido el caso disfrazado de clase (§5.10). Lo destapó la revisión del diff.
- **Controles positivos:** dar por bueno el guardado del libro → **rc=1**, «AC-7 un libro que no se
  guarda NO se anuncia en verde»; devolver `true` fijo → **rc=1**, «AC-7 y devuelve false para que
  el panel de importación no mienta». Con control de VACUIDAD: sin fallo sembrado, sigue verde.
- **Estado:** **CERRADA**.
- **Qué la reabre:** que aparezca un tercer anuncio de éxito en ese camino. Lo vigila
  `tools/sumideros.py`.

### D-29 · La invariante «si el guardado local falló, no se sube» sólo la respetaba `guardarTodo` — CERRADA 2026-09-01
- **Qué era:** `onUseTargetsToggle` hacía `saveMeta(); schedulePush();` seguido: con `saveMeta`
  fallido, subía igualmente y machacaba la copia buena de la nube.
- **Cómo se cerró, por la CLASE:** la subida está condicionada al resultado, y el conjunto de
  salidas queda **sellado** en `.paul/baseline-sumideros.json`: hoy hay exactamente dos llamantes
  de producción del lanzador de subidas, los dos gobernados, más la referencia del arranque,
  nombrada. Un sumidero nuevo pone la puerta en rojo.
- **Control positivo:** `if (saveMeta() || true)` → **rc=1**, «AC-7 el interruptor NO sube si la
  lista de carteras no se guardó».
- **Estado:** **CERRADA en su daño**: no queda ningún camino que suba tras un guardado local
  fallido. Los **cinco** llamantes de `saveMeta` que siguen ignorando su booleano **no suben ni
  anuncian**, así que su daño es otro y tiene ficha propia: **D-48**. Se dice aquí para que nadie
  lea esta ficha como «ya no queda nada».
- **Qué la reabre:** un sumidero de subida nuevo sin gobernar. Lo vigila `tools/sumideros.py`.

### D-30 · `applySyncPayload` escribía META sin `savedAt` — CERRADA 2026-09-01
- **Qué era:** tras aplicar un documento de la nube, META se reescribía **sin el campo `savedAt`**.
  La siguiente lectura calculaba `localSaved = 0` y cualquier documento posterior se consideraba
  más nuevo.
- **Cómo se cerró, y por qué CRUZANDO un boundary:** su ficha decía «va con la Fase 3», y los
  boundaries del plan dicen que la resolución por `savedAt` es Fase 3. **Se cruza y se dice en voz
  alta**: sin esto, el cierre de D-45 habría sido ficticio —pasaría su control con el daño vivo—.
  Lo que NO se toca es la **semántica de fusión** (unir operaciones por `id`, marca por sección),
  que sigue entera en la Fase 3. Se conserva la marca del documento APLICADO; poner la hora actual
  marcaría lo local como más nuevo y bloquearía sincronizaciones legítimas.
- **Controles positivos:** quitar el `savedAt` → **rc=1**, «AC-3 la marca de tiempo del documento
  SOBREVIVE al aplicar»; usar `|| Date.now()` en vez de `|| 0` → **rc=1**, «AC-3 un documento SIN
  marca deja el reloj local en cero».
- **Estado:** **CERRADA**. Su consecuencia sobre dispositivos ya sincronizados está en **D-50**, y
  el sesgo de relojes entre dispositivos en **D-51**.
- **Qué la reabre:** que la Fase 3 cambie quién escribe META al aplicar.

---

## Cerradas en la CUARTA transición (2026-09-01)

### D-15 · La guarda de subida está comprobada por presencia, no por precedencia — CERRADA 2026-09-01
- **Qué era:** la guarda que impide subir un libro vacío se comprobaba sólo por PRESENCIA: los
  sabotajes demostraban que `schedulePush` **llamaba** al juez, no que su veredicto se respetara ni
  que corriera ANTES del `set()`. Medido en el 01-02: `if (false && vaciariaElLibro(...))` dejaba
  la puerta verde.
- **Cómo se cerró:** el ciclo **01-04** reescribió la zona entera —una sola puerta de subida,
  `subirALaNube`, gobernada por el juez puro `decidirSubida`— y cerró la deuda **sin que nadie lo
  anotara**. La cuarta transición (2026-09-01) lo re-midió en vez de heredarlo, sobre copia
  aislada y con el ancla afirmada única antes de mutar:
  `if (!decision.subir)` → `if (false && !decision.subir)` en `subirALaNube` da
  **`rc=1`, «FALLO autopruebas (runSelfTests)», «HALLAZGOS (rc=1)»**.
  Ignorar el veredicto del juez MUERDE. Presencia **y** precedencia están ejercidas.
- **Estado:** **CERRADA**. La ficha se cierra citando la medición de hoy, no el acta del 01-04:
  una medición commiteada no se hereda (`CLAUDE.md` §7).
- **Qué la reabre:** que el camino de subida vuelva a tener más de una salida, o que la Fase 3
  reescriba la zona sin traerse su arnés.

---

## Cerradas en el ciclo 01-06 (2026-08-31)

### D-38 · La capa de AVISO no tiene oráculo: nueve mutantes sobreviven a la puerta entera
- **Qué es:** el aparato de medición cubre el MECANISMO de las guardas pero no su AVISO. Sustituir
  en `showSaveIndicator` el color condicional por un verde fijo —o sea, **pintar en VERDE un
  guardado que ha fallado**— deja `tools/verify.sh` en `rc=0` y «VERDE — todo ejercido y en
  verde», con el banco de sabotaje ejecutado y en OK. Otras ocho mutaciones de la misma capa
  sobreviven igual: la duración del aviso de error, el `aviso` que devuelve `decidirSubida` en sus
  ramas de rechazo, y tres mensajes de consola degradables a informativos. Es **§5.6**: el
  mecanismo tiene control, su aviso no.
- **Por qué es invisible hoy:** `tools/dom_stub.js` devuelve `null` en `getElementById`, así que el
  CUERPO de `showSaveIndicator` es código muerto en node; las autopruebas lo sustituyen por un
  espía, o sea que miden que los llamantes pasan `ok=false`, nunca qué hace la función con ese
  `false`. La matriz de 84 filas comprueba `clave` y `subir`, **nunca `aviso`**. Y
  `cloudwrites.py` prohíbe el literal `setSyncUI('ok')`, no un `estadoSync('ok')` alimentado por
  el juez — D-31 cerró el caso literal, no esta clase.
- **Cómo se midió:** TERCERA transición de la Fase 1 (2026-08-31), brazo adversario del oráculo
  sobre una copia aislada; el mutante representativo **re-verificado a mano** por el orquestador:
  `bash tools/verify.sh` → `rc=0`. Control positivo del arnés hecho: invertir `vaciariaElLibro`
  SÍ muere (rc=2), o sea que el estímulo llega y el oráculo muerde cuando puede.
- **Segundo pintor que DECIDE, destapado por la revisión adversaria del PLAN 01-05 (2026-08-31):**
  `setSyncUI` lleva dentro toda la cascada de estados con sus colores. Mutar su rama de error para
  pintar el verde `#27ae60` es literalmente «un fallo de sincronización pintado en verde» —el daño
  que da nombre al ciclo— y **hoy no lo mide nada**: la matriz comprueba el `aviso` que DEVUELVE el
  juez, no lo que el pintor HACE con él, y `cloudwrites.py` sólo prohíbe el literal
  `setSyncUI('ok')`. El arreglo tiene que cortar por el mismo sitio en los DOS pintores.
- **La duración no vive en el elemento:** vive en el `setTimeout` del aviso. Un espía que registre
  lo escrito en el elemento **no puede leerla**, así que ese mutante exige un reloj falso (§5.12),
  no un espía de pantalla.
- **Estado:** **CERRADA** en el ciclo **01-06** (2026-08-31), por la CLASE y no por los casos.
  Lo que la cierra, cada pieza con su mutante en `tools/sabotage.py`:
  - **Los dos pintores se EJECUTAN de verdad** sobre un DOM observable con reloj falso, dentro de
    una ventana que se retira en un `finally` idempotente. Ya no se les sustituye por espías, que
    era el agujero. Se afirma el color **por su valor**, la **visibilidad** y la **duración**.
  - **El `aviso` del juez de subida** entra en las 84 filas de la matriz, con oráculo escrito
    aparte: ninguna rama de rechazo puede devolver el aviso de éxito.
  - **`tools/avisos.py`**, cableado a la puerta, con dos redes disjuntas: por RECEPTOR (nadie toca
    los elementos del aviso fuera de los pintores) y por CANAL (los **34** avisos al operador
    sellados con su nivel y su prefijo literal, cada uno con su motivo escrito).
- **Lo que costó cerrarla de verdad:** el ciclo se dio por hecho una vez y **los tres brazos
  adversarios lo demolieron**, cada uno viendo algo que los otros dos no. El peor hallazgo:
  los asertos exigían que los colores de éxito y de fallo fueran **DISTINTOS**, nunca **CUÁLES**,
  así que **intercambiarlos —el fallo pintado en VERDE— salía `rc=0` y «✅ Autopruebas OK»**. Es
  literalmente el daño que nombra esta ficha, vivo dentro del ciclo escrito para matarlo: mi
  oráculo heredó mi punto ciego (§5.8). Otros tres del mismo grupo: el error de sincronización en
  naranja, un aviso de **2 milisegundos**, y el detector de cesión de control pasando con el
  mecanismo **borrado** (§5.1).
- **Qué la reabre:** que aparezca cualquier aviso al operador sin entrada sellada en
  `.paul/baseline-avisos.json`, o cualquier propiedad del aviso que el operador MIRA —color,
  texto, visibilidad, duración, nivel— sin un mutante que la mate. **No basta con que exista un
  aserto: tiene que haberse visto rojo.**

---

## Cerradas en el ciclo 01-04 (2026-08-30)

### D-33 · Una tercera escritura a la nube esquivaba la guarda de no-vaciado — CERRADA 2026-08-30
- **Qué era:** tres escrituras al documento de Firestore y sólo dos pasaban por el juez. La
  tercera vivía en el manejador de inicio de sesión y se recorría también cuando la lectura de la
  nube **fallaba**, porque su `catch` devolvía `false`, indistinguible de «arriba no hay nada».
- **Cómo se cerró (ciclo 01-04):** se cerró la CLASE, no los tres casos. Ahora existe **una sola
  función con una escritura a la nube** (`subirALaNube`), quien decide es la función pura
  `decidirSubida`, y la nube es un **tri-estado explícito** (`con-datos` / `vacia` / `ilegible`)
  más un cuarto caso (`no-consultada`): la distinción que se perdía al colapsarla en un booleano
  es exactamente la que causaba el daño. El juez **falla CERRADO de forma simétrica**: si para
  decidir hace falta mirar la nube y no se pudo mirar, no se sube — para las operaciones **y**
  para los activos.
- **Qué lo demuestra mañana:** `tools/cloudwrites.py`, cableado como paso de `tools/verify.sh` en
  el mismo commit, con **dos redes disjuntas** (por el receptor y por el método) que se ponen
  rojas si aparece una CUARTA escritura. No es una lista blanca: los enlaces a Firestore se
  DERIVAN del código, y el instrumento da rc=2 si no consigue derivar ninguno. Más los sabotajes
  «aparece una cuarta escritura a la nube fuera de la puerta» y «el manejador de inicio de sesión
  vuelve a escribir por su cuenta» (control positivo literal de esta ficha), y las 84 filas de la
  matriz de `decidirSubida`.

### D-34 · Dos `catch` vacíos en la función que construye lo que se sube — CERRADA 2026-08-30
- **Qué era:** `buildSyncPayload` se tragaba con `catch {}` el fallo de leer una cartera, la
  omitía del paquete, y como `ref.set` **reemplaza el documento entero**, la borraba de la nube.
- **Cómo se cerró (ciclo 01-04):** `buildSyncPayload` devuelve `{ payload, incompleto }` y NOMBRA
  las claves que no pudo leer; la subida se rechaza con ese motivo y el indicador no se pone
  verde. Decisión declarada: un fallo en el histórico bloquea igual que uno en los activos, porque
  el histórico **no es reconstruible** y omitirlo lo borraría de la nube.
- **Qué lo demuestra mañana:** `tools/emptycatch.py`, cableado a la puerta, con foto sellada que
  **nombra uno a uno** los `catch` vacíos tolerados y **cero tolerados en el camino de subida**.
  Cuenta las DOS variantes (`catch (e) {}` y `catch {}`): contar sólo una ERA el defecto. Más tres
  sabotajes: el del censo, el del **eslabón productor** (una clave corrupta sembrada en el
  almacenamiento, que exige que el paquete la nombre) y el del **cable** entre productor y juez.
- **Corrección de una cifra publicada:** el censo del acta anterior decía 6 `catch` vacíos. Con el
  instrumento —que además ignora los que sólo aparecen en comentarios— la cifra real es **5**, y
  vive en `.paul/baseline-catches.json`, no copiada aquí.

### D-31 · El indicador de sincronía se pintaba VERDE después de un error — CERRADA 2026-08-30
- **Qué era:** el `catch` del manejador de inicio de sesión hacía `console.error` y después ponía
  el punto en verde. Era la fábrica de silencio que hacía invisible a D-33.
- **Cómo se cerró (ciclo 01-04): por la CLASE, no por el caso.** La ficha nombraba un `catch`,
  pero había **dos miembros más vivos**: el callback de error del `onSnapshot` era `() => {}` —el
  escucha moría y el punto seguía verde— y el arranque pintaba verde incondicionalmente,
  borrando un naranja o un rojo legítimos. Hoy hay **cero llamadas literales** que pinten verde:
  el verde sólo se alcanza por `estadoSync(resultado)`, un mapa CERRADO donde lo desconocido da
  ROJO. Se añadió el estado `error` al indicador, con mensaje propio: reutilizar el de
  autenticación habría mentido sobre la causa.
- **Qué lo demuestra mañana:** la comprobación del aviso en `tools/cloudwrites.py` (cero verdes
  escritos a mano), y tres sabotajes: «un resultado desconocido vuelve a pintar verde», «el fallo
  del inicio de sesión vuelve a declararse verde» y «el manejador deja de pintar el indicador»
  —este último porque el valor de retorno seguía siendo correcto y nadie miraba si además se
  pintaba: cubrir el mecanismo no cubre su cableado.

---

## Cerradas ANTES de este ciclo

### D-00 · Un número tecleado con coma se multiplicaba por mil — CERRADA 2026-08-29
- **Qué era:** `parseNum` aplicaba una heurística de miles y leía `0,123` como `123`. Afectaba a
  títulos, precios y a la edición de operaciones importadas, o sea al FIFO y al Excel del IRPF.
- **Cómo se midió:** reproducido ejecutando el código real fuera del navegador antes de tocarlo.
- **Cómo se cerró:** revisión `69f728e`. En la entrada de teclado el último separador es el
  decimal; la heurística de miles se quedó sólo en el camino del OCR.
- **Qué la reabriría:** el invariante está en `runSelfTests()` y hay un sabotaje permanente que
  lo verifica. Si `tools/sabotage.py` deja de morder ahí, esta deuda vuelve a estar abierta.

### D-12 · Los identificadores de operación colisionaban dentro de un extracto — CERRADA 2026-08-29
- **Qué era:** `genOpId` mezclaba la marca de tiempo con tres caracteres aleatorios, y un extracto
  entero se importa dentro del mismo milisegundo: sólo 46.656 valores distinguían las operaciones.
- **Cómo se midió:** ejecutando el generador real, 2026-08-29: **10,2 % de los extractos de 100
  operaciones tenía al menos una colisión**. El sufijo aleatorio sí tenía siempre 3 caracteres
  (200.000 muestras); la causa era el problema del cumpleaños, no la longitud.
- **Cómo se cerró:** ciclo 01-02 (`77f8cef`). Un contador monotónico de ancho fijo, detrás de la
  marca de tiempo y delante del azar, hace imposible que dos llamadas coincidan. El ancho es fijo
  porque el identificador es el desempate al ordenar el FIFO.
- **Residuo conocido:** los identificadores ya guardados NO se migran, así que las colisiones
  históricas siguen en disco. Por eso la deduplicación del sync exige identificador **Y** huella:
  una colisión de fábrica no puede comerse una operación legítima.
- **Qué la reabriría:** hay autoprueba (mil ráfagas de 500 identificadores) con su control positivo
  —el generador viejo tiene que seguir colisionando— y un sabotaje permanente. Si `tools/sabotage.py`
  deja de morder en «los identificadores vuelven a poder chocar», esta deuda vuelve a estar abierta.
