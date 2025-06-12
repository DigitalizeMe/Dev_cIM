# convert_ttl_to_rdfxml.py

from rdflib import Graph
import os

def convert_ttl_to_rdfxml(input_path, output_path=None):
    if not os.path.exists(input_path):
        print(f"Datei nicht gefunden: {input_path}")
        return False

    g = Graph()
    try:
        g.parse(input_path, format="turtle")
    except Exception as e:
        print(f"Fehler beim Parsen von {input_path}: {e}")
        return False

    if not output_path:
        # Erzeuge .owl-Dateiname
        output_path = os.path.splitext(input_path)[0] + ".owl"

    try:
        g.serialize(destination=output_path, format="xml")
        print(f"Erfolgreich konvertiert: {input_path} → {output_path}")
        return True
    except Exception as e:
        print(f"Fehler beim Schreiben von {output_path}: {e}")
        return False

if __name__ == "__main__":
    # Beispielaufruf
    # Passe hier die Pfade an:
    ttl_files = [
        "Onto/TBOX/TIME_TBOX.ttl",
    ]
    for file in ttl_files:
        convert_ttl_to_rdfxml(file)
