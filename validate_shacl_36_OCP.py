# validate_shacl_36_OCP.py

import os
import subprocess
import logging
from rdflib import Graph, Namespace, RDF, SH, URIRef
from owlready2 import get_ontology, sync_reasoner_pellet, default_world
from rdflib.plugins.sparql import prepareQuery

# Logging configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
logging.basicConfig(
    filename=os.path.join(BASE_DIR, "validation.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w"
)
logger = logging.getLogger(__name__)

# Paths and namespaces
OCP_TBOX_PATH = os.path.join(BASE_DIR, "Onto/TBOX/OCP_TBOX.ttl").replace("\\", "/")
OCP_SHAPES_PATH = os.path.join(BASE_DIR, "Onto/SHACL/OCP_SHACL-Shapes.ttl").replace("\\", "/")
OCP_ABOX_PATH = os.path.join(BASE_DIR, "Onto/ABOX/OCP/OCP_ABOX_12.ttl").replace("\\", "/")
ABOX_POST_DIR = os.path.join(BASE_DIR, "Onto/ABOX/OCP/POST_ABOX").replace("\\", "/")
REASONER_DIR = os.path.join(ABOX_POST_DIR, "Reasoner").replace("\\", "/")
JAVA_EXE = r"G:\Java\JDK_23\bin\java.exe".replace("\\", "/")
JENA_HOME = os.path.join(BASE_DIR, "apache-jena-5.3.0").replace("\\", "/")
OCP = Namespace("http://www.semanticweb.org/DigitalizeMe/ontologies/2025/3/OCP#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
EX = Namespace("http://www.example.de/example#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
DCTERMS = Namespace("http://purl.org/dc/terms/")
OWL = Namespace("http://www.w3.org/2002/07/owl#")
TIME = Namespace("http://www.w3.org/2006/time#")

def perform_shacl_jena_validation(data_file, shapes_path=OCP_SHAPES_PATH):
    """
    Perform SHACL validation using Apache Jena.
    Args:
        data_file (str): Path to the data file.
        shapes_path (str): Path to the SHACL shapes file.
    Returns:
        tuple: (bool, list) - Conforms status and list of violations.
    """
    try:
        jena_shacl_cmd = os.path.join(JENA_HOME, "bat", "shacl.bat") if os.name == 'nt' else os.path.join(JENA_HOME, "bin", "shacl")
        if not os.path.exists(jena_shacl_cmd):
            logger.error(f"Jena SHACL-Tool not found: {jena_shacl_cmd}")
            return False, []

        data_file_jena = data_file.replace("\\", "/")
        shapes_path_jena = shapes_path.replace("\\", "/")
        cmd = [jena_shacl_cmd, "validate", "--data", data_file_jena, "--shapes", shapes_path_jena]
        
        report_file = os.path.join(BASE_DIR, "validation_report.ttl").replace("\\", "/")
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
            violations = []
            for s, p, o in report_graph.triples((None, SH.conforms, None)):
                conforms = o.toPython()
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
                            violations.append({
                                "message": message,
                                "focus_node": focus_node,
                                "path": path,
                                "severity": severity
                            })
                            logger.error(f"Validation error: {message} (Focus Node: {focus_node}, Path: {path}, Severity: {severity})")
            return conforms, violations
        else:
            logger.error("Jena SHACL validation failed with non-zero exit code.")
            return False, []
    except Exception as e:
        logger.error(f"Error during Jena SHACL validation: {e}")
        return False, []

def load_and_validate_ocp(abox_path=OCP_ABOX_PATH):
    """
    Load OCP TBOX, TIME ontology, and ABOX with rdflib, validate ABOX with SHACL,
    perform SPARQL-based inference, save inferred ABOX in Turtle format,
    and perform SHACL validation.
    Args:
        abox_path (str): Path to the ABOX file.
    Returns:
        bool: True if validation is successful, False otherwise.
    """
    try:
        # Dynamically determine output filename
        abox_filename = os.path.basename(abox_path)
        inferred_filename = abox_filename.replace(".ttl", "_RInf.ttl")
        inferred_file = os.path.join(REASONER_DIR, inferred_filename).replace("\\", "/")
        validated_abox_file = os.path.join(BASE_DIR, "validated_abox.ttl").replace("\\", "/")

        # Check if input files exist
        for file_path in [OCP_TBOX_PATH, OCP_SHAPES_PATH, abox_path]:
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return False

        # Step 1: Load Ontologies with rdflib
        try:
            time_graph = Graph()
            time_graph.parse("http://www.w3.org/2006/time#", format="turtle")
            logger.info(f"TIME ontology loaded successfully from http://www.w3.org/2006/time# ({len(time_graph)} triples)")
        except Exception as e:
            logger.error(f"Failed to load TIME ontology: {e}")
            return False

        try:
            tbox_graph = Graph()
            tbox_graph.parse(OCP_TBOX_PATH, format="turtle")
            logger.info(f"Loaded TBox: {OCP_TBOX_PATH} ({len(tbox_graph)} triples)")
        except Exception as e:
            logger.error(f"Failed to load OCP TBOX: {e}")
            return False

        try:
            abox_graph = Graph()
            abox_graph.parse(abox_path, format="turtle")
            logger.info(f"Loaded ABox: {abox_path} ({len(abox_graph)} triples)")
        except Exception as e:
            logger.error(f"Failed to load ABOX: {e}")
            return False

        # Step 2: Validate original ABOX with SHACL
        try:
            abox_graph.serialize(destination=validated_abox_file, format="turtle")
            logger.info(f"Original ABOX saved for validation: {validated_abox_file}")
            conforms, violations = perform_shacl_jena_validation(validated_abox_file)
            if not conforms:
                logger.warning("Original ABOX contains SHACL violations. Filtering invalid triples.")
                invalid_subjects = set(v["focus_node"] for v in violations)
                valid_abox_graph = Graph()
                for triple in abox_graph:
                    if str(triple[0]) not in invalid_subjects:
                        valid_abox_graph.add(triple)
                abox_graph = valid_abox_graph
                logger.info(f"Filtered ABOX contains {len(abox_graph)} triples after removing invalid subjects")
            else:
                logger.info("Original ABOX is valid according to SHACL shapes")
        except Exception as e:
            logger.error(f"Failed to validate original ABOX: {e}")
            return False

        # Step 3: Combine graphs for inference
        combined_graph = Graph()
        combined_graph += time_graph
        combined_graph += tbox_graph
        combined_graph += abox_graph
        logger.info(f"Combined ontology created with {len(combined_graph)} triples")

        # Step 4: Perform SPARQL-based inference
        try:
            inferred_graph = Graph()
            inferred_graph.bind("ocp", OCP)
            inferred_graph.bind("xsd", XSD)
            inferred_graph.bind("ex", EX)
            inferred_graph.bind("time", TIME)
            inferred_graph += abox_graph  # Start with validated ABOX triples

            # SPARQL query for time:TemporalEntity inference
            temporal_entity_query = prepareQuery(
                """
                CONSTRUCT { ?s a time:TemporalEntity }
                WHERE {
                    ?s a ocp:Phase .
                }
                """,
                initNs={"ocp": OCP, "time": TIME}
            )

            # SPARQL query for ocp:isInProcess inference
            is_in_process_query = prepareQuery(
                """
                CONSTRUCT { ?phase ocp:isInProcess ?process }
                WHERE {
                    ?process ocp:containsPhase ?phase .
                }
                """,
                initNs={"ocp": OCP}
            )

            # Execute queries
            for triple in combined_graph.query(temporal_entity_query):
                inferred_graph.add(triple)
            for triple in combined_graph.query(is_in_process_query):
                inferred_graph.add(triple)

            logger.info(f"Inferred ABOX contains {len(inferred_graph)} triples")
            os.makedirs(REASONER_DIR, exist_ok=True)
            try:
                inferred_graph.serialize(destination=inferred_file, format="turtle")
                logger.info(f"Inferred ABOX saved in Turtle format: {inferred_file}")
                temp_graph = Graph()
                temp_graph.parse(inferred_file, format="turtle")
                logger.info(f"Inferred ABOX Turtle syntax validated: {len(temp_graph)} triples")
            except Exception as e:
                logger.warning(f"Failed to save or validate inferred ABOX in Turtle format: {e}")
                inferred_file = inferred_file.replace(".ttl", ".xml")
                inferred_graph.serialize(destination=inferred_file, format="xml")
                logger.info(f"Inferred ABOX saved in RDF/XML format: {inferred_file}")
        except Exception as e:
            logger.error(f"Failed to generate inferred ABOX: {e}")
            return False

        # Step 5: Perform SHACL validation on inferred ABOX
        conforms, violations = perform_shacl_jena_validation(inferred_file)
        if conforms:
            logger.info("Validation successful: Inferred ABOX conforms to SHACL.")
        else:
            logger.error("Validation failed.")
        return conforms

    except Exception as e:
        logger.error(f"Error during OCP validation: {e}")
        return False
    finally:
        temp_file = os.path.join(BASE_DIR, "temp_ontology.xml").replace("\\", "/")
        if os.path.exists(temp_file):
            os.remove(temp_file)
        validated_abox_file = os.path.join(BASE_DIR, "validated_abox.ttl").replace("\\", "/")
        if os.path.exists(validated_abox_file):
            os.remove(validated_abox_file)

if __name__ == "__main__":
    os.makedirs(ABOX_POST_DIR, exist_ok=True)
    os.makedirs(REASONER_DIR, exist_ok=True)
    conforms = load_and_validate_ocp()
    print(f"Validation Conforms: {conforms}")