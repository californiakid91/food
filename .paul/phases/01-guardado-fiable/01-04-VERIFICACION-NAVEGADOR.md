# Verificación en el navegador — ciclo 01-04

**Por qué existe este documento.** La puerta (`tools/verify.sh`) ejerce las funciones puras en
node sobre un DOM de mentira. **No prueba la pantalla.** El 01-04 añade un estado visual nuevo
—el punto ROJO «No se pudo sincronizar»— y §7 bis exige abrir la app desplegada antes de dar
por buena una fase que toque la interfaz.

**Estado del despliegue.** Empujado el 2026-08-31: `9ca21ee..7b6115a`. La puerta pasó por su
variante automática (enganche `pre-push`, `rc=0`, ocho pasos en verde). Confirmado que GitHub
Pages sirve la versión nueva: huella del fichero descargado `4ff3b0ba79afa7ca1d479ea1525ad51d`,
idéntica a la local. Los dos primeros intentos devolvieron la anterior (`661acd6b…`), como en
la pasada del 01-03: **el service worker sirve la versión vieja en la primera carga**.

---

## 0. Antes de mirar nada: confirmar que ESTE navegador tiene el código nuevo

Abrir `https://californiakid91.github.io/food/`, **recargar dos veces**, abrir la consola
(F12) y escribir:

```
typeof decidirSubida === 'function' && typeof estadoSync === 'function'
```

Tiene que decir `true`. Si dice `false`, el navegador sigue con la versión anterior: recargar
otra vez con Ctrl+Shift+R. **No se comprueba nada más hasta que esto sea `true`.** Juzgar por
el aspecto de la pantalla es exactamente lo que esta línea evita.

## 1. Contar los datos ANTES

En la consola:

```
JSON.parse(localStorage.getItem('balance-ops')||'[]').length
```

Anotar el número. En las dos pasadas anteriores fueron **90 operaciones y 4 carteras**.

## 2. Uso normal: el punto se pone VERDE

Guardar cualquier cambio pequeño y mirar el indicador de sincronía. Esperado: **verde**,
«Guardado ✓». El verde ya no se pinta al entrar por costumbre: sólo se alcanza cuando la
subida termina bien de verdad.

## 3. Autopruebas dentro del navegador real

Abrir `https://californiakid91.github.io/food/?selftest=1`. Esperado en consola:
**«✅ Autopruebas OK»**. Y volver a contar las operaciones del paso 1: **el mismo número**.
Que no diga «OK» y que no borre son dos afirmaciones independientes — el fallo original de
este proyecto consistía justo en decir OK MIENTRAS borraba.

## 4. El estado NARANJA «Cambios sin subir» (no destructivo)

En la consola:

```
await subirALaNube('prueba manual', {ref: userDocRef(), paquete: buildSyncPayload,
  mirar: observarNube, cerrojo: () => true, activos: hasRealLocalData})
```

Esto le dice al juez que el libro local está ilegible. **No escribe nada en la nube.**
Esperado: el punto se pone **naranja** y la consola devuelve `aviso: 'pendiente'`.

## 5. El estado ROJO «No se pudo sincronizar» — lo nuevo de este ciclo

Perder la conexión NO sirve para verlo: sin red la escritura se queda esperando y el punto se
queda naranja. El rojo lo pinta el fallo REAL de la escritura, así que se provoca dándole al
código una escritura que falla:

```
await subirALaNube('prueba manual', {ref: {set: () => Promise.reject(new Error('prueba'))},
  paquete: buildSyncPayload, mirar: observarNube, cerrojo: () => opsIlegible,
  activos: hasRealLocalData})
```

La escritura es de mentira: **no toca la nube**. Recorre el camino real hasta el `catch`.
Esperado: punto **ROJO**, texto «No se pudo sincronizar: los cambios siguen guardados en este
dispositivo», y la consola devuelve `aviso: 'error'`.

Para volver a verde: recargar y guardar cualquier cambio.

## 6. Volver a contar los datos DESPUÉS

Repetir el paso 1. Tiene que dar el mismo número que al principio.

---

## Resultados

| Punto | Resultado | Evidencia |
|---|---|---|
| 0 · el navegador tiene el código nuevo | **PASS** | `typeof decidirSubida === 'function'` → `true` en la consola del operador |
| 2 · verde en uso normal | **PASS** | visto en pantalla por el operador |
| 3 · «✅ Autopruebas OK» | **PASS** | leído en la consola |
| 3 · `?selftest=1` deja los datos intactos | **PASS** | operaciones contadas antes y después por el operador, sin cambio |
| 4 · naranja «Cambios sin subir» | **PASS** | provocado con el cerrojo de mentira; punto naranja, `aviso: 'pendiente'` |
| 5 · **ROJO «No se pudo sincronizar»** | **PASS** | provocado con una escritura que rechaza; punto rojo, `aviso: 'error'`. **Es la primera vez que este estado se ve en un navegador real** |
| 6 · datos intactos al final | **PENDIENTE** | recuento final no comunicado |

> Se rellena con lo que el operador VE, no con lo que se espera que pase. Un punto sin
> evidencia se queda en PENDIENTE, no pasa a PASS.

**Lo que este documento NO demuestra.** Las cifras exactas del recuento no quedaron anotadas en
esta pasada: el operador confirmó que no cambiaban, pero las dos pasadas anteriores sí dejaron
el número (90 operaciones, 4 carteras). Una confirmación sin cifra es más débil que una con
cifra y así se dice, en vez de copiar el 90 de una pasada anterior como si se hubiera medido hoy.

**D-18 sigue abierta.** El rojo comprobado aquí es el de la SUBIDA fallida. El aviso rojo del
GUARDADO LOCAL fallido —el que exige agotar el almacenamiento del navegador— sigue sin
comprobarse desde la Fase 0. Son dos avisos distintos y este ciclo sólo cierra uno.
