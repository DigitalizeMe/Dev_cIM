# validate_shacl.py

import os
import subprocess
import logging
from rdflib import Graph, Namespace, RDF, SH
from construct_queries import CONSTRUCT_BASE, CONSTRUCT_EXTENDED  # Import queries

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
            logger.error(f"Jena SHACL-Tool not found: {jena_shacl_cmd}")
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
            logger.info(f"Conformité: {conforms}")
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
        logger.error(f"Error during Jena SHACL validation: {e}")
        return False

if __name__ == "__main__":
    ABOX_PATH = os.path.join(ABOX_DIR, "OCCP_Pre_2.ttl")
    
    # Load TBox and ABox separately
    tbox_graph = Graph()
    tbox_graph.parse(TBOX_PATH, format="turtle")
    abox_graph = Graph()
    abox_graph.parse(ABOX_PATH, format="turtle")

    # Pre-check for required instants
    pre_check_query = """
        PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
        ASK {
            # Check for a starting instant (e.g., BeginningOfPlanning or SubmissionToReview)
            ?instantStart a ?startType .
            VALUES ?startType { occp:BeginningOfPlanning occp:SubmissionToReview }
            { ?instantStart occp:hasActualTime ?startTime . }
            UNION
            { ?instantStart occp:hasEstimatedTime ?startTime . }
            # Check for an ending instant (e.g., ReviewApproval or ReviewRejection)
            ?instantEnd a ?endType .
            VALUES ?endType { occp:ReviewApproval occp:ReviewRejection }
            { ?instantEnd occp:hasActualTime ?endTime . }
            UNION
            { ?instantEnd occp:hasEstimatedTime ?endTime . }
        }
    """
    if not abox_graph.query(pre_check_query).askAnswer:
        logger.error("PreI-ABox lacks required instants (BeginningOfPlanning and ReviewApproval)!")
        exit(1)

    # Step 1: Apply CONSTRUCT query
    construct_result = abox_graph.query(CONSTRUCT_EXTENDED).graph  # Use base query for PreI_1.ttl
    if len(construct_result) == 0:
        logger.error("CONSTRUCT generated no triples – PreI-ABox or query faulty!")
        exit(1)
    logger.info(f"CONSTRUCT generated {len(construct_result)} triples.")
    for s, p, o in construct_result:
        logger.debug(f"CONSTRUCT Triple: {s} {p} {o}")

    # Combine graphs: ABox + CONSTRUCT (TBox optional, Jena loads it implicitly)
    inferred_graph = Graph()
    inferred_graph += abox_graph  # PreI data
    inferred_graph += construct_result  # CONSTRUCT triples
    logger.info(f"Inferred Graph contains {len(inferred_graph)} triples.")

    # Bind namespaces
    inferred_graph.bind("occp", OCCP)
    inferred_graph.bind("ould", OULD)
    inferred_graph.bind("xsd", XSD)

    inferred_file = os.path.join(BASE_DIR, "OCCP_Post_2_inferred.ttl")
    inferred_graph.serialize(destination=inferred_file, format="turtle")
    logger.info(f"PostI-ABox generated: {inferred_file}")

    # Step 2: SHACL validation
    conforms = perform_shacl_jena_validation(inferred_file)
    if conforms:
        logger.info("Validation successful: PostI conforms to SHACL.")
    else:
        logger.error("Validation failed.")