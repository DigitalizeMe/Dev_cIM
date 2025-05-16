import os
import subprocess
import logging
from rdflib import Graph, Namespace, SH

# Logging configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(
    filename=os.path.join(BASE_DIR, "validation.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w"
)
logger = logging.getLogger(__name__)

# Paths and namespaces
OCCP_TBOX_PATH = os.path.join(BASE_DIR, "OCCP_TBOX_V2.3p.ttl")  
OCCP_SHAPES_PATH = os.path.join(BASE_DIR, "OCCP_SHACL_V1.8.ttl")  
ABOX_DIR = os.path.join(BASE_DIR, "OCCP_ABox")
ABOX_POST_DIR = os.path.join(ABOX_DIR, "POST_ABOX")
JAVA_EXE = r"G:\Java\JDK_23\bin\java.exe".replace("\\", "/")
JENA_HOME = os.path.join(BASE_DIR, "apache-jena-5.3.0")
OCCP = Namespace("http://www.semanticweb.org/DigitalizeMe/ontologies/2022/9/cMod_V0.1#")
OULD = Namespace("http://www.semanticweb.org/DigitalizeMe/ontologies/2024/OULD#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
EX = Namespace("http://www.example.de/example#")  

# ABox-Pfad (anpassbar, falls online oder lokal)
ABOX_PATH = os.path.join(ABOX_DIR, "OCCP_Pre_ABOX.ttl")  # Lokaler Pfad
# Falls online verwendet werden soll:
# ABOX_PATH = "https://raw.githubusercontent.com/DigitalizeMe/12071923_Dev/refs/heads/main/OCCP_ABox/OCCP_Pre_ABOX.ttl"

def perform_shacl_jena_validation(data_file, shapes_paths=[OCCP_SHAPES_PATH]):
    """
    Führt eine SHACL-Validierung mit Jena SHACL durch.
    :param data_file: Pfad zur ABox-Datei
    :param shapes_paths: Liste der SHACL-Shapes-Dateien (Standard: nur OCCP_SHAPES)
    :return: Boolean, ob die Validierung erfolgreich war
    """
    try:
        jena_shacl_cmd = os.path.join(JENA_HOME, "bat", "shacl.bat") if os.name == 'nt' else os.path.join(JENA_HOME, "bin", "shacl")
        if not os.path.exists(jena_shacl_cmd):
            logger.error(f"Jena SHACL-Tool nicht gefunden: {jena_shacl_cmd}")
            return False

        data_file_jena = data_file.replace("\\", "/")
        cmd = [jena_shacl_cmd, "validate", "--data", data_file_jena]
        for shapes_path in shapes_paths:
            shapes_path_jena = shapes_path.replace("\\", "/")
            cmd.extend(["--shapes", shapes_path_jena])
        
        report_file = os.path.join(BASE_DIR, "validation_report.ttl")
        with open(report_file, "w", encoding="utf-8") as f:
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True, env={**os.environ, "JENA_HOME": JENA_HOME})

        if result.stderr:
            logger.error(f"Jena SHACL validation stderr: {result.stderr}")

        if result.returncode == 0:
            with open(report_file, "r", encoding="utf-8") as f:
                report_data = f.read()
            logger.debug(f"SHACL Report: {report_data}")
            report_graph = Graph()
            report_graph.parse(data=report_data, format="turtle")
            conforms = False
            for s, p, o in report_graph.triples((None, SH.conforms, None)):
                conforms = o.toPython()
            logger.info(f"Conformity: {conforms}")
            if not conforms:
                seen_errors = set()
                for s, p, o in report_graph.triples((None, SH.result, None)):
                    for result_obj in report_graph.objects(s, SH.result):
                        message = report_graph.value(result_obj, SH.resultMessage) or "Kein spezifisches Message"
                        focus_node = report_graph.value(result_obj, SH.focusNode) or "Unbekannt"
                        path = report_graph.value(result_obj, SH.resultPath) or "Unbekannt"
                        severity = report_graph.value(result_obj, SH.resultSeverity) or "Unbekannt"
                        error_key = (str(message), str(focus_node), str(path), str(severity))
                        if error_key not in seen_errors:
                            seen_errors.add(error_key)
                            logger.error(f"Validation error: {message} (Focus Node: {focus_node}, Path: {path}, Severity: {severity})")
            return conforms
        else:
            logger.error("Jena SHACL validation fehlgeschlagen mit nicht-null Exit-Code.")
            return False
    except Exception as e:
        logger.error(f"Fehler während der Jena SHACL-Validierung: {e}")
        return False

def main():
    """Hauptfunktion zur Validierung der ABox."""
    logger.info("Starte SHACL-Validierung der ABox...")

    # Prüfen, ob die ABox existiert
    if not os.path.exists(ABOX_PATH):
        logger.error(f"ABox-Datei nicht gefunden: {ABOX_PATH}")
        print(f"Fehler: ABox-Datei nicht gefunden: {ABOX_PATH}")
        return

    # Validierung durchführen (nur OCCP_SHAPES, OULD optional hinzufügbar)
    shapes_paths = [OCCP_SHAPES_PATH]  # Standard: nur OCCP_SHAPES
    # Falls OULD_SHAPES auch verwendet werden soll, uncomment:
    # shapes_paths.append(OULD_SHAPES_PATH)

    logger.info(f"Validiere {ABOX_PATH} gegen {shapes_paths}")
    conforms = perform_shacl_jena_validation(ABOX_PATH, shapes_paths)

    # Ergebnis ausgeben
    if conforms:
        logger.info("Validierung erfolgreich! Die ABox entspricht den SHACL-Shapes.")
        print("Validierung erfolgreich! Die ABox entspricht den SHACL-Shapes.")
    else:
        logger.info("Validierung fehlgeschlagen. Siehe validation.log für Details.")
        print("Validierung fehlgeschlagen. Siehe validation.log für Details.")

if __name__ == "__main__":
    main()