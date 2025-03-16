import os
import subprocess
import logging
from rdflib import Graph, Namespace, RDF, SH

# Konfiguration des Loggings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(
    filename=os.path.join(BASE_DIR, "validation.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w"
)
logger = logging.getLogger(__name__)

# Pfade und Namespace
TBOX_PATH = os.path.join(BASE_DIR, "OCCP_V0.3.ttl")
ABOX_DIR = os.path.join(BASE_DIR, "OCCP_ABox")
SHAPES_PATH = os.path.join(BASE_DIR, "OCCP_SHACL_V1.3.ttl")
JAVA_EXE = r"G:\Java\JDK_23\bin\java.exe".replace("\\", "/")
JENA_HOME = os.path.join(BASE_DIR, "apache-jena-5.3.0")
OCCP = Namespace("http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#")
OULD = Namespace("http://www.semanticweb.org/albrechtvaatz/ontologies/2024/OULD#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")

def perform_shacl_jena_validation(data_file, shapes_path=SHAPES_PATH):
    try:
        jena_shacl_cmd = os.path.join(JENA_HOME, "bat", "shacl.bat") if os.name == 'nt' else os.path.join(JENA_HOME, "bin", "shacl")
        if not os.path.exists(jena_shacl_cmd):
            logger.error(f"Jena SHACL-Tool nicht gefunden: {jena_shacl_cmd}")
            return False

        data_file_jena = data_file.replace("\\", "/")
        shapes_path_jena = shapes_path.replace("\\", "/")
        report_file = os.path.join(BASE_DIR, "validation_report.ttl")
        cmd = [
            jena_shacl_cmd,
            "validate",
            "--data", data_file_jena,
            "--shapes", shapes_path_jena
        ]
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
            logger.info(f"Konformität: {conforms}")
            if not conforms:
                for s, p, o in report_graph.triples((None, SH.result, None)):
                    for result_obj in report_graph.objects(s, SH.result):
                        message = report_graph.value(result_obj, SH.resultMessage) or "No specific message"
                        focus_node = report_graph.value(result_obj, SH.focusNode) or "Unknown"
                        path = report_graph.value(result_obj, SH.resultPath) or "Unknown"
                        severity = report_graph.value(result_obj, SH.resultSeverity) or "Unknown"
                        logger.error(f"Validation error: {message} (Focus Node: {focus_node}, Path: {path}, Severity: {severity})")
            return conforms
        else:
            logger.error("Jena SHACL validation failed with non-zero exit code.")
            return False
    except Exception as e:
        logger.error(f"Fehler bei der Jena SHACL-Validierung: {e}")
        return False

if __name__ == "__main__":
    ABOX_PATH = os.path.join(ABOX_DIR, "OCCP_Pre_1.ttl")
    
    # TBox und ABox getrennt laden
    tbox_graph = Graph()
    tbox_graph.parse(TBOX_PATH, format="turtle")
    abox_graph = Graph()
    abox_graph.parse(ABOX_PATH, format="turtle")

    # Leichte Vorabprüfung
    pre_check_query = """
        PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
        ASK {
            ?instant a occp:BeginningOfPlanning ;
                     occp:hasActualTime ?time .
        }
    """
    if not abox_graph.query(pre_check_query).askAnswer:
        logger.error("PreI-ABox enthält keinen BeginningOfPlanning-Instant mit Zeitangabe!")
        exit(1)

    # Schritt 1: SPARQL Construct nur auf ABox
    construct_query = """
        PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
        CONSTRUCT {
            ?phase occp:hasActualBeginning ?instantStart .
            ?cycle occp:hasActualBeginning ?instantStart .
            ?cycle occp:isInPhase ?phase .
            ?cycle occp:hasCycleNumber ?cycleNumber .
            ?instantEnd occp:endsPhase ?phase .
            ?instantEnd occp:endsCycle ?cycle .
            ?phase occp:hasEstimatedEnd ?instantEnd .
            ?cycle occp:hasEstimatedEnd ?instantEnd .
        }
        WHERE {
            ?instantStart a occp:BeginningOfPlanning ;
                occp:startsPhase ?phase ;
                occp:startsCycle ?cycle ;
                occp:hasActualTime ?startTime .
            ?component occp:hasPhase ?phase ;
                occp:hasCycle ?cycle .
            ?instantEnd a occp:ReviewApproval ;
                occp:endsPhase ?phase ;
                occp:endsCycle ?cycle ;
                occp:hasEstimatedTime ?endTime .
            OPTIONAL {
                ?cycle occp:hasCycleNumber ?existingNumber .
            }
            BIND(COALESCE(?existingNumber, 1) AS ?cycleNumber)
        }
    """
    construct_result = abox_graph.query(construct_query).graph
    logger.info(f"CONSTRUCT hat {len(construct_result)} Triple erzeugt.")
    for s, p, o in construct_result:
        logger.debug(f"CONSTRUCT Triple: {s} {p} {o}")

    # inferred_graph: Nur ABox + CONSTRUCT
    inferred_graph = Graph()
    inferred_graph += abox_graph  # Nur PreI-Daten
    inferred_graph += construct_result  # CONSTRUCT-Triple
    logger.info(f"Inferred Graph hat {len(inferred_graph)} Triple.")

    # Namespace binden
    inferred_graph.bind("occp", OCCP)
    inferred_graph.bind("ould", OULD)
    inferred_graph.bind("xsd", XSD)

    if len(inferred_graph) == 0:
        logger.error("Inferred Graph ist leer – PreI-ABox oder CONSTRUCT fehlerhaft!")
        exit(1)
    inferred_file = os.path.join(BASE_DIR, "OCCP_Post_1_inferred.ttl")
    inferred_graph.serialize(destination=inferred_file, format="turtle")
    logger.info(f"PostI-ABox erzeugt: {inferred_file}")

    # Schritt 2: SHACL-Validierung (TBox wird von Jena implizit geladen)
    conforms = perform_shacl_jena_validation(inferred_file)
    if conforms:
        logger.info("Validation successful: PostI conforms to SHACL.")
    else:
        logger.error("Validation failed.")