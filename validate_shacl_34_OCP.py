# validate_shacl_34.py

import os
import subprocess
import logging
from rdflib import Graph, Namespace, RDF, SH
from construct_queries import generate_post_graph  # Neue Funktion importieren

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
OULD_TBOX_PATH = os.path.join(BASE_DIR, "OULD_TBOX_V1.7.ttl")  
OULD_SHAPES_PATH = os.path.join(BASE_DIR, "OULD_SHACL_V1.2.ttl")  
OCCP_TBOX_PATH = os.path.join(BASE_DIR, "OCP_TBOX.ttl")  
OCCP_SHAPES_PATH = os.path.join(BASE_DIR, "OCP_SHACL-Shapes.ttl")  
ABOX_DIR = os.path.join(BASE_DIR)
ABOX_POST_DIR = os.path.join(ABOX_DIR, "POST_ABOX")
JAVA_EXE = r"G:\Java\JDK_23\bin\java.exe".replace("\\", "/")
JENA_HOME = os.path.join(BASE_DIR, "apache-jena-5.3.0")
OCP = Namespace("http://www.semanticweb.org/DigitalizeMe/ontologies/2025/3/OCP#")
OULD = Namespace("http://www.semanticweb.org/DigitalizeMe/ontologies/2024/OULD#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
EX = Namespace("http://www.example.de/example#")  

def perform_shacl_jena_validation(data_file, shapes_paths=[OCCP_SHAPES_PATH, OULD_SHAPES_PATH]):
    try:
        jena_shacl_cmd = os.path.join(JENA_HOME, "bat", "shacl.bat") if os.name == 'nt' else os.path.join(JENA_HOME, "bin", "shacl")
        if not os.path.exists(jena_shacl_cmd):
            logger.error(f"Jena SHACL-Tool not found: {jena_shacl_cmd}")
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
                        message = report_graph.value(result_obj, SH.resultMessage) or "No specific message"
                        focus_node = report_graph.value(result_obj, SH.focusNode) or "Unknown"
                        path = report_graph.value(result_obj, SH.resultPath) or "Unknown"
                        severity = report_graph.value(result_obj, SH.resultSeverity) or "Unknown"
                        error_key = (str(message), str(focus_node), str(path), str(severity))
                        if error_key not in seen_errors:
                            seen_errors.add(error_key)
                            logger.error(f"Validation error: {message} (Focus Node: {focus_node}, Path: {path}, Severity: {severity})")
            return conforms
        else:
            logger.error("Jena SHACL validation failed with non-zero exit code.")
            return False
    except Exception as e:
        logger.error(f"Error during Jena SHACL validation: {e}")
        return False

if __name__ == "__main__":
     
     # Variable for testing efficiency
    part_name3 = "Site"  

    ABox_Pre_file = f"OCCP_Pre_{part_name3}.ttl"

    ABOX_PATH = os.path.join(ABOX_DIR, ABox_Pre_file)
    
    # Load TBox (OCCP and OULD)
    tbox_graph = Graph()
    tbox_graph.parse(OCCP_TBOX_PATH, format="turtle")
    tbox_graph.parse(OULD_TBOX_PATH, format="turtle") 

    # Load ABox
    abox_graph = Graph()
    abox_graph.parse(ABOX_PATH, format="turtle")



    # Step 1: Apply CONSTRUCT queries using the new function
    ABox_Post_file = f"OCCP_Post_{part_name3}_inferred.ttl"
    inferred_file = os.path.join(ABOX_POST_DIR, ABox_Post_file)
    construct_result = generate_post_graph(ABOX_PATH, inferred_file)
    if len(construct_result) == 0:
        logger.error("CONSTRUCT generated no triples – PreI-ABox or query faulty!")
        exit(1)
    logger.info(f"CONSTRUCT generated {len(construct_result)} triples.")
    for s, p, o in construct_result:
        logger.debug(f"CONSTRUCT Triple: {s} {p} {o}")

    # Combine graphs: TBox (optional) + ABox + CONSTRUCT
    inferred_graph = Graph()
    inferred_graph += abox_graph
    inferred_graph += construct_result
    inferred_graph.bind("occp", OCCP)
    inferred_graph.bind("ould", OULD)
    inferred_graph.bind("xsd", XSD)
    inferred_graph.bind("ex", EX)  

    # Save inferred graph 
    inferred_graph.serialize(destination=inferred_file, format="turtle")
    logger.info(f"PostI-ABox generated: {inferred_file}")

    # Step 2: SHACL validation
    conforms = perform_shacl_jena_validation(inferred_file)
    if conforms:
        logger.info("Validation successful: PostI conforms to SHACL.")
    else:
        logger.error("Validation failed.")