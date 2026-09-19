# Fase 1 — SEXTA transición · medición contra el código

**Fecha:** 2026-09-19 · **Revisión medida:** `3a7a54e` (HEAD), árbol limpio
**Huella de `index.html`:** `64e6e29462fc48b4d7876b14bf514b07`, idéntica al empezar y al terminar,
en el árbol real y en las cinco copias. La misma que sirve GitHub Pages (medido por el brazo D con
`curl`).
**Puerta al empezar:** `bash tools/verify.sh` → **rc=0**, **once pasos**, «VERDE — todo ejercido y
en verde». El árbol quedó byte a byte igual.

## Veredicto

> ## 🔴 La FASE 1 **NO** cierra. Abre el ciclo **01-09**.

Los tres objetivos del ALCANCE siguen en PASS. La **META** no, por dos motivos medidos:

1. **El freno del 01-08 no sobrevive a una recarga cuando no se pudo escribir en disco** —que es
   justo el caso para el que existe, el almacenamiento lleno—, y entonces **D-58 vuelve entera:
   42 operaciones → 2 en la nube, con el punto VERDE**. Reproducido por el brazo A y
   **re-verificado por el orquestador** en copia propia.
2. **El naranja de empate (D-67) es el mismo punto y el mismo título que el aviso real de riesgo**,
   y sale tras cada sincronización correcta. En el camino del punto 1, el único aviso previo a la
   pérdida es precisamente ese naranja que el operador ya ha aprendido a ignorar.

Y un tercero, de oráculo: **12 mutantes que rompen comportamiento real pasan la puerta entera en
`rc=0`**, entre ellos los cables del freno en sus dos llamantes y la restauración de las filas
en los llamantes de carteras.

Es la **sexta vez consecutiva** que medir cambia el resultado. `PLAN == SUMMARY` (8 y 8) habría
cerrado la fase las seis veces.

## Método

G7 (radio de impacto) sigue **DEGRADADO** — `code-review-graph` no ve el JS dentro de un `.html`
(**D-22**). Se sustituyó, como en las cinco anteriores, por **cinco brazos adversarios disjuntos**,
cada uno con **una frase concreta que demoler**, **cada uno sobre su propia copia**, con la
prohibición escrita por lo que EJECUTAN, directorio de trabajo fijado en absoluto y afirmado, y
huella + `git status` del árbol real al empezar y al terminar.

| Brazo | Frase a demoler | Resultado |
|---|---|---|
| A · caminos de pérdida | «tras el 01-08, ningún fallo de guardado, arranque o aplicación de la nube empobrece el libro —en disco o en la nube— sin que se vea» | **DEMOLIDA — 1 grave, re-verificado** |
| B · calidad del oráculo | «toda guarda que el 01-08 añadió o tocó tiene un control que muere si se revierte» | **DEMOLIDA — 12 de 81 mutantes vivos con defecto real** |
| C · cableado e instrumentos | «los once pasos están cableados, ninguno falla en verde, rc nominales, las dos variantes ejercen lo mismo» | **RESISTE** |
| D · documentos contra evidencia | «lo que afirman los documentos es cierto y toda cifra se re-deriva» | DEMOLIDA en parte (`PROJECT.md` un ciclo atrás, por segunda vez) |
| E · deudas re-medidas | «el libro de deudas describe el estado real» | RESISTE en las cerradas; **agrava D-67** |

## Los tres objetivos del ALCANCE — PASS

No se tocaron desde la quinta transición; el brazo C y el E corrieron la puerta completa fresca en
sus copias (rc=0) y las autopruebas que los cubren siguen muriendo con sus mutantes.

## Hallazgos

### 🔴 T6-1 · El freno que no pudo escribirse no sobrevive a la recarga, y la nube pierde el libro en VERDE
**Brazo A, y RE-VERIFICADO POR EL ORQUESTADOR** en copia propia (`scratchpad/reverif/food`),
reconstruyendo el ejecutor desde `index.html` y corriendo el reproductor del brazo.

Camino: almacenamiento lleno de verdad → `applySyncPayload` no puede escribir el libro (42) →
`armarFreno` tampoco puede escribir META (es best-effort, declarado) → el freno vive **sólo en
memoria** (`libroPendiente`) → **recarga** → `initPortfolios` arranca sin freno → un guardado local
antes de que responda la nube sella la hora actual (la «segunda red» —el reloj que no avanza— mira
la misma variable, así que desaparece a la vez) → la bajada dice `nube-no-mas-nueva` → la subida
exporta el libro pobre.

Salida literal de la re-verificación:

```
OK    sesión 1: el freno NO está en disco (la META no cupo)
OK    recarga: el freno se ha perdido
OK    guardado local tras recargar: dice que fue bien
OK    y la marca de tiempo local AVANZÓ (la segunda red no existe ya)
[SYNC] documento de la nube NO aplicado: documento NO más nuevo (9000 <= 1789807695745) con 2 operaciones locales que proteger
  [pantalla tras la bajada] punto=#e67e22 titulo="Cambios sin subir" | …
OK    subida: SE SUBE
OK    y lo que llega a la nube es el libro POBRE (42 -> ?)      ← 2
  [pantalla tras la subida] punto=#27ae60 titulo="Sincronizado" | estado="Sincronizado con tu cuenta." | guardado="Guardado ✓" (var(--green))
```

**Variante sin carrera (T6-1b)**, misma salida: tras la recarga sin freno, si la lectura de la nube
falla al iniciar sesión, `decidirSubida` sube con la nube `ilegible` porque hay datos locales que
subir, y la nube recibe el libro pobre **sin haberla leído**, en verde.

**Control que resiste:** si el freno SÍ se pudo escribir (sólo falla el libro), la recarga lo
recupera, el reloj no avanza y la subida se frena. El defecto es exactamente «freno sólo en
memoria». El comentario de `armarFreno` («NO es la única red. La otra es que la marca de tiempo no
avanza») es cierto sólo mientras dura la sesión (§5.1).

**Lo que NO está medido:** la ventana real en el navegador (desde `load` hasta la respuesta de la
nube; la abre el primer `schedSave` de 600 ms), ni con qué frecuencia la cuota se llena «de
verdad». El mecanismo sí: reproducido dos veces por dos manos distintas. Ficha **D-74**.

### 🔴 T6-2 · El naranja de empate es el MISMO aviso que el riesgo real
**Brazo E, re-verificado por el orquestador leyendo `setSyncUI` y `desempatePorReloj`.**

`desempatePorReloj` es estricto a propósito (`remoto > localSaved`, comentado: con `>=` volvía un
defecto del 01-08), así que el empate —el estado NORMAL tras sincronizar— cae en `pendiente` con
clave `nube-no-mas-nueva`. Y `setSyncUI('pendiente', …)` pinta **todas** las claves pendientes con
el mismo punto `#e67e22` y el mismo título «Cambios sin subir»; sólo cambia el texto largo, que va
oculto tras el punto. Entre esas claves está `nube-pendiente`, el freno real de D-70.

Consecuencia medida en T6-1: **el único aviso que precede a la pérdida es este naranja**, que el
operador ve tras cada sincronización correcta (confirmado en su navegador el 2026-09-06). Ya no es
«un aviso que salta siempre»: es **la máscara concreta de una pérdida reproducida**. **D-67** sube
de limpieza a meta.

### 🔴 T6-3 · Doce mutantes con defecto real pasan la puerta entera en `rc=0`
**Brazo B: 81 mutantes válidos, 62 mueren con mensaje nominal, 16 viven (12 con defecto real, 4
equivalentes), 3 cazados sólo por accidente del banco.** Re-verificados por el orquestador en
copia propia, con ancla única afirmada y huella restaurada: **F09, C02 y A07 → `rc=4`
«VERDE, PERO EL BANCO NO CORRIO»** (la variante interior: autopruebas e instrumentos verdes).
Una primera versión de mi A07 rompió la sintaxis (`rc=1` por «sintaxis de index.html»): el
defecto era mío, se rehizo con un ancla de sentencia completa.

| Familia | Mutantes vivos | Qué queda sin oráculo |
|---|---|---|
| **Cables del freno en los llamantes** | F09 (arranque), F08 (escucha), F04, F05 (la escucha no suelta el freno), F15 (recuperar el freno sólo si hay carteras) | El freno se prueba en el JUEZ (`decidirBajada` llamado a mano). Cortar `frenoPuesto: !!d.freno()` → `false` en el llamante reabre el freno permanente de un dispositivo nuevo **con la puerta en verde**. Es D-49 otra vez: el cableado por defecto no lo toca ninguna prueba |
| **Restauración de filas en los llamantes de carteras** | C02 (`switchPortfolio` no restaura `rows`), C12 (`deletePortfolio` en la rama de ÉXITO), y C06 (cazado sólo por accidente) | Pinta rojo y restaura la cartera activa, **pero deja en memoria los activos de la otra**: el siguiente guardado los escribe encima. Las pruebas miran la rama de fallo y sólo borran una cartera no activa (§5.8) |
| **Todo-o-nada** | A07 (falla SÓLO la META y aplicar dice que sí → verde), A11 (reparar el libro ilegible devuelve `true` al fallar), A12 (el formato antiguo devuelve `true`), A20 (tras sincronizar queda una sola cartera) | Nadie prueba «falla sólo la última escritura», ni documentos con más de una cartera |
| **`avisos.py`** | V03b (una foto editada a mano con claves sin motivo pasa `--check`), V01 (la mitad «lo nuevo bloquea» de `--update` sin control propio; mitigado por el `--check` siguiente) | Instrumento; no daña el libro |

Fichas nuevas: **D-76** (cables del freno), **D-77** (filas de los llamantes), **D-78**
(todo-o-nada), **D-79** (`avisos.py`).

### 🟠 T6-4 · Con META corrupta al recargar, el freno se pierde y el reloj renace por delante
**Brazo A, no re-verificado por el orquestador.** `initPortfolios` lanza antes de leer `pendiente`
y `createDefaultPortfolios` sella una hora nueva y `pendiente: null` encima. La prueba
`pruebasFrenoNoEsPermanente (2)` mide el juez con `frenoPuesto: true, savedAt: 0`, no la cadena
real (§5.8). Con la nube con activos (lo realista) no hay pérdida —la guarda de activos frena la
subida— pero el dispositivo queda atascado sin freno, con la nube inaplicable para siempre y un
aviso que no nombra la causa. Sin activos en la nube: pérdida en verde. Misma familia que T6-1:
entra en **D-74**.

### 🟡 T6-5 · La escucha suelta el freno con `exists: false` sin pintar nada
**Brazo A; mecanismo reproducido, estímulo no medido** (si el SDK con persistencia puede entregar
un snapshot `exists: false` por fallo de caché sin red). La pantalla sigue diciendo «la nube trae
42 operaciones y no caben» con el freno ya suelto. Ficha **D-75**.

### 🟡 T6-6 · Documentos
- **`PROJECT.md` volvió a quedar un ciclo atrás**: narra hasta la quinta transición y no sabe que
  el 01-08 se cerró, se desplegó ni se vio en el navegador. **Reincidente**: el mismo hallazgo de
  la quinta transición (§5.17: escribir la lección no la evita).
- **La métrica «Invariantes cubiertos por `runSelfTests()`: 1 (target 4)»** es de la Fase 0. El
  brazo D la dio por falsa contando 359 `check()`; **esa lectura es incorrecta**: la métrica cuenta
  FAMILIAS (decimal, FIFO, año fiscal, sync), no asertos. Aun así está rancia: decimal y sync ya
  tienen invariante, así que son al menos 2.
- `paul.json` con `updated_at` dormido; pie de `ROADMAP.md` con fecha vieja.

## Lo que RESISTIÓ — para que esto no sea un panel que refuta todo

- **El aparato de medición entero (brazo C, frase no demolida):** once pasos cableados;
  **161 controles del banco, todos muerden** —cifra re-derivada por dos brazos, coincide con la
  publicada—; el enganche instalado es byte a byte el del instalador; fotos ausentes o corruptas
  ⇒ `rc=2` con remedio; `--check` nunca escribe; delta mixto ⇒ gana el empeoramiento; `node` o
  `ruff` ausentes ⇒ DEGRADADO ruidoso; `avisos.py --update` se niega en las dos direcciones y
  nombra la clave. D-53 confirmada tal cual, no agravada.
- **Las cuatro deudas que cerró el 01-08 están BIEN cerradas** (brazo E), revirtiendo su arreglo:
  D-58, D-59, D-48 y D-61, las cuatro `rc=1` con mensaje nominal, dos de ellas con dos o tres
  vigilantes disjuntos.
- **62 de 81 mutantes mueren**, incluidos todo el bloque de la pintura (P01–P25 salvo P08), el
  orden del todo-o-nada, el cable del freno en la SUBIDA (F10), la hora sellada fuera del `if`
  (F13) y la recuperación del freno al arrancar.
- **En la misma sesión el freno resiste** (brazo A): reloj quieto, subida frenada, caso mixto
  coherente, y los cinco llamantes de carteras pintan rojo y deshacen su cambio con la META que no
  cabe.
- **Lo desplegado es lo medido:** huella local = huella servida por Pages.
- **D-60 sigue viva** tal como dice su ficha: cortar la llamada dentro de `schedulePush` da rc=0.

## Nota de proceso — dos brazos rompieron la exclusividad DENTRO de su copia

El brazo C y el brazo E lanzaron el banco de sabotaje en segundo plano y, mientras seguía vivo,
corrieron otra medición sobre **la misma copia** (§5.13). A los dos los delató el control de
huella; el E acabó con su copia a mitad de una mutación (`rc=2` «sintaxis rota») y la restauró
dentro de ella. **El árbol real no se tocó** (huella y `git status` idénticos al terminar, en los
cinco). Trabajar sobre copia convirtió dos incidentes en intrascendentes, otra vez.

Y una segunda: al brazo E **no le llegaban las notificaciones de sus tareas en segundo plano** y se
detuvo dos veces esperando. La regla práctica para los próximos briefs: **los brazos ejecutan en
primer plano** y redirigen a fichero; nada de segundo plano dentro de un brazo.

## Qué abre el ciclo 01-09

**Objetivo:** que el freno de la nube sobreviva a lo que el operador hace de verdad —recargar—, que
el aviso de riesgo real no se confunda con el eco de una sincronización correcta, y que los cables
y restauraciones del 01-08 tengan oráculo.

1. **T6-1 / T6-4 / D-74** — que el freno no dependa de poder escribir la META completa, o que su
   ausencia en disco tras un aplicar fallido se detecte al arrancar. Cerrar la **clase**: tras una
   recarga, un documento que no aterrizó no puede quedar olvidado. Diseño ABIERTO (dónde vive el
   freno cuando el disco está lleno): **dialéctica** en el PLAN.
2. **T6-2 / D-67** — que el empate de relojes tras sincronizar no pinte el aviso de riesgo, y que
   el freno real tenga un aviso distinguible del resto de pendientes.
3. **T6-3 / D-76, D-77, D-78** — oráculo para los cables del freno en los dos llamantes de bajada,
   para la restauración de filas en `switchPortfolio`/`deletePortfolio` (incluida la rama de
   éxito con la cartera ACTIVA), y para «falla sólo la META» y documentos con varias carteras.

**Fuera de alcance del 01-09, fichado y dicho por escrito:** D-75 (estímulo sin medir: primero
medir si el SDK lo entrega), D-79 (`avisos.py`: no daña el libro; se ataca con el siguiente ciclo
de instrumentos), D-60 (sigue su propia ficha), y todo lo de fusión (Fase 3).

## Correcciones aplicadas en este mismo commit

- **D-67** ampliada: máscara concreta de T6-1 y del freno real; sube a meta.
- **D-70** ampliada: el freno tiene criterio de muerte medible **y** criterio de muerte ACCIDENTAL.
- **D-60** re-medida (brazo E): viva.
- Fichas nuevas: **D-74** a **D-79**.
- `PROJECT.md`, `STATE.md`, `ROADMAP.md` y `paul.json` puestos al día.
