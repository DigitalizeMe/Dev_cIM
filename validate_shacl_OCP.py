# validate_shacl_OCP.py

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
OCP_TBOX_PATH = os.path.join(BASE_DIR, "Onto/TBOX/OCP_TBOX.ttl")       
OCP_SHAPES_PATH = os.path.join(BASE_DIR, "Onto/SHACL/OCP_SHACL-Shapes.ttl")  
OCP_ABOX_PATH = os.path.join(BASE_DIR, "Onto/ABOX/OCP/OCP_ABOX_13.ttl") 
ABOX_POST_DIR = os.path.join(BASE_DIR, "Onto/ABOX/OCP/POST_ABOX")        
JAVA_EXE = r"G:\Java\JDK_23\bin\java.exe".replace("\\", "/")             
JENA_HOME = os.path.join(BASE_DIR, "apache-jena-5.3.0")                  

OCP = Namespace("http://www.semanticweb.org/DigitalizeMe/ontologies/2025/3/OCP#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
EX = Namespace("http://www.example.de/example#")

def perform_shacl_jena_validation(data_file, shapes_path=OCP_SHAPES_PATH):
    """
    Perform SHACL validation using Apache Jena.
    Args:
        data_file (str): Path to the data file (ABox or inferred ABox).
        shapes_path (str): Path to the SHACL shapes file.
    Returns:
        bool: True if the data conforms to the SHACL shapes, False otherwise.
    """
    try:
        jena_shacl_cmd = os.path.join(JENA_HOME, "bat", "shacl.bat") if os.name == 'nt' else os.path.join(JENA_HOME, "bin", "shacl")
        if not os.path.exists(jena_shacl_cmd):
            logger.error(f"Jena SHACL tool not found: {jena_shacl_cmd}")
            return False

        data_file_jena = data_file.replace("\\", "/")
        shapes_path_jena = shapes_path.replace("\\", "/")
        cmd = [jena_shacl_cmd, "validate", "--data", data_file_jena, "--shapes", shapes_path_jena]

        report_file = os.path.join(BASE_DIR, "validation_report.ttl")
        with open(report_file, "w", encoding="utf-8") as f:
            result = subprocess.run(
                cmd,
                stdout=f,
                stderr=subprocess.PIPE,
                text=True,
                env={**os.environ, "JENA_HOME": JENA_HOME}
            )

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
            logger.info(f"Validation conformity: {conforms}")
            if not conforms:
                seen_errors = set()
                for s, p, o in report_graph.triples((None, SH.result, None)):
                    for result_obj in report_graph.objects(s, SH.result):
                        message = report_graph.value(result_obj, SH.resultMessage) or "No message"
                        focus_node = report_graph.value(result_obj, SH.focusNode) or "Unknown"
                        path = report_graph.value(result_obj, SH.resultPath) or "Unknown"
                        severity = report_graph.value(result_obj, SH.resultSeverity) or "Unknown"
                        error_key = (str(message), str(focus_node), str(path), str(severity))
                        if error_key not in seen_errors:
                            seen_errors.add(error_key)
                            logger.error(
                                f"Validation error: {message} (Focus Node: {focus_node}, Path: {path}, Severity: {severity})"
                            )
            return conforms
        else:
            logger.error("Jena SHACL validation failed with non-zero exit code.")
            return False
    except Exception as e:
        logger.error(f"Error during Jena SHACL validation: {e}")
        return False

def load_and_validate_ocp(input_abox_path=None):
    """
    Load OCP TBox and ABox, perform SHACL validation, and save the inferred ABox.
    Args:
        input_abox_path (str): Optional. Path to the ABox to validate (default: OCP_ABOX_PATH)
    Returns:
        bool: True if validation is successful, False otherwise.
    """
    try:
        abox_path = input_abox_path if input_abox_path else OCP_ABOX_PATH
        for file_path in [OCP_TBOX_PATH, OCP_SHAPES_PATH, abox_path]:
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return False

        # Load TBox
        tbox_graph = Graph()
        tbox_graph.parse(OCP_TBOX_PATH, format="turtle")
        logger.info(f"Loaded TBox: {OCP_TBOX_PATH}")

        # Load ABox
        abox_graph = Graph()
        abox_graph.parse(abox_path, format="turtle")
        logger.info(f"Loaded ABox: {abox_path}")

        inferred_file = os.path.join(ABOX_POST_DIR, "OCP_Post_inferred.ttl")
        inferred_graph = Graph()
        inferred_graph += abox_graph
        inferred_graph.bind("ocp", OCP)
        inferred_graph.bind("xsd", XSD)
        inferred_graph.bind("ex", EX)

        os.makedirs(ABOX_POST_DIR, exist_ok=True)
        inferred_graph.serialize(destination=inferred_file, format="turtle")
        logger.info(f"Inferred ABox saved: {inferred_file}")

        conforms = perform_shacl_jena_validation(inferred_file)
        if conforms:
            logger.info("Validation successful: ABox conforms to SHACL shapes.")
        else:
            logger.error("Validation failed: ABox does not conform.")
        return conforms

    except Exception as e:
        logger.error(f"Error during OCP validation: {e}")
        return False

if __name__ == "__main__":
    os.makedirs(ABOX_POST_DIR, exist_ok=True)
    conforms = load_and_validate_ocp()
    print(f"Validation Conforms: {conforms}")
