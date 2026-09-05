# Fase 1 — QUINTA transición · medición contra el código

**Fecha:** 2026-09-05 · **Revisión medida:** `50c0ac4` (HEAD), árbol limpio
**Huella de `index.html`:** `9459b0fc3b40a50a38d0c506fec2b862`, idéntica al empezar y al terminar,
comprobada seis veces durante la sesión.
**Puerta al empezar:** `bash tools/verify.sh` → **rc=0**, **once pasos**, «VERDE — todo ejercido y
en verde». El árbol quedó byte a byte igual.

## Veredicto

> ## 🔴 La FASE 1 **NO** cierra. Abre el ciclo **01-08**.

Los tres objetivos del ALCANCE siguen en PASS. La **META** no: hay un camino de arranque,
**reproducido ejecutando y re-verificado por el orquestador**, que acaba **borrando 40 de 42
operaciones en la nube con la pantalla en verde**; y la capa de aviso del camino de nube tiene
**mutantes vivos** que dejan pintar en verde un fallo de sincronización con la puerta entera en
rc=0.

Es la **quinta vez consecutiva** que medir cambia el resultado. `PLAN == SUMMARY` habría cerrado
la fase las cinco veces.

## Método

G7 (radio de impacto) sigue **DEGRADADO** — `code-review-graph` no ve el JS dentro de un `.html`
(**D-22**). Se sustituyó por **cinco brazos adversarios disjuntos**, cada uno con **una frase
concreta que demoler**, **cada uno sobre su propia copia del proyecto**, con prohibición escrita
por lo que EJECUTAN (no sólo por lo que editan), según la regla que dejó la cuarta transición.

Control de fidelidad antes de medir: las cinco copias reprodujeron la huella exacta de
`index.html` y la puerta en rc=0.

| Brazo | Frase a demoler | Resultado |
|---|---|---|
| A · caminos de pérdida | «ningún fallo de guardado ni de arranque empobrece el libro sin que el operador se entere» | **DEMOLIDA — 1 grave nuevo, reproducido** |
| B · calidad del oráculo | «toda guarda de la meta tiene un control que muere si se revierte» | **DEMOLIDA — 12 de 79 mutantes sin oráculo** |
| C · cableado e instrumentos | «los once pasos están cableados, ninguno falla en verde, las dos variantes ejercen lo mismo» | **DEMOLIDA — 5 hallazgos, 2 graves** |
| D · documentos contra evidencia | «lo que los documentos afirman es cierto y toda cifra se re-deriva» | DEMOLIDA en parte (2 cifras falsas, 1 estado atrasado) |
| E · deudas re-medidas | «el libro de deudas describe el estado real del código» | **DEMOLIDA — 1 deuda mal clasificada, 3 fichas inexactas** |

**Novedad respecto a las cuatro transiciones anteriores:** por primera vez **los cinco brazos
demuelen su frase**, y por primera vez el brazo de mutación encuentra un **bloque entero sin
oráculo** en vez de supervivientes sueltos.

## Los tres objetivos del ALCANCE — PASS

| Objetivo | Resultado | Evidencia medida hoy |
|---|---|---|
| Cargar `ops` incondicionalmente al arrancar, fuera del `if` de META | **PASS** | `ops = loadOpsAll()` es la primera sentencia de `initPortfolios`, antes del `try` de META. Mutante `carga condicional`: muere |
| Los `catch` vacíos de guardado avisan en la UI en vez de decir «Guardado ✓» | **PASS en `guardarTodo`**, con la salvedad T5-3 | `guardarTodo` sólo canta victoria con las tres escrituras bien; G1/G3/G4/G5/G6 mueren con mensaje nominal |
| `applySyncPayload` deduplica por `id`, nunca por huella | **PASS** | `dedupeOpsById` en la rama del formato nuevo; `dedupeOps` sólo en la antigua, por decisión del 01-03. D1/D2/D3 mueren |

## Hallazgos

### 🔴 T5-1 · Un libro de la nube que NO CABE adelanta el reloj, y el siguiente guardado lo exporta encima
**Reproducido por el brazo A y RE-VERIFICADO POR EL ORQUESTADOR ejecutando su reproductor.**

Camino: arranque → `pullFromFirestore` → `applySyncPayload`. La nube trae un documento más nuevo
con 42 operaciones; en local hay 2 y el almacenamiento del navegador no admite el libro grande.
`saveOpsAll(entrante)` falla, lo cuenta **sólo por `console.error`** — y la función **sigue**:
escribe META con el `savedAt` del documento, recarga el libro VIEJO del disco y devuelve `true`.

Salida literal de la re-verificación:

```
consola: ["No se pudo guardar el libro de operaciones: QuotaExceededError (simulada)…",
          "No se pudo guardar el libro recibido de la nube."]
disco=["o1","o2"] META.savedAt=9000 memoria=["o1","o2"]
guardarTodo=true save="Guardado ✓" var(--green)
subida={"subido":true,"aviso":"ok","motivo":"ok"} nube ahora tiene 2 ops (tenía 42)
pantalla={"dot":"#27ae60","dotTitle":"Sincronizado"}
```

**El dispositivo se cree al día sin estarlo, y en el primer guardado exporta su libro pobre sobre
el rico.** La pérdida no es local: es en la nube, que es de donde sale la declaración de la renta.
Y el otro dispositivo, al arrancar, verá ese documento como más nuevo y adoptará el libro de 2.

**La puerta no lo ve:** rc=0. Lo único vigilado es el TEXTO de la consola (borrarlo da rc=1 por el
censo de avisos); el MECANISMO —adelantar el reloj y devolver `true` con el libro sin aterrizar—
**no tiene oráculo**. Ficha nueva: **D-58**.

### 🔴 T5-2 · La capa de aviso del camino de NUBE no tiene oráculo: ocho mutantes vivos
**Medido por el brazo B (79 mutantes) y RE-VERIFICADO POR EL ORQUESTADOR en tres casos, con
ancla única afirmada antes de mutar.**

`subirALaNube` es la única función que escribe a la nube, y **nada mide lo que PINTA**:

| Mutante re-verificado | rc | Veredicto |
|---|---|---|
| **U8** · la escritura que falla se pinta **VERDE** (devolviendo `error`) | **0** — «VERDE — todo ejercido y en verde» | **VIVO** |
| **U3** · la subida omitida por el juez se pinta **VERDE** | **0** — «VERDE — todo ejercido y en verde» | **VIVO** |
| **U9** · la escritura que falla devuelve `subido: true` | **1** — «AC-3 una escritura que lanza no acaba en verde: esperaba error, obtuve ok» | **MUERTO** |

**Corrección al brazo B, medida:** reportó U9 como vivo y **no lo está**. Lo que sobrevive es
pintar, no devolver. La distinción importa: el control existente mira el VALOR DEVUELTO, y el
operador mira la PANTALLA. Son dos cosas distintas y sólo una está medida.

Otros vivos del mismo bloque, no re-verificados uno a uno: la escucha de Firestore que **muere**
se pinta en verde (E7); el texto del estado de error puede decir «Sincronizado con tu cuenta.» con
el punto rojo (T5); un documento con `portfolios: []` se declara sincronizado sin aplicar nada
(B5); y el motivo del aviso naranja sigue sin control en la subida y en la escucha (U2, E2 —
confirma **D-56** ejecutando, no heredando).

Causa común: las pruebas del camino de subida **cuentan escrituras, no pintadas**; el espía del
pintor se montó para el arranque y la escucha y nunca para `subirALaNube`. Ficha nueva: **D-59**.

### 🔴 T5-3 · Cambiar o crear una cartera pinta «Guardado ✓» en VERDE con la escritura fallida
**Medido por el brazo E y RE-VERIFICADO POR EL ORQUESTADOR ejecutando su reproductor.**

Salida literal:

```
switchPortfolio: memoria currentPortId= B | disco currentPortId= A
D-48 switchPortfolio con saveMeta fallido → pintado: [{"t":"Guardado ✓","ok":true}] | subidas: 0
D-48 addPortfolio  con saveMeta fallido → pintado: [{"t":"Guardado ✓","ok":true}] | subidas: 0
D-48 deletePortfolio: rows-B borrado del disco, META en disco sigue listando B
```

`saveRows()` con anuncio va ANTES de `saveMeta()`, así que el verde se pinta antes de saber si la
lista de carteras entró. **Es exactamente la categoría de D-27**, que el 01-07 cerró para el libro
y quedó viva aquí. No sube a la nube (0 subidas en los cinco llamantes), así que no toca el libro
de operaciones — por eso es un verde falso y no una pérdida del libro. Sin oráculo: quitar el
`saveMeta()` de `switchPortfolio` deja la puerta en **rc=0**.

**D-48 estaba MAL CLASIFICADA** («cambio sin una palabra»): la mitad de sus llamantes no callan,
**mienten en verde**. Se reescribe su ficha.

### 🔴 T5-4 · El censo de avisos AMNISTÍA en silencio una alarma que desaparece
**Medido por el brazo C y RE-VERIFICADO POR EL ORQUESTADOR, con ancla única afirmada.**

Cerrada la boca `console.error('No se sincroniza: el guardado local falló.')`:

```
$ python3 tools/avisos.py --check
HALLAZGO (rc=1): han DESAPARECIDO avisos que la foto sellaba.
   - guardarTodo|error|No se sincroniza: el guardado local falló.  (1 -> 0): ha desaparecido
   Una boca que se cierra es el silencio que esta fase existe para impedir.
   … No se resella de tramite.
rc=1

$ python3 tools/avisos.py --update          # SIN --amnesty
Foto sellada: 39 aviso(s) en 39 claves.
rc=0                                         # ← la sella, en silencio, sin nombrarla

$ python3 tools/avisos.py --check
Capa de aviso sin cambios… rc=0              # ← verde para siempre
```

Es la trampa de §4.4 **dentro del instrumento escrito para impedirla**: `--check` la trata como
hallazgo, pero `sellar` sólo se niega ante `peor`, y la desaparición se clasifica como `mejor`.
Dos predicados distintos sobre el mismo conjunto (§5.16). El ciclo 01-06 decidió por escrito que
«un aviso que DESAPARECE es un HALLAZGO, no una mejora» y lo cerró **sólo por el lado de
`--check`**. `tools/sumideros.py` NO tiene el defecto: ahí la boca cerrada va a `peor` y `--update`
se niega. Ficha nueva: **D-61**.

### 🟠 T5-5 · Un `index.html` que no decodifica sale como rc=1 «hallazgo del código», no rc=2
Medido por el brazo C, no re-verificado por el orquestador. Los **siete** instrumentos Python
mueren con `UnicodeDecodeError` sin capturar: traceback y **rc=1**. Es §4.3 literal: instrumento
roto disfrazado de hallazgo, que manda a mirar el código en vez de las herramientas. Las fotos
selladas, en cambio, sí fallan cerrado ante el mismo byte. Ficha nueva: **D-62**.

### 🟠 T5-6 · El cable del guardado a la subida puede cortarse en verde
`schedulePush` puede dejar de llamar a `subirALaNube` con la puerta en **rc=0**: las pruebas
**reasignan** `schedulePush` para contar llamadas, así que su cuerpo nunca se ejerce (§5.6). La
app dejaría de sincronizar en silencio, con el punto verde tras cada guardado. Ficha nueva:
**D-60**.

### 🟠 T5-7 · Reglas de medida que viven FUERA de la semántica sellada
Quitar `'delete'` de los mutadores de `cloudwrites.py`, o dejar que `emptycatch.py` no vea un
`catch {}` desnudo, deja pasar el daño correspondiente con **rc=0**: sin foto, sin deriva y sin
sabotaje que lo cace. Ficha nueva: **D-63**.

### 🟠 T5-8 · `hookcheck` da verde a un enganche que git no puede ejecutar
Con el enganche en CRLF, `hookcheck` dice «idéntico» y `git push` falla con
`/usr/bin/env: 'bash\r'`. Falla cerrado por git, pero el instrumento certifica lo contrario.
Ficha nueva: **D-64**.

### 🟠 T5-9 · Los censos son ciegos a un sumidero escrito de otra forma
Un pintor por `querySelector`, una id en variable, un nombre partido (`window['schedule'+'Push']`)
o una subida por REST pasan los tres censos con **rc=0**. Sí cazan `.call`, `.apply`,
`window['schedulePush']`, la desestructuración y los alias directos. Amplía **D-49**, cuya ficha
además afirma una ceguera que **hoy es falsa** (`schedulePush.call(null)` da rc=1, no rc=0).

### 🟡 T5-10 · Cuatro mutantes que la puerta caza por ACCIDENTE del banco
G2, L6, E2 y J3 ponen la puerta roja con «BANCO ROTO: ancla no única», **no porque ningún control
muerda**: con el banco omitido dan rc=4 verde. El mensaje **dirige la mano al sitio equivocado**
(arreglar el banco, no el código). Entre ellos, G2: perder `okRows` del veredicto de `guardarTodo`
no tiene autoprueba propia. Entra en **D-59**.

### 🟡 T5-11 · Caminos de pérdida menores, reproducidos por el brazo A
- **Activos ilegibles al arrancar** se leen como vacíos, sin consola ni rescate, y el primer
  guardado los sobrescribe con `[]` en verde. Asimetría con `loadOpsAll`, que sí rescata (§5.16).
  Ficha **D-66**.
- **El naranja de empate sale tras CADA sincronización correcta** (el eco del propio documento),
  con el mismo texto con el que T5-1 disfraza una pérdida real. Un aviso que salta siempre enseña
  a ignorarlo. Ficha **D-67**.
- **Dos pestañas sin sesión** se pisan el libro con «Guardado ✓» en las dos; con sesión y red
  resiste, porque el eco repara. Ficha **D-68**.
- **El punto verde persistente no se apaga** tras un guardado local fallido: el rojo dura 5 s y el
  estado durable sigue diciendo «Sincronizado». Ficha **D-69**.
- **Carrera arranque/sesión**: si la sesión de Firebase se resuelve antes del evento `load`, el
  juez de bajada no tiene nada que proteger y una nube más vieja pisa el libro. El mecanismo está
  reproducido; **el orden real en el navegador NO está medido**, y el reproductor se colgó al
  re-verificarlo. Ficha **D-65**, con su medición pendiente como primer paso.

### 🟡 T5-12 · Documentos
- **D-54 repite el defecto de forma de D-38**: su campo dice `Estado: CERRADA` y vive bajo
  `## Abiertas — limpieza`. La lección se escribió en la cuarta transición y no lo evitó (§5.17).
- **`PROJECT.md` está un ciclo entero atrás**: describe el estado tras la cuarta transición y no
  menciona el 01-07. De los cuatro sitios del estado, sólo él quedó sin actualizar.
- **`ROADMAP.md`** tiene el cuerpo al día y el pie con fecha vieja.
- **`CLAUDE.md` §4.2 enumera 6 pasos de la puerta; la puerta tiene 11.**
- **La ficha D-49 afirma una ceguera falsa** (ver T5-9).

## Lo que RESISTIÓ — para que esto no sea un panel que refuta todo

- **Las cinco deudas que cerró el 01-07 están BIEN CERRADAS**, re-medidas revirtiendo el arreglo:
  D-45 (tres reversiones distintas, todas rc=1), D-46, D-27, D-30 y D-29, cada una con su mensaje
  nominal. Ninguna se cerró de palabra.
- **67 de 79 mutantes mueren** con mensaje nominal, incluidos los de `decidirBajada` (8 de 9), la
  matriz del juez de subida, el cerrojo del libro ilegible, la deduplicación por identificador y
  el paso del motivo en el arranque y en la bajada.
- **Fallo cerrado**: fotos ausentes, corruptas, con tipo equivocado o sin semántica ⇒ **rc=2 con
  nombre y remedio** en las cuatro. `node` ausente, `ruff` ausente, `git` ausente ⇒ DEGRADADO.
- **Deriva**: quince cambios de regla de medida ⇒ **rc=3 siempre, y ninguno imprime el comando de
  resellado**.
- **Delta mixto** en `funcsize`, `emptycatch` y `sumideros`: **gana el empeoramiento**, `--update`
  se niega y `--amnesty` enumera lo amnistiado.
- **Las dos variantes ejercen lo mismo**: el enganche instalado es byte a byte el del instalador;
  `VERIFY_INNER=1` exportado no se cuela y con `BASH_ENV` el push queda bloqueado con rc=4.
- **118 sabotajes muerden** — cifra **re-derivada hoy por el orquestador** en copia limpia, con el
  árbol idéntico antes y después. Un brazo publicó 119: **es falsa**, la buena es 118.
- **`--check` nunca escribe**: hash idéntico en los cuatro trinquetes.

## Nota de proceso — la regla de la copia funcionó, y aun así se rompió por un sitio nuevo

Un brazo dejó **dos ficheros suyos sin rastrear dentro del repositorio real** (`reverts.sh`,
`reverts.log`): una llamada en segundo plano arrancó con el directorio de trabajo reseteado al
repo. **`index.html` no se tocó** —el script sólo lo leía para copiarlo a su laboratorio, y su
huella se mantuvo en `9459b0fc…` durante toda la sesión—, y el propio brazo los retiró al
detectarlo. Otros dos brazos lo reportaron por su cuenta comparando el estado del árbol.

La lección nueva, que va a `CLAUDE.md`: **la prohibición se cumplió y aun así hubo escritura**,
porque el directorio de trabajo de un proceso en segundo plano puede no ser el que el brazo cree.
👉 Regla: un brazo no sólo tiene prohibido escribir en el árbol real; **sus scripts deben fijar su
directorio de trabajo de forma absoluta y afirmarlo antes de escribir nada**. Y el control que lo
destapó —comparar el estado del árbol al empezar y al terminar— vuelve a ser el que funciona.

Otro brazo mató a mitad un sabotaje **dentro de su propia copia** y lo restauró él mismo. Es la
prueba de que trabajar sobre copia convierte un incidente grave en uno intrascendente.

## Qué abre el ciclo 01-08

**Objetivo:** que el camino de la NUBE no pueda pintar verde sobre un fallo, y que un libro
entrante que no aterriza no pueda adelantar el reloj ni exportarse encima.

1. **T5-1 / D-58** — que `applySyncPayload` no adelante la marca de tiempo si el libro entrante no
   se pudo escribir, y que lo diga en pantalla. Cerrar la **clase**: ninguna escritura fallida
   durante la aplicación puede acabar en un estado que se declare al día.
2. **T5-2 / D-59** — montar el espía del pintor sobre `subirALaNube` y sobre el callback de error
   de la escucha, y afirmar el color y el TEXTO por su valor en las dos ramas de fallo. Cerrar por
   **receptor**, no enumerando los tres casos conocidos (§5.15).
3. **T5-3 / D-48** — que el anuncio de éxito de los llamantes de la lista de carteras dependa del
   resultado de su escritura. Misma clase que D-27, cerrada para el libro y viva aquí.
4. **T5-4 / D-61** — que `avisos.py` se niegue a sellar una boca que desaparece, como ya hace
   `sumideros.py`. Es un hueco del aparato de medición y va dentro del ciclo, no diferido.

**Fuera de alcance del 01-08, fichado y dicho por escrito:** la carrera de arranque (D-65, primero
hay que medir el orden en el navegador); la fusión de `ops` por `id` y la política de quién gana
(D-01, D-51, D-57, Fase 3); los instrumentos de T5-5 a T5-9 salvo D-61; y los caminos menores
D-66 a D-69.

## Correcciones aplicadas en este mismo commit

- **D-54** movida a la sección de cerradas: su ubicación contradecía su estado.
- **D-48** reescrita: de «cambio sin una palabra» a **verde falso**, con la medición de hoy.
- **D-49** corregida: la ceguera que afirmaba es falsa; se sustituye por la real (T5-9).
- **D-18**, **D-56** y **D-50** actualizadas con lo que el código hace hoy.
- **D-01** pasa a REPRODUCIDA, con sus dos nuevas puertas de entrada.
- Fichas nuevas: **D-58** a **D-69**.
- `PROJECT.md` puesto al día; pie de `ROADMAP.md` corregido.
- `CLAUDE.md`: la puerta tiene once pasos, y la regla nueva sobre el directorio de trabajo de los
  brazos.
