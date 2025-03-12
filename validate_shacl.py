import owlready2
from rdflib import Graph, Namespace, RDF
from rdflib.namespace import SH, OWL
import logging
import os
import sys
import subprocess
import json
import shutil
from io import StringIO

# Konfiguration des Loggings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(
    filename=os.path.join(BASE_DIR, "validation.log"),
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w"
)

# Logging-Setup (falls nicht schon vorhanden)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pfade und Namespace
TBOX_PATH = os.path.join(BASE_DIR, "OCCP_V0.3.ttl")
ABOX_DIR = os.path.join(BASE_DIR, "OCCP_ABox")
SHAPES_PATH = os.path.join(BASE_DIR, "OCCP_SHACL_min.ttl")
JAVA_EXE = r"G:\Java\JDK_23\bin\java.exe".replace("\\", "/")
JENA_HOME = os.path.join(BASE_DIR, "apache-jena-5.3.0")  # Hauptverzeichnis der Jena-Installation
OULD = Namespace("http://www.semanticweb.org/albrechtvaatz/ontologies/2024/OULD#")
OCCP = Namespace("http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#")

def combine_and_reason(tbox_path=TBOX_PATH, abox_path=None, java_exe=JAVA_EXE):
    try:
        tbox_path_normalized = tbox_path.replace("\\", "/")
        abox_path_normalized = abox_path.replace("\\", "/") if abox_path else None
        onto = owlready2.get_ontology(f"file://{tbox_path_normalized}").load(format="turtle")
        if abox_path:
            abox_onto = owlready2.get_ontology(f"file://{abox_path_normalized}").load(format="turtle")
            with onto:
                for indiv in abox_onto.individuals():
                    new_indiv = onto.get_entities(indiv.name, indiv.__class__)
                    if not new_indiv:
                        new_indiv = indiv.__class__(indiv.name, namespace=onto)
                    for prop in indiv.get_properties():
                        for value in prop[indiv]:
                            prop[new_indiv] = value
                owlready2.sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True, debug=2)
        data_graph = Graph()
        data_graph.parse(tbox_path, format="turtle")
        if abox_path:
            data_graph.parse(abox_path, format="turtle")
        output_file = os.path.join(BASE_DIR, "inferred_ontology.ttl")
        data_graph.serialize(destination=output_file, format="turtle")
        logger.info(f"Inferierte Ontologie gespeichert: {output_file}")
        # Generische Disjunktheitsprüfung
        logger.info("Prüfe Ontologie auf Disjunktheit...")
        disjoint_pairs = set()
        for s, p, o in data_graph.triples((None, OWL.disjointWith, None)):
            disjoint_pairs.add((s, o))
            disjoint_pairs.add((o, s))  # Bidirektional
        logger.debug(f"Disjunkte Klassenpaare: {disjoint_pairs}")
        for subj in data_graph.subjects(RDF.type, None):
            types = set(o for s, p, o in data_graph.triples((subj, RDF.type, None)))
            for class1, class2 in disjoint_pairs:
                if class1 in types and class2 in types:
                    logger.error(f"Disjunktheitsverletzung gefunden: {subj} hat Typen {class1} und {class2}")
                    raise Exception(f"Ontology is inconsistent: {subj} has disjoint types {class1} and {class2}")
        logger.info("Keine Disjunktheitsverletzungen gefunden.")
        return output_file
    except Exception as e:
        logger.error(f"Fehler beim Reasoning oder Disjunktheitsprüfung: {e}")
        raise

def debug_sparql(data_file):
    try:
        data_graph = Graph().parse(data_file, format="turtle")
        query = """
            PREFIX ould: <http://www.semanticweb.org/albrechtvaatz/ontologies/2024/OULD#>
            SELECT ?chain (COUNT(?u) AS ?updateCount)
            WHERE {
                ?chain a ould:UpdateChain .
                ?chain ould:hasUpdate ?u .
            }
            GROUP BY ?chain
        """
        logger.info("Starte SPARQL-Abfrage für alle UpdateChains...")
        results = data_graph.query(query)
        logger.info("SPARQL-Abfrage Ergebnisse:")
        for row in results:
            logger.info(f"Chain: {row.chain}, UpdateCount: {row.updateCount}")
        return len(results) > 0
    except Exception as e:
        logger.error(f"Fehler bei der SPARQL-Abfrage: {e}")
        raise

def perform_shacl_jena_validation(data_file, shapes_path=SHAPES_PATH):
    try:
        # Suche shacl im PATH
        jena_shacl_cmd = shutil.which("shacl")
        if not jena_shacl_cmd:
            # Fallback: Versuche den direkten Pfad
            jena_shacl_cmd = os.path.join(JENA_HOME, "bin", "shacl.bat") if os.name == 'nt' else os.path.join(JENA_HOME, "bin", "shacl")
            if not os.path.exists(jena_shacl_cmd):
                logger.error(f"Jena SHACL-Tool nicht gefunden: {jena_shacl_cmd}")
                return False

        # Konvertiere Pfade für Jena (Backslashes zu Schrägstrichen)
        data_file_jena = data_file.replace("\\", "/")
        shapes_path_jena = shapes_path.replace("\\", "/")

        # Schreibe die Ausgabe in eine temporäre Datei
        report_file = os.path.join(BASE_DIR, "validation_report.ttl")
        cmd = [
            jena_shacl_cmd,
            "validate",
            "--data", data_file_jena,
            "--shapes", shapes_path_jena
        ]
        with open(report_file, "w", encoding="utf-8") as f:
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True, env={**os.environ, "JENA_HOME": JENA_HOME})

        # Logge stderr
        if result.stderr:
            logger.error(f"Jena SHACL validation stderr: {result.stderr}")

        if result.returncode == 0:
            # Lese die Ausgabe aus der Datei
            with open(report_file, "r", encoding="utf-8") as f:
                report_data = f.read()
            logger.info(f"Jena SHACL validation stdout: {report_data}")

            # Parse die Turtle-Ausgabe mit rdflib
            report_graph = Graph()
            report_graph.parse(data=report_data, format="turtle")
            conforms = False
            for s, p, o in report_graph.triples((None, SH.conforms, None)):
                conforms = o.toPython()  # o sollte ein Literal mit "true" oder "false" sein
            logger.info(f"Konformität (inference=none): {conforms}")
            if not conforms:
                # Extrahiere Ergebnisse für detaillierte Fehler
                for s, p, o in report_graph.triples((None, SH.result, None)):
                    for result_obj in report_graph.objects(s, SH.result):
                        message = report_graph.value(result_obj, SH.message) or "No message"
                        focus_node = report_graph.value(result_obj, SH.focusNode) or "Unknown"
                        path = report_graph.value(result_obj, SH.path) or "Unknown"
                        severity = report_graph.value(result_obj, SH.severity) or "Unknown"
                        logger.error(f"Validation error: {message} (Focus Node: {focus_node}, Path: {path}, Severity: {severity})")
            return conforms
        else:
            logger.error("Jena SHACL validation failed with non-zero exit code.")
            return False
    except Exception as e:
        logger.error(f"Fehler bei der Jena SHACL-Validierung: {e}")
        return False

if __name__ == "__main__":
    ABOX_PATH = os.path.join(ABOX_DIR, "OCCP_Valid_LCycle_1.ttl")
    inferred_file = combine_and_reason(tbox_path=TBOX_PATH, abox_path=ABOX_PATH, java_exe=JAVA_EXE)
    debug_sparql(inferred_file)
    conforms = perform_shacl_jena_validation(inferred_file)

    if conforms:
        logger.info("Validation successful: Conforms to SHACL.")
    else:
        logger.error("Validation failed.")