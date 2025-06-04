# validate_shacl_34_OCP.py

import os
import subprocess
import logging
from rdflib import Graph, Namespace, RDF, SH
# Note: construct_queries is not used unless CONSTRUCT queries are needed
# from construct_queries import generate_post_graph

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
OCP_TBOX_PATH = os.path.join(BASE_DIR, "Onto/TBOX/OCP_TBOX.ttl")  # Path to OCP TBOX
OCP_SHAPES_PATH = os.path.join(BASE_DIR, "Onto/SHACL/OCP_SHACL-Shapes.ttl")  # Path to OCP SHACL shapes
OCP_ABOX_PATH = os.path.join(BASE_DIR, "Onto/ABOX/OCP/OCP_ABOX_12.ttl")  # Path to OCP ABOX
ABOX_POST_DIR = os.path.join(BASE_DIR, "Onto/ABOX/OCP/POST_ABOX")  # Directory for inferred ABOX
JAVA_EXE = r"G:\Java\JDK_23\bin\java.exe".replace("\\", "/")  # Path to Java executable
JENA_HOME = os.path.join(BASE_DIR, "apache-jena-5.3.0")  # Path to Jena installation
OCP = Namespace("http://www.semanticweb.org/DigitalizeMe/ontologies/2025/3/OCP#")  # OCP namespace
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")  # XSD namespace
EX = Namespace("http://www.example.de/example#")  # Example namespace

def perform_shacl_jena_validation(data_file, shapes_path=OCP_SHAPES_PATH):
    """
    Perform SHACL validation using Apache Jena.
    Args:
        data_file (str): Path to the data file (ABOX or inferred ABOX).
        shapes_path (str): Path to the SHACL shapes file.
    Returns:
        bool: True if the data conforms to the SHACL shapes, False otherwise.
    """
    try:
        # Check if Jena SHACL tool exists
        jena_shacl_cmd = os.path.join(JENA_HOME, "bat", "shacl.bat") if os.name == 'nt' else os.path.join(JENA_HOME, "bin", "shacl")
        if not os.path.exists(jena_shacl_cmd):
            logger.error(f"Jena SHACL-Tool not found: {jena_shacl_cmd}")
            return False

        # Prepare command for Jena SHACL validation
        data_file_jena = data_file.replace("\\", "/")
        shapes_path_jena = shapes_path.replace("\\", "/")
        cmd = [jena_shacl_cmd, "validate", "--data", data_file_jena, "--shapes", shapes_path_jena]
        
        # Run validation and save report
        report_file = os.path.join(BASE_DIR, "validation_report.ttl")
        with open(report_file, "w", encoding="utf-8") as f:
            result = subprocess.run(
                cmd,
                stdout=f,
                stderr=subprocess.PIPE,
                text=True,
                env={**os.environ, "JENA_HOME": JENA_HOME}
            )

        # Log any stderr output
        if result.stderr:
            logger.error(f"Jena SHACL validation stderr: {result.stderr}")

        # Check if validation was successful
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

def load_and_validate_ocp():
    """
    Load OCP TBOX and ABOX, perform SHACL validation, and optionally apply CONSTRUCT queries.
    Returns:
        bool: True if validation is successful, False otherwise.
    """
    try:
        # Check if input files exist
        for file_path in [OCP_TBOX_PATH, OCP_SHAPES_PATH, OCP_ABOX_PATH]:
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return False

        # Load TBox
        tbox_graph = Graph()
        tbox_graph.parse(OCP_TBOX_PATH, format="turtle")
        logger.info(f"Loaded TBox: {OCP_TBOX_PATH}")

        # Load ABox
        abox_graph = Graph()
        abox_graph.parse(OCP_ABOX_PATH, format="turtle")
        logger.info(f"Loaded ABox: {OCP_ABOX_PATH}")

        # Optional: Apply CONSTRUCT queries (disabled by default)
        inferred_file = os.path.join(ABOX_POST_DIR, "OCP_Post_inferred.ttl")
        inferred_graph = Graph()
        inferred_graph += abox_graph
        inferred_graph.bind("ocp", OCP)
        inferred_graph.bind("xsd", XSD)
        inferred_graph.bind("ex", EX)

        # Note: Uncomment the following lines to enable CONSTRUCT queries
        # construct_result = generate_post_graph(OCP_ABOX_PATH, inferred_file)
        # if len(construct_result) == 0:
        #     logger.error("CONSTRUCT generated no triples – ABox or query faulty!")
        #     return False
        # logger.info(f"CONSTRUCT generated {len(construct_result)} triples.")
        # for s, p, o in construct_result:
        #     logger.debug(f"CONSTRUCT Triple: {s} {p} {o}")
        # inferred_graph += construct_result

        # Save inferred graph
        os.makedirs(ABOX_POST_DIR, exist_ok=True)
        inferred_graph.serialize(destination=inferred_file, format="turtle")
        logger.info(f"Inferred ABox saved: {inferred_file}")

        # Perform SHACL validation
        conforms = perform_shacl_jena_validation(inferred_file)
        if conforms:
            logger.info("Validation successful: ABox conforms to SHACL.")
        else:
            logger.error("Validation failed.")
        return conforms

    except Exception as e:
        logger.error(f"Error during OCP validation: {e}")
        return False

if __name__ == "__main__":
    # Ensure POST_ABOX directory exists
    os.makedirs(ABOX_POST_DIR, exist_ok=True)
    
    # Run validation
    conforms = load_and_validate_ocp()
    print(f"Validation Conforms: {conforms}")