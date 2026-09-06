# Medición previa al ciclo 01-08 — 2026-09-06

> **Por qué existe este documento.** El acta de la quinta transición
> (`01-TRANSICION-5.md`) dejó un aviso explícito: *«los hallazgos de los brazos NO se heredan;
> uno de ellos resultó falso al re-verificarlo»*. Antes de escribir el PLAN 01-08 se han vuelto
> a medir, **ejecutando**, las cuatro deudas que lo abren. El plan se escribe sobre esto, no
> sobre el acta.

## Condiciones de la medición

- Árbol real **en exclusiva**, limpio (`git status` vacío) antes y después.
- `index.html` en `9459b0fc3b40a50a38d0c506fec2b862` **antes y después**. No se tocó.
- Puerta de partida: `tools/verify.sh` → **rc=0**, once pasos, «VERDE — todo ejercido y en verde».
- Cada medición sobre **su propia copia** bajo el directorio de sesión, con la ruta **fijada en
  absoluto** y afirmada por el arnés (`assert BASE.is_dir()`). Es la regla que nació de la quinta
  transición: un proceso lanzado en segundo plano arrancó con el directorio reseteado al repo.
- Cada sabotaje **afirma la unicidad de su ancla antes de mutar** y aborta si no es única.

## Resultados

### D-58 · el libro que no cabe adelanta el reloj — **CONFIRMADA**

Sembrado: disco con 2 operaciones y `savedAt: 1000`; llega de la nube un documento con 42
operaciones y `savedAt: 9000`; la escritura de `balance-ops` lanza `QuotaExceededError` y **sólo
esa clave** falla. Medido:

```
opsAntes: 2          aplicado: true       discoOps: ["o1","o2"]
metaSavedAt: 9000    opsEnMemoria: 2
guardado: true       pintado: "Guardado ✓" / var(--green)
subida: {"subido": true, "aviso": "ok", "motivo": "ok"}
nubeAntes: 42        nubeDespues: 2
puntoSync: "Sincronizado"   textoSync: "Sincronizado con tu cuenta."
```

**Control de vacuidad (PASA):** el mismo arnés sin la cuota llena aterriza las 42 operaciones en
disco y la nube se queda en 42. El instrumento no es siempre-rojo: distingue.

Lectura: la pérdida ocurre **en la nube**, que es de donde sale la declaración. La puerta entera
sale `rc=0` sobre este código.

### D-59 · el aviso del camino de nube no tiene oráculo — **CONFIRMADA**

Dos mutantes semánticos, cada uno sobre su copia, con ancla única afirmada; después se corrió la
**puerta entera** sobre cada copia:

| Mutante | Qué cambia | Puerta |
|---|---|---|
| **U8** | tras una escritura a la nube que **falla**, pintar `ok` en vez de `error` | **rc=0** · «VERDE — todo ejercido y en verde» |
| **U3** | una subida **omitida por el juez** se pinta `ok` en vez del aviso del veredicto | **rc=0** · «VERDE — todo ejercido y en verde» |

Nota de método: el ancla de U3 **no era única** al primer intento (2 ocurrencias:
`subirALaNube` y `listenFirestore`). Se amplió con su línea de contexto en vez de reportar «no
muerde» — el defecto habría sido del banco, no del código (§5.4).

### D-48 · cambiar o crear cartera pinta verde con la escritura fallida — **CONFIRMADA**

`balance-meta-v2` lanza al escribir; el resto del disco funciona. Los cinco llamantes:

| Llamante | Pinta | Subidas | Lista en disco | Lista en memoria | Activos de B |
|---|---|---|---|---|---|
| `switchPortfolio` | **«Guardado ✓» / var(--green)** | 0 | A, B | A, B | presente |
| `addPortfolio` | **«Guardado ✓» / var(--green)** | 0 | A, B | A, B, **Nueva** | presente |
| `renamePortfolio` | — | 0 | A, B | **Renombrada**, B | presente |
| `deletePortfolio` | — | 0 | **A, B** | A | **BORRADO DEL DISCO** |
| `createDefaultPortfolios` | — | 0 | A, B | ☢ Nuclear, 🤖 Robótica | presente |

**Control de vacuidad (PASA):** sin la escritura rota, disco y memoria coinciden en los cinco.

El peor sigue siendo `deletePortfolio`: borra los activos **antes** de guardar la lista, así que
la lista guardada sigue anunciando una cartera cuyos datos ya no existen. Ninguno sube a la nube:
el daño de los otros cuatro es **pantalla que miente y divergencia silenciosa**, no pérdida del
libro de operaciones.

### D-61 · `avisos.py --update` amnistía en silencio — **CONFIRMADA**

Ancla única afirmada (1 ocurrencia) y cerrada una boca: `console.error('No se sincroniza: el
guardado local falló.')` → `console.log`.

```
--check  (sin sabotaje) → rc=0   «Capa de aviso sin cambios: 40 aviso(s) en 40 claves»   [vacuidad]
--check  (con sabotaje) → rc=1   nombra la clave: «(1 -> 0): ha desaparecido»
                                  y añade «No se resella de tramite.»
--update (sin --amnesty)→ rc=0   «Foto sellada: 39 aviso(s) en 39 claves»  ← SIN NOMBRAR NADA
--check  (después)      → rc=0   verde para siempre
```

Causa confirmada por lectura: `sumideros.py` clasifica una boca que desaparece como **`peor`**
para el tipo `anunciar`; `avisos.py` la clasifica como **`mejor`**. La asimetría ES el defecto
(§5.16). El 01-06 lo cerró sólo por el lado de `--check`.

## Mapa de pintados del camino de nube (para cerrar D-59 por RECEPTOR)

Derivado del fichero, no enumerado a mano. Atribución **por función contenedora**, que es
presencia y no precedencia (§5.11) — sirve para saber dónde mirar, no como criterio:

| Función | Pintados | Ramas |
|---|---|---|
| `subirALaNube` | 3 | subida omitida por el juez · escritura que lanza · éxito. **Y una cuarta rama sin pintar: `sin sesión` sale con `aviso:'offline'` y no toca la pantalla** |
| `listenFirestore` | 3 | META ilegible · cambio no aplicado · el escucha muere |
| `alIniciarSesion` | 2 | ya cubiertos por el 01-07 |

## Estado del árbol al terminar

`index.html` → `9459b0fc3b40a50a38d0c506fec2b862` · `git status` vacío · puerta `rc=0`.

---

## Ampliación de la medición — mismo día, tras la dialéctica

### D-59: dos mutantes más de la ESCUCHA, medidos

| Mutante | Qué cambia | Puerta |
|---|---|---|
| **E7** | el escucha de la nube **muere** y se pinta `ok` en vez de `error` | **rc=0** · VERDE — **VIVE** |
| **E2** | el naranja de la escucha pierde su **motivo** | rc=1, **pero por accidente** |

E2 merece su propia línea porque **corrige la ficha**. El rojo NO viene de un oráculo: viene del
banco, con este mensaje literal:

```
BANCO ROTO: la escucha en vivo rechaza sin pintar nada — ancla no unica en index.html:
0 apariciones de "...". El defecto esta en el BANCO, no en el control.
CONTROLES QUE NO MUERDEN (1): la escucha en vivo rechaza sin pintar nada (banco)
```

Es decir: el mutante rompió el ancla de un sabotaje vecino y el rojo **manda a mirar la
herramienta, no el código**. Cuenta como caza accidental, no como cobertura. Confirma la frase de
la ficha D-59 sobre «los cuatro que la puerta sólo caza por accidente del banco».

### La rama «sin sesión» de `subirALaNube` NO es un hueco

Se sospechó al derivar el mapa: es la única de las cuatro ramas que no pinta. Medido con un
estado ROJO previo en pantalla:

```
antes:    punto "No se pudo sincronizar" · texto "...los cambios siguen guardados en este dispositivo."
resultado {"subido": false, "aviso": "offline", "motivo": "sin sesión"}
después:  punto "No se pudo sincronizar" · texto (idéntico)
```

No pisa el estado anterior con verde: lo deja como estaba. **No se ficha.**

### HALLAZGO NUEVO · la cuota llena DE VERDAD hace algo distinto — y peor

La ficha D-58 describe el caso en que **sólo** falla la escritura del libro. Si la cuota está
llena para **todas** las claves —que es lo que pasa en un navegador real—, el comportamiento es
otro. Medido:

```
LANZO: QuotaExceededError            ← la excepción ESCAPA de applySyncPayload
discoOps:  ["o1"]                    ← disco: libro viejo
discoMeta: {portfolios:[Vieja], currentPortId:7, nextId:8, savedAt:1000}   ← disco: coherente y viejo
memoriaCarteras: ["DeLaNube"]        ← MEMORIA: las carteras de la nube
memoriaCurrent: 9   memoriaNextId: 20
```

Dos consecuencias:

1. **La memoria queda mutada y el disco no.** `applySyncPayload` asigna `portfolios`,
   `currentPortId` y `nextId` (líneas 3045-3047) **antes** de intentar ninguna escritura, y las
   escrituras de filas e historial (3049-3054) **no tienen `try/catch`**. La app queda enseñando
   una cartera que no está en disco y cuyas filas nunca se escribieron. El primer `saveMeta`
   posterior escribiría esa memoria en disco.
2. **La excepción no la recoge nadie.** `pullFromFirestore` llama a `d.aplicar(data)` **sin
   `try`** (línea 3263), así que sale de la función y de la promesa.

Esto no invalida D-58: la agrava y le añade una segunda familia. El enfoque elegido —probar el
libro PRIMERO y abortar antes de escribir nada— cierra **las dos**, porque suprime las escrituras
posteriores en vez de tratarlas una a una.

### Hecho verificado a mano que sostiene el enfoque

`pullFromFirestore` línea 3266: `d.pintar(estadoSync(decision.aviso), decision.motivo);` se
ejecuta **siempre con el aviso del veredicto** e **ignora `aplicado`**, que sí calcula y sí
devuelve. Por eso el verde no se apaga donde el daño se produce.
