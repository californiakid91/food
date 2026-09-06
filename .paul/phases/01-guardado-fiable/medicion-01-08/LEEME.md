# Arneses de la medición previa al 01-08

**Qué son:** los arneses con los que se re-midieron D-58, D-59, D-48 y D-61 el 2026-09-06, antes
de escribir el PLAN. Resultados en `../01-08-MEDICION-PREVIA.md`.

**Qué NO son: NO son instrumentos de la puerta.** No están cableados a `tools/verify.sh` y nadie
los ejecuta solo. Se guardan aquí para que las cifras del plan sean **reproducibles**, no para
vigilar nada. Lo que vigila mañana son las autopruebas y el banco de sabotaje, y el PLAN 01-08
exige que los cruces que estos arneses miden pasen a vivir allí.

**Cómo se usan** (desde una COPIA del proyecto, nunca sobre el árbol real):

```
cp -r <repo> /ruta/copia
python3 arnes.py /ruta/copia caso-d58.js
```

`arnes.py` extrae el `<script>` inline, lo carga sobre el DOM de mentira de `tools/dom_stub.js`
—derivando del marcado los identificadores reales, para que un identificador inexistente devuelva
`null` como en el navegador— y ejecuta el caso. Falla CERRADO: si no puede extraer, cargar o
terminar, sale con `rc=2`, nunca «0 hallazgos».

**Los dos casos de vacuidad son obligatorios.** Sin ellos, un arnés siempre-rojo pasaría por
hallazgo.
