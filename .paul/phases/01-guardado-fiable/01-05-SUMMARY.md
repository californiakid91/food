---
phase: 01-guardado-fiable
plan: 05
subsystem: testing
tags: [verify, sabotage, ratchet, git-hooks, exit-codes]
requires:
  - phase: 01-guardado-fiable
    provides: la puerta `tools/verify.sh` y el banco `tools/sabotage.py`
provides:
  - los dos trinquetes fallan CERRADO (rc=2 con nombre y remedio)
  - una semantica de codigos de salida escrita y sellada, con rc=4 reservado
  - el enganche `pre-push` inmune a un entorno contaminado
  - `tools/hookcheck.py`: la variante automatica, vigilada
affects: [01-06, toda fase futura que se mida con esta puerta]
tech-stack:
  added: []
  patterns:
    - "un codigo de salida verde para UN SOLO consumidor, nombrado en la cabecera"
    - "el comprobador deriva lo esperado del instalador, no de una copia pegada"
key-files:
  created: [tools/hookcheck.py]
  modified: [tools/funcsize.py, tools/emptycatch.py, tools/verify.sh, tools/sabotage.py, tools/install-hooks.sh, .paul/DEUDAS.md]
key-decisions:
  - "El rc=4 y el `unset` del enganche son DOS capas, no una"
  - "El vigilante del enganche va DESPUES del banco y fuera de la corrida interior"
  - "`comparar_o_roto` se queda sin oraculo a proposito y se ficha como D-42"
duration: ~1h
completed: 2026-08-31
---

# Fase 1 · Ciclo 05: la vara de medir, arreglada antes de medir con ella

**Ningun instrumento puede ya romperse y salir rotulado como un hallazgo del codigo; la puerta no
puede terminar en verde con el banco apagado, ni por codigo de salida ni por entorno; y la variante
automatica esta vigilada en vez de supuesta. `index.html` no se toco: cero bytes.**

Commit: `4e81e6c`. Cierra **D-39, D-40 y D-41**. Abre **D-42**. Re-mide **D-26**.

## Por que este ciclo fue primero

El 01-06 (la capa de aviso, D-38) se va a medir con esta puerta. Medir un arreglo con una regla de
goma no mide nada: una puerta que puede salir verde sin correr el banco, o que rotula un
instrumento roto como «el codigo ha engordado», habria certificado el 01-06 pasara lo que pasara.

## Condiciones de la medicion de este acta

Todo lo de abajo se ejecuto **en esta sesion, en fresco**, no se hereda del APPLY:

- Arbol **limpio y en exclusiva**: `git status --porcelain` vacio; arbol de HEAD
  `1bd8d35b12c35c70883d445102dac1b978898c3e`.
- `index.html` **byte a byte intacto**: `git show --stat 4e81e6c -- index.html` vacio; blob
  `a2ed63a9765fa5b5e873fbb5dd8c1c1fb04407b2`, md5 `4ff3b0ba79afa7ca1d479ea1525ad51d`.
- **Ninguna foto sellada resellada** — que es la prueba de que los instrumentos siguen midiendo lo
  mismo: este ciclo cambio como FALLAN, no que MIDEN.

## Resultados de los criterios de aceptacion

| AC | Estado | Evidencia (rc y mensaje literales, medidos hoy) |
|---|---|---|
| **AC-1** · un instrumento roto dice «no pude medir», con su nombre | **PASS** | Sobre copia aislada, tres fotos malformadas. `funcsize --check` con `"excede": null` → `rc=2 INSTRUMENTO ROTO: funcsize: la foto sellada baseline-funcs.json: la clave 'excede' es NoneType, se esperaba un objeto`. `emptycatch --check` **y** `--update` con `motivos` de tipo str → `rc=2 INSTRUMENTO ROTO: emptycatch: … la clave 'motivos' es str, se esperaba un objeto`. Sin traceback. Los tres imprimen ademas el **remedio** |
| **AC-2** · un hallazgo real sigue en rc=1, no lo tapa el aviso | **PASS** | Engordada `runSelfTests` en una copia → `rc=1 EL MONOLITO HA ENGORDADO (1 empeoramiento(s)): - runSelfTests: aparece 1 vez/veces excediendo, la foto sellaba 0`. El `except` de la comparacion es estrecho a proposito |
| **AC-3** · «verde sin banco» no es verde, y la tabla esta escrita | **PASS** | `VERIFY_INNER=1 bash tools/verify.sh` → **rc=4**, con mensaje propio: «VERDE, PERO EL BANCO NO CORRIO (rc=4)… Para el operador y para el enganche pre-push, un 4 NO es un verde». Tabla 0/1/2/3/4 en la cabecera de `verify.sh`. Unico consumidor que lo acepta como base: `sabotage.py::puerta()` (linea 70) |
| **AC-4** · el banco sigue vivo tras cambiar el contrato que consume | **PASS** | `python3 tools/sabotage.py` → **rc=0**, «Todos los controles de la puerta muerden». Vacuidad viva y actualizada al contrato nuevo: «control de vacuidad: sin sabotaje, la puerta interior da rc=4». Y **control positivo del propio arreglo**: «sin el `exit 4`, la puerta interior vuelve a dar 0 y la vacuidad lo caza» |
| **AC-5** · el enganche es inmune a un entorno contaminado | **PASS** | Con `VERIFY_INNER=1` **exportado**, `git push --dry-run origin main` → el enganche ejercio los **nueve** pasos, **banco de sabotaje incluido**, y salio «VERDE — todo ejercido y en verde», rc=0. Dos capas: el rc=4 (que ese verde no exista) y `unset VERIFY_INNER` en el enganche (que no lo herede) |
| **AC-6** · la variante automatica esta vigilada, no supuesta | **PASS** | Sobre copia, por camino independiente del banco: enganche borrado → `rc=1 ENGANCHE AUSENTE`; un byte de mas → `rc=1 ENGANCHE DISTINTO`; instalador ausente → `rc=2 INSTRUMENTO ROTO: hookcheck: no existe el instalador…`; copia sana → `rc=0`. Lo esperado se **deriva del heredoc del instalador**, no de una copia pegada |
| **AC-7** · cada control nuevo se ha visto ROJO y el estimulo llego | **PASS** (con una nota, abajo) | Once controles nuevos, todos verdes. `TOCABLES` cubre ahora **once** ficheros —incluidos `verify.sh`, `sabotage.py`, `install-hooks.sh`, `hookcheck.py` y el enganche instalado—, asi que el «arbol identico» prueba algo sobre lo que este ciclo anade. Huella del banco antes = despues: `39474868af25` |

**Las dos variantes de la puerta dan la MISMA salida.** Comparadas linea a linea hoy: la unica
diferencia entre `bash tools/verify.sh` y la corrida del enganche son las dos lineas de `git` sobre
el remoto. Ninguna diferencia en la puerta.

### Nota sobre AC-7 — una debilidad menor, escrita en vez de callada

De los seis mutadores del bloque de `hookcheck`, cinco no necesitan ancla (borran el fichero,
le quitan el bit, le anaden una linea, le cambian los permisos) y `sin_unset` **si** afirma la
unicidad de la suya. El sexto, `sin_heredoc`, sustituye `<<'HOOK'` **sin afirmar que sea unico**.
No es un falso verde: si el ancla no casara, la copia quedaria intacta, `hookcheck` daria rc=0 y el
caso gritaria «NO MUERDE» — falla **ruidosamente**, que es la propiedad que importa (§5.4). Pero es
una desviacion nominal del AC y por eso se escribe aqui y sube al libro de deudas.

## Cifras — re-derivadas hoy, contadas y no recordadas

Todas medidas **despues** del ultimo cambio, con el arbol limpio, no copiadas del APPLY:

| Cifra | Valor | Como se derivo |
|---|---|---|
| Pasos de la puerta | **9** | `grep -c '  OK '` sobre la salida de `verify.sh` |
| Casos en la lista `CASOS` | **46** | importando el modulo y midiendo `len(CASOS)` |
| Mordidas totales del banco | **52** | los 46 anteriores + los 6 del bloque de `hookcheck`, que no caben como `Caso` |
| Controles verdes del banco | **61** | 52 mordidas + 9 controles que no son mordidas |
| De ellos, nuevos en este ciclo | **11** | 2 casos + 6 mordidas de `hookcheck` + 3 controles (vacuidad de hookcheck, control positivo del rc=4, y «la puerta y el instalador siguen siendo ejecutables») |

`CASOS` paso de **44** a **46**, derivado importando las dos versiones del modulo y restando —
no leyendo el diff.

> El mensaje de commit publica estas mismas cifras. Se han vuelto a derivar aqui **por comando**
> antes de copiarlas, precisamente porque la cifra del ciclo anterior («15 sabotajes») eran 14 y
> estaba publicada en tres sitios.

## Lo que se construyo

| Fichero | Cambio | Que hace |
|---|---|---|
| `tools/funcsize.py` | Modificado | `cargar_baseline()` valida el **tipo** de cada clave, no solo su presencia. rc=2 con nombre, clave y remedio |
| `tools/emptycatch.py` | Modificado | Igual, **incluidas las claves que solo lee `--update`** (`motivos`): antes `--check` salia verde con una foto que `--update` no podia leer |
| `tools/verify.sh` | Modificado | Tabla de codigos 0/1/2/3/4 en la cabecera; la variante interior devuelve **4**; paso nuevo del enganche, **despues** del banco |
| `tools/hookcheck.py` | **Creado** (160 lineas) | Compara el enganche instalado contra lo que produce su instalador, derivando lo esperado de su heredoc. Seis desenlaces distinguibles |
| `tools/install-hooks.sh` | Modificado | El enganche **limpia** `VERIFY_INNER` antes de llamar a la puerta |
| `tools/sabotage.py` | Modificado (+223) | `TOCABLES` ampliado a once ficheros; los once controles nuevos; contrato de `puerta()` actualizado al rc=4 |
| `.paul/DEUDAS.md` | Modificado | D-39/40/41 cerradas, D-42 abierta, D-26 re-medida — **en el mismo commit** |

## Decisiones tomadas

| Decision | Motivo | Efecto |
|---|---|---|
| El rc=4 **y** el `unset` del enganche son **dos capas**, no una | Con una sola, el agujero sigue abierto por el otro lado: el rc arregla el contrato, el `unset` arregla el entorno | Ninguna de las dos por si sola cierra D-40 |
| El contrato del rc se cambio **en el mismo commit** que su consumidor vivo | `sabotage.py::puerta()` corre la puerta con esa variable y su vacuidad exige que salga verde. Cambiarlo sin tocar al consumidor **mataba el banco entero** | Y con control positivo: revertido el `exit 4`, la vacuidad lo caza |
| El vigilante del enganche va **despues** del banco y **fuera** de la corrida interior | Cablearlo antes dejaba al banco sin correr en cualquier maquina sin el enganche instalado — o sea, en un CI. Y mide **la maquina**, no el codigo | Un CI limpio sigue ejerciendo el banco |
| `comparar_o_roto` se deja **sin oraculo** a proposito y se ficha como **D-42** | Quitarlo devolveria el rc=1 con traceback en cuanto alguien anada una clave sin validar, que es justo D-39. Se queda como red de seguridad declarada | Deuda escrita, no escondida |
| La foto corrupta imprime su **remedio** | Una foto ilegible bloqueaba tambien el resellado: el operador quedaba sin salida | Todos los rc=2 de foto dicen como salir |
| `index.html` intacto es **evidencia**, no ausencia de trabajo | Junto con «ninguna foto resellada», es la prueba de que los instrumentos siguen midiendo lo mismo | Boundary respetado y verificado por comando |

## Revision adversaria del diff (G6)

Se ejecuto **durante APPLY**, antes del commit, con **9 hallazgos, todos atendidos**. Los dos mas
graves eran **falsos verdes del arreglo recien escrito**, y se reprodujeron a mano en un repo de
usar y tirar antes de creerselos:

1. **Un enganche sin bit de ejecucion hace que git lo IGNORE**, y el push sale con rc=0. El
   comprobador lo daba por bueno. → caso «NO EJECUTABLE» (rc=1), permanente.
2. **Suponer `.git/hooks` es falso** con `core.hooksPath` puesto, o en un worktree. → resuelto
   preguntandoselo a git.
3. **Dano colateral:** cablear el vigilante ANTES del banco dejaba al banco sin correr en cualquier
   maquina sin el enganche. → movido despues y fuera de la corrida interior.
4. Al arreglar la restauracion atomica de la puerta **se perdia su bit de ejecucion** — la misma
   clase de fallo. → test permanente («la puerta y el instalador siguen siendo ejecutables») y
   control positivo.

> **Lo que hace que esto no sea una anecdota fechada:** los nueve hallazgos no se arreglaron y ya;
> **once controles nuevos del banco** los vuelven a demostrar manana. Eso es lo que se ha
> verificado hoy en fresco, y no el recuerdo de la revision.
>
> **Con fidelidad:** la revision en si **no dejo artefacto propio en el repo** — su unica traza
> narrativa es el mensaje de commit. Lo que si es verificable y se ha verificado es su **resultado**
> cableado al banco. Se anota como observacion, no se blanquea.

## Desviaciones del plan

| Tipo | Cuantas | Valoracion |
|---|---|---|
| Auto-corregidas dentro del ciclo | 9 | Todas de la revision adversaria; todas con control permanente |
| Ampliaciones de alcance | 0 | Ningun boundary cruzado. `index.html` intacto |
| Diferidas por escrito | 1 | **D-42**, en el libro en el mismo commit |

El plan preveia **tres** desenlaces de `hookcheck` (AUSENTE · DISTINTO · ILEGIBLE) y se
construyeron **seis** (+ NO EJECUTABLE, + FORMA, + el enganche deja de limpiar la variable). No es
ampliacion de alcance: tres de ellos salieron de la revision adversaria como **agujeros reales del
comprobador recien escrito**.

## Estado de las deudas

| Deuda | Antes | Ahora |
|---|---|---|
| **D-39** trinquetes fallando ABIERTO | ABIERTA, bloqueando | **CERRADA**. Reabre: cualquier instrumento nuevo que lea una foto sin validar tipos |
| **D-40** `VERIFY_INNER=1` deja rc=0 sin banco | ABIERTA, bloqueando | **CERRADA** con las dos capas. Reabre: cualquier interruptor nuevo que reduzca lo ejercido sin cambiar el rc |
| **D-41** nadie vigila el enganche | ABIERTA, bloqueando | **CERRADA** con `hookcheck.py` cableado. Reabre: otro enganche de git sin su fila |
| **D-42** `comparar_o_roto` sin oraculo | — | **ABIERTA** a proposito, con su motivo escrito |
| **D-26** `funciones_vistas` sellada y sin re-derivar | ABIERTA | **RE-MEDIDA**: 186 sellado vs **190** derivadas. Se ha vuelto a desfasar. Sigue abierta |
| **D-38** la capa de aviso sin oraculo | ABIERTA, **bloquea la Fase 1** | **SIGUE ABIERTA**. Es el ciclo **01-06**, entera |

## Preparado para lo siguiente

**Listo:** la puerta con la que se va a medir el 01-06 ya no puede salir verde sin ejercerse, ni
confundir un instrumento roto con un hallazgo del codigo, ni suponer la variante automatica.

**Sin verificacion en navegador, y correctamente:** este ciclo **no toca la app**. El requisito de
§7 bis no aplica aqui y **reaparece obligatorio en el 01-06**, que si cambia lo que el operador ve
cuando algo falla.

**Sin desplegar:** el local va **5 commits por delante** de `origin/main` (que sigue en `7b6115a`).
Comprobado que eso **no afecta a la app**: el `index.html` de HEAD es **el mismo blob**
(`a2ed63a9…`) que el de `origin/main`, o sea que Pages sirve exactamente el codigo que se verifico
en el navegador el 2026-08-31. Lo pendiente de empujar son actas y herramientas.

**Bloqueadores para cerrar la Fase 1:** **D-38**, entera. Es el 01-06.

---
*Fase: 01-guardado-fiable, Ciclo: 05*
*Completado: 2026-08-31 — cifras derivadas en esta sesion, arbol `1bd8d35b…`*
