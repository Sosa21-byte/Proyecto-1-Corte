# -*- coding: utf-8 -*-
# pepper_expo_full.py
#
# Ejecuta varios .txt con animaciones incrustadas en orden.
# Uso:
#   python pepper_expo_full.py --ip 192.168.0.106

import qi, argparse, time, sys

# Lista de archivos de exposición (ajusta los nombres si quieres)
ARCHIVOS = [
    "expo_pepper.txt",       # Explain_2: materiales programables
    "expo_metaverso.txt",    # Explain_1: metaverso interoperable
    "expo_biohibridos.txt"   # Explain_3: robots biohíbridos
]

def leer_archivo(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main(ip, port):
    app = qi.Application(["pepper_expo_full", "--qi-url=tcp://{}:{}".format(ip, port)])
    app.start()
    session = app.session

    anim_say = session.service("ALAnimatedSpeech")
    tts = session.service("ALTextToSpeech")

    # Estado recomendado
    try:
        life = session.service("ALAutonomousLife")
        life.setState("solitary")
    except Exception:
        pass

    # Configuración de idioma/volumen
    try:
        tts.setLanguage("Spanish")
    except Exception:
        pass
    tts.setParameter("volume", 0.9)

    # Desactivar gestos automáticos (solo usamos los que marcamos en los .txt)
    try:
        anim_say.setBodyLanguageModeFromStr("disabled")
    except Exception:
        pass

    # Recorre los archivos en orden
    for i, archivo in enumerate(ARCHIVOS, 1):
        try:
            texto = leer_archivo(archivo)
        except Exception as e:
            print("Error leyendo {}: {}".format(archivo, e), file=sys.stderr)
            continue

        print(">> [Pepper] Iniciando bloque {}: {}".format(i, archivo))
        anim_say.say(texto)

        if i < len(ARCHIVOS):
            print(">> Pausa antes del siguiente bloque...")
            time.sleep(3)  # pausa de transición entre bloques

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", required=True, help="IP de Pepper, ej. 192.168.1.50")
    parser.add_argument("--port", type=int, default=9559, help="Puerto NAOqi (default 9559)")
    args = parser.parse_args()

    try:
        main(args.ip, args.port)
    except KeyboardInterrupt:
        sys.exit(0)
