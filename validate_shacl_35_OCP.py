# validate_shacl_35_OCP.py 

import os
import subprocess
import logging
from rdflib import Graph, Namespace, RDF, SH

# Logging configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(
    filename=os.path.join(BASE_DIR, "validation.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w"
)
logger = logging.getLogger(__name__)

# Relative Pfade zu kombinierten Dateien
COMBINED_TBOX_PATH = os.path.join("Onto", "TBOX", "TIME+OCP_TBOX.ttl")
OCP_SHAPES_PATH = os.path.join("Onto", "SHACL", "OCP_SHACL-Shapes.ttl")
OCP_ABOX_PATH = os.path.join("Onto", "ABOX", "OCP", "OCP_ABOX_13.ttl")
REASONER_OUT_DIR = os.path.join("Onto", "ABOX", "OCP", "POST_ABOX", "Reasoner")
INFERRED_ABOX_PATH = os.path.join(REASONER_OUT_DIR, "OCP_ABOX_13_inferred.ttl")
JENA_HOME = os.path.join("apache-jena-5.3.0")

OCP = Namespace("http://www.semanticweb.org/DigitalizeMe/ontologies/2025/3/OCP#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
EX = Namespace("http://www.example.de/example#")


def perform_jena_reasoning(data_file, tbox_file, output_file):
    if os.name == 'nt':
        reasoner_cmd = os.path.join(JENA_HOME, "bat", "infer.bat")
    else:
        reasoner_cmd = os.path.join(JENA_HOME, "bin", "jena")

    if not os.path.exists(reasoner_cmd):
        logger.error(f"Jena reasoner not found at {reasoner_cmd}")
        return False

    if not os.path.exists(tbox_file):
        logger.error(f"Missing combined TBox file: {tbox_file}")
        return False

    if not os.path.exists(data_file):
        logger.error(f"Missing ABox file: {data_file}")
        return False

    cmd = f'"{reasoner_cmd}" --data "{data_file}" --tbox "{tbox_file}" --out TTL > "{output_file}"'
    logger.info(f"Starting Jena reasoning with command: {cmd}")

    try:
        result = subprocess.run(cmd, shell=True)
        if result.returncode != 0:
            logger.error("Jena reasoning failed with non-zero exit code.")
            return False
        if not os.path.exists(output_file):
            logger.error(f"Inferred ABox was not created at expected path: {output_file}")
            return False
        logger.info(f"Reasoning completed successfully. Output written to: {output_file}")
        return True
    except Exception as e:
        logger.error(f"Jena reasoning subprocess error: {e}")
        return False


def perform_shacl_jena_validation(data_file, shapes_path=OCP_SHAPES_PATH):
    jena_shacl_cmd = os.path.join(JENA_HOME, "bat", "shacl.bat") if os.name == 'nt' else os.path.join(JENA_HOME, "bin", "shacl")

    if not os.path.exists(jena_shacl_cmd):
        logger.error(f"Jena SHACL tool not found: {jena_shacl_cmd}")
        return False

    report_file = "validation_report.ttl"
    cmd = f'"{jena_shacl_cmd}" validate --data "{data_file}" --shapes "{shapes_path}"'

    try:
        with open(report_file, "w", encoding="utf-8") as f:
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True, shell=True)

        if result.stderr:
            logger.warning(f"SHACL stderr: {result.stderr}")

        if result.returncode == 0:
            report_graph = Graph()
            with open(report_file, "r", encoding="utf-8") as f:
                report_data = f.read()
            report_graph.parse(data=report_data, format="turtle")
            conforms = False
            for s, p, o in report_graph.triples((None, SH.conforms, None)):
                conforms = o.toPython()
            logger.info(f"SHACL Validation Conformity: {conforms}")
            return conforms
        else:
            logger.error("SHACL validation failed (non-zero exit code).")
            return False
    except Exception as e:
        logger.error(f"SHACL validation error: {e}")
        return False


def load_and_validate_ocp():
    os.makedirs(REASONER_OUT_DIR, exist_ok=True)

    if not all(os.path.exists(p) for p in [OCP_ABOX_PATH, COMBINED_TBOX_PATH, OCP_SHAPES_PATH]):
        logger.error("Required input file(s) missing.")
        return False

    logger.info("Starting reasoning and validation process...")

    if not perform_jena_reasoning(OCP_ABOX_PATH, COMBINED_TBOX_PATH, INFERRED_ABOX_PATH):
        logger.error("OWL reasoning failed. Aborting validation.")
        return False

    conforms = perform_shacl_jena_validation(INFERRED_ABOX_PATH)
    return conforms


if __name__ == "__main__":
    result = load_and_validate_ocp()
    print(f"Validation Conforms: {result}")
