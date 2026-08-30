#!/usr/bin/env bash
# LA PUERTA. El unico objetivo agregado que ejerce todo lo que hay que ejercer.
#
# Correr "las autopruebas" NO es la puerta: la puerta es esto.
# El pre-push de git llama a este mismo script, asi que la variante automatica
# no puede ejercer menos que la manual: hay UNA sola lista, la de aqui abajo.
#
# Codigos de salida nominales (cada uno con su mensaje propio):
#   0  verde
#   1  hallazgo real: algo esta mal en el codigo
#   2  instrumento roto: no se pudo medir. NO es lo mismo que "0 hallazgos".
#   3  deriva: cambio la regla de medida, la foto sellada ya no es comparable
#
# Uso:
#   tools/verify.sh            comprueba todo
#
# NO hay interruptor de degradado. Aqui se anunciaba un VERIFY_DEGRADED=1 que
# NINGUNA rama de este script leia: un comentario que promete un mecanismo sin
# cablearlo no cablea nada (CLAUDE.md 5.1). Se borra en vez de implementarlo.
# El unico interruptor real es VERIFY_INNER=1, y AVISA cuando actua.

set -uo pipefail
cd "$(dirname "$0")/.." || { echo "rc=2 INSTRUMENTO ROTO: no puedo situarme en el repo" >&2; exit 2; }

rc_final=0
fallos=()
rotos=()
derivas=()

# Registra el resultado de un paso sin dejar que la tuberia se coma su codigo.
paso() {
  local nombre="$1"; shift
  local salida rc
  salida="$("$@" 2>&1)"; rc=$?
  case $rc in
    0) printf '  OK    %s\n' "$nombre" ;;
    1) printf '  FALLO %s\n' "$nombre"; fallos+=("$nombre"); [ "$rc_final" -lt 1 ] && rc_final=1 ;;
    3) printf '  DERIVA %s\n' "$nombre"; derivas+=("$nombre"); rc_final=3 ;;
    *) printf '  ROTO  %s (rc=%s)\n' "$nombre" "$rc"; rotos+=("$nombre"); [ "$rc_final" -lt 2 ] && rc_final=2 ;;
  esac
  if [ $rc -ne 0 ]; then
    printf '%s\n' "$salida" | sed 's/^/        /'
  fi
}

echo "PUERTA — food"
echo

# ── Comprobaciones. UNA sola lista, compartida por el hook y por la mano. ────

# 1. El fichero que se sirve tiene que existir y no estar vacio.
paso "index.html presente y no vacio" bash -c '[ -s index.html ]'

# 2. Sintaxis del script que se sirve al navegador.
paso "sintaxis de index.html" python3 tools/check_syntax.py

# 3. Los invariantes del propio codigo, ejecutados de verdad.
paso "autopruebas (runSelfTests)" python3 tools/run_selftests.py

# 4. El monolito no engorda.
paso "trinquete de tamano de funciones" python3 tools/funcsize.py --check

# 5. La puerta unica de escritura a la nube, y su aviso. Dos redes disjuntas.
#    Va FUERA de cualquier interruptor de degradado: las comprobaciones nuevas
#    no se saltan nunca.
paso "puerta unica de escritura a la nube" python3 tools/cloudwrites.py

# 6. Censo de catch vacios contra la foto sellada.
paso "censo de catch vacios" python3 tools/emptycatch.py --check

# 7. El banco de sabotaje: demuestra que lo de arriba MUERDE.
#    Se salta cuando la puerta corre DENTRO del propio banco (VERIFY_INNER=1),
#    que es la unica forma de que no se llame a si misma en bucle.
#    Si algo de lo anterior ya esta rojo, el banco no puede medir nada (su
#    control de vacuidad lo detectaria y gritaria "instrumento roto"), y ese
#    aviso TAPARIA el hallazgo real mandando a mirar las herramientas en vez
#    del codigo. Asi que se omite, ruidosamente, sin contar como verde.
banco_omitido=""
if [ "${VERIFY_INNER:-0}" = "1" ]; then
  # El salto era MUDO y el resumen seguia diciendo "todo ejercido y en verde".
  # Si esta variable quedara exportada en un entorno, la puerta dejaria de
  # probar que los controles muerden sin decir ni una palabra. El silencio
  # nunca es limpio.
  echo "  OMITIDO banco de sabotaje: VERIFY_INNER=1 (la puerta corre DENTRO del banco)"
  banco_omitido="si"
elif [ "$rc_final" -ne 0 ]; then
  banco_omitido="si"
  echo "  OMITIDO banco de sabotaje: la puerta ya esta roja, arregla primero lo de arriba"
else
  paso "banco de sabotaje (los controles muerden)" python3 tools/sabotage.py
fi

# 8. Higiene de las herramientas de medida. Un instrumento sucio no mide.
if command -v ruff >/dev/null 2>&1; then
  paso "lint de tools/" ruff check tools/
else
  # Las comprobaciones nuevas van FUERA del interruptor de degradado, pero una
  # herramienta ausente se avisa, no se calla.
  echo "  AVISO ruff no instalado: no se pudo comprobar la higiene de tools/"
  rotos+=("lint de tools/ (ruff ausente)")
  [ "$rc_final" -lt 2 ] && rc_final=2
fi

echo
# ── Veredicto. Ante delta mixto manda lo peor. ───────────────────────────────
if [ ${#derivas[@]} -gt 0 ]; then
  echo "DERIVA (rc=3): ${derivas[*]}"
  echo "La regla de medida cambio. Comparar las cifras ya no significa nada."
  echo "Esto NO se arregla resellando la foto: averigua por que cambio."
  exit 3
fi
if [ ${#rotos[@]} -gt 0 ]; then
  echo "DEGRADADO — INSTRUMENTO ROTO (rc=2): ${rotos[*]}"
  echo "No se pudo medir. Esto NO es un verde."
  exit 2
fi
if [ ${#fallos[@]} -gt 0 ]; then
  echo "HALLAZGOS (rc=1): ${fallos[*]}"
  exit 1
fi
if [ -n "$banco_omitido" ]; then
  echo "VERDE, PERO EL BANCO NO CORRIO: nada demuestra hoy que estos controles muerdan."
  exit 0
fi
echo "VERDE — todo ejercido y en verde."
exit 0
