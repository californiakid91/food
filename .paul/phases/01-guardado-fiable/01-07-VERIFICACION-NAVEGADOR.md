# Verificación en navegador — ciclo 01-07

**Estado: EN CURSO.** Despliegue hecho y confirmado; falta la pasada del operador.

## Preparación (hecha por el asistente, 2026-09-05)

| Paso | Resultado |
|---|---|
| Puerta manual `tools/verify.sh` | **rc=0**, once pasos en verde |
| `index.html` idéntico antes y después de la puerta | `5b3807ddb7edf1f8bd7959bda7773901` en ambas |
| Push a `origin/main` | `685b44b..42ee677`, con el enganche `pre-push` ejerciendo la puerta otra vez (rc=0) |
| Pages sirve la versión nueva | **SÍ**. Huella descargada `5b3807ddb7edf1f8bd7959bda7773901`, idéntica a la local. Los **dos primeros intentos** devolvieron todavía la anterior (`66e6dd20…`) |

Se confirma la huella ANTES de mirar la pantalla, como en las cuatro pasadas previas.

## Puntos a ejercer — AC-9

URL: `https://californiakid91.github.io/food/` — **recargar dos veces** (el service worker
sirve la versión anterior en la primera).

| # | Punto | Cómo | Resultado | Evidencia |
|---|---|---|---|---|
| 1 | El navegador tiene el código nuevo | en consola: `typeof decidirBajada === 'function'` → debe dar `true` | PENDIENTE | |
| 2 | Recuento ANTES | en consola: `JSON.parse(localStorage.getItem('balance-ops')).length` y el número de carteras | PENDIENTE | |
| 3 | `?selftest=1` imprime «✅ Autopruebas OK» | abrir con el parámetro y leer la consola | PENDIENTE | |
| 4 | Recuento DESPUÉS, idéntico | mismo comando que el punto 2 | PENDIENTE | |
| 5 | Guardar sigue funcionando tras las autopruebas | cambiar un valor y ver el aviso de guardado | PENDIENTE | |
| 6 | Alta de cartera | crear una cartera nueva | PENDIENTE | |
| 7 | Borrado de operación | borrar una operación (uno de los dos sitios operados este ciclo) | PENDIENTE | |
| 8 | Interruptor de objetivos | accionarlo (el otro sitio operado este ciclo) | PENDIENTE | |
| 9 | **Estado del indicador de sincronización** | mirar el puntito y decir de qué color está | PENDIENTE | |

El punto 9 va aparte y se reporta **explícitamente**: quedó sin reportar en la pasada del 01-06 y
no se hereda de que el resto fuera bien.

## Lo que esta pasada NO comprueba

- El aviso ROJO del **guardado local** fallido: sigue siendo **D-18**. Exige agotar el
  almacenamiento del navegador con el libro real delante.


## Hallazgo en el punto 0 — antes de empezar la lista

Al abrir la app desplegada, **lo primero** que apareció fue el naranja «Cambios sin subir: este
dispositivo **no tiene operaciones** y no se pisa el libro de la nube», en un dispositivo con **90
operaciones**. El operador preguntó si era normal.

**Causa DEMOSTRADA, no supuesta.** En la consola del dispositivo del operador:

```
JSON.parse(localStorage.getItem('balance-meta-v2')||'{}').savedAt   →   undefined
```

Sin marca de tiempo local, `decidirBajada` entra por la rama `reloj-desconocido`: hay datos que
proteger y no hay desempate posible, así que **no aplica** el documento y avisa. Es **D-50**, el
coste declarado del ciclo, y es el comportamiento QUERIDO: quedarse quieto y decirlo, antes que
dejar ganar a la nube y empobrecer el libro en verde.

| Parte | Veredicto |
|---|---|
| **Comportamiento** (no aplicar, avisar en naranja, no perder nada) | **CORRECTO y previsto** — D-50 |
| **Texto del aviso** | **DEFECTO** — atribuye una causa falsa: **D-54** |

El texto es un hallazgo de correctness y se arregla dentro de este ciclo. El comportamiento no se
toca.

**El despliegue no pierde datos**, y el estado se deshace solo en cuanto el operador guarde algo una
vez: eso vuelve a poner el reloj local en hora.
