#!/usr/bin/env python3
"""Vigila la variante AUTOMATICA de la puerta: el enganche `pre-push`.

La doctrina exige verificar las DOS variantes, la manual y la automatica. Hasta
este ciclo la automatica estaba SUPUESTA: los hooks de git no viajan en el repo,
asi que en una maquina nueva simplemente no existe, y nada se ponia rojo. Un
instrumento que existe pero que no dispara ningun objetivo no existe (D-41).

Compara el enganche INSTALADO en `.git/hooks/pre-push` con el que produce
`tools/install-hooks.sh`. El contenido esperado se DERIVA del instalador -- se
extrae su heredoc como texto -- en vez de pegar aqui una copia: dos copias se
desincronizan a la primera, y entonces este comprobador vigilaria un texto que
ya no instala nadie.

No se puede EJECUTAR el instalador para averiguarlo: escribe en `.git/hooks`,
o sea que muta el arbol que estamos midiendo.

CEGUERAS DECLARADAS (antes de que alguien las descubra):
  - Compara TEXTO, byte a byte tras normalizar el salto de linea final. No
    ejecuta el enganche ni comprueba que haga lo que dice.
  - Solo mira `pre-push`. Si algun dia hubiera mas enganches, hay que anadirlos
    aqui: esta lista es enumerada, no derivada.
  - No mira si el repo tiene remoto, ni si el operador usa `--no-verify`. Eso
    ultimo es deliberado: saltarse la puerta a sabiendas y en voz alta esta
    permitido; lo que no puede pasar es que se salte sola.
  - Extraer el heredoc lo convierte en OTRO escaner, con su propio deber de
    fallar cerrado: si el instalador cambia de forma y el heredoc no aparece
    exactamente una vez, esto es rc=2, nunca "coinciden".

Tres desenlaces distintos y DISTINGUIBLES, porque mandan a sitios distintos:
  AUSENTE     -> hay que correr tools/install-hooks.sh
  NO EJECUTABLE -> git lo IGNORA y el push sale con rc=0
  DISTINTO -> alguien edito el enganche a mano, o el instalador cambio y no se
              reinstalo
  ILEGIBLE -> el instrumento no pudo medir

Codigos de salida (nominales, cada uno con su mensaje):
  0  verde: el enganche instalado es exactamente el que instala el instalador
  1  hallazgo real: AUSENTE, NO EJECUTABLE o DISTINTO
  2  instrumento roto: no pudo medir (ILEGIBLE)
"""
import argparse
import os
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INSTALADOR = ROOT / 'tools' / 'install-hooks.sh'


def enganche_por_defecto():
    """Donde git va a buscar `pre-push` DE VERDAD, preguntandoselo a git.

    Suponer `.git/hooks` era un falso verde medido el 2026-08-31: con
    `core.hooksPath` apuntando a otro sitio, un `pre-push` ejecutable en
    `.git/hooks` se ignora entero y el push sale con rc=0 -- mientras esto
    habria dicho "Verde". Lo mismo en un `git worktree`, donde `.git` es un
    fichero y ese directorio no puede existir.
    """
    try:
        r = subprocess.run(['git', 'rev-parse', '--git-path', 'hooks'],
                           capture_output=True, text=True, check=False, cwd=ROOT)
    except OSError as e:
        roto(f"no pude preguntarle a git donde viven los enganches: {e}")
    if r.returncode != 0:
        roto("no pude preguntarle a git donde viven los enganches: "
             f"`git rev-parse --git-path hooks` dio rc={r.returncode}: "
             f"{r.stderr.strip()}")
    ruta = r.stdout.strip()
    if not ruta:
        roto("`git rev-parse --git-path hooks` no devolvio ninguna ruta")
    d = pathlib.Path(ruta)
    return (d if d.is_absolute() else ROOT / d) / 'pre-push'

# La forma del instalador de la que se deriva el contenido esperado. Si esto
# deja de casar, el instrumento NO adivina: dice que no puede medir.
HEREDOC = re.compile(
    r"^cat > \"\$HOOKS/pre-push\" <<'HOOK'\n(.*?)^HOOK\n",
    re.DOTALL | re.MULTILINE)


def roto(msg):
    print(f"rc=2 INSTRUMENTO ROTO: hookcheck: {msg}", file=sys.stderr)
    sys.exit(2)


def esperado(instalador):
    """El texto que el instalador escribiria, extraido de su heredoc."""
    if not instalador.is_file():
        roto(f"no existe el instalador {instalador}")
    try:
        texto = instalador.read_text(encoding='utf-8')
    except Exception as e:  # noqa: BLE001 - fallar CERRADO ante cualquier lectura mala
        roto(f"no puedo leer el instalador {instalador}: {e}")
    hallados = HEREDOC.findall(texto)
    if len(hallados) != 1:
        roto(f"esperaba 1 heredoc 'HOOK' en {instalador.name}, encontre "
             f"{len(hallados)}. El instalador ha cambiado de forma: este "
             "comprobador ya no sabe que deberia haber instalado.")
    cuerpo = hallados[0]
    if not cuerpo.strip():
        roto(f"el heredoc de {instalador.name} esta vacio")
    return cuerpo


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--hook', default=None,
                    help='enganche a comprobar (por defecto, el que mira git)')
    ap.add_argument('--installer', default=str(INSTALADOR),
                    help='instalador del que derivar lo esperado')
    args = ap.parse_args()

    enganche = pathlib.Path(args.hook) if args.hook else enganche_por_defecto()
    quiero = esperado(pathlib.Path(args.installer))

    if not enganche.is_file():
        print(f"rc=1 ENGANCHE AUSENTE: no existe {enganche}.")
        print("   La variante AUTOMATICA de la puerta no existe en esta maquina:")
        print("   un push no ejerce nada. Los hooks no viajan en el repo.")
        print("   Se arregla con:  bash tools/install-hooks.sh")
        sys.exit(1)

    # Existe, pero puede estar MUERTO. Sin el bit de ejecucion git lo ignora,
    # avisa con un `hint:` silenciable y el push SALE CON RC=0: la variante
    # automatica desaparece sin que nada se ponga rojo, que es exactamente el
    # falso verde que D-41 existe para cerrar. Medido el 2026-08-31 en un repo
    # de usar y tirar, no razonado.
    if not os.access(enganche, os.X_OK):
        print(f"rc=1 ENGANCHE NO EJECUTABLE: {enganche} existe, pero sin permiso "
              "de ejecucion.")
        print("   Git IGNORA los enganches no ejecutables: avisa con un `hint:`")
        print("   que se puede silenciar, y el push sale con rc=0. La variante")
        print("   AUTOMATICA de la puerta esta muerta aunque el fichero este ahi.")
        print("   Se arregla con:  bash tools/install-hooks.sh")
        sys.exit(1)

    try:
        tengo = enganche.read_text(encoding='utf-8')
    except Exception as e:  # noqa: BLE001 - fallar CERRADO: ilegible no es "coinciden"
        roto(f"el enganche {enganche} existe pero no puedo leerlo: {e}")

    if tengo.rstrip('\n') != quiero.rstrip('\n'):
        print(f"rc=1 ENGANCHE DISTINTO: {enganche} no es lo que instala "
              f"{pathlib.Path(args.installer).name}.")
        print("   O alguien lo edito a mano, o el instalador cambio y nadie")
        print("   reinstalo: la variante automatica esta ejerciendo OTRA cosa")
        print("   que la manual, que es justo lo que la doctrina prohibe.")
        print("   Se arregla con:  bash tools/install-hooks.sh")
        sys.exit(1)

    print(f"Verde: el enganche instalado es identico al que produce "
          f"{pathlib.Path(args.installer).name}.")


if __name__ == '__main__':
    main()
