# validate_shacl_35_OCP.py

import os
import subprocess
import logging
import tempfile
from rdflib import Graph, Namespace, RDF, SH, URIRef, Literal
from owlready2 import get_ontology, sync_reasoner_pellet, default_world, Thing

# Logging configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(
    filename=os.path.join(BASE_DIR, "validation.log"),
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w"
)
logger = logging.getLogger(__name__)

# Paths and namespaces
OCP_TBOX_PATH = os.path.join(BASE_DIR, "Onto", "TBOX", "OCP_TBOX.ttl").replace("\\", "/")
OCP_SHAPES_PATH = os.path.join(BASE_DIR, "Onto", "SHACL", "OCP_SHACL-Shapes.ttl").replace("\\", "/")
OCP_ABOX_PATH = os.path.join(BASE_DIR, "Onto", "ABOX", "OCP", "OCP_ABOX_12.ttl").replace("\\", "/")
ABOX_POST_DIR = os.path.join(BASE_DIR, "Onto", "ABOX", "OCP", "POST_ABOX").replace("\\", "/")
REASONER_DIR = os.path.join(ABOX_POST_DIR, "Reasoner").replace("\\", "/")
CONSTRUCT_DIR = os.path.join(ABOX_POST_DIR, "CONSTRUCT").replace("\\", "/")
TIME_OWL_PATH = os.path.join(BASE_DIR, "Onto", "TBOX", "time.owl").replace("\\", "/")
JAVA_EXE = r"G:\Java\JDK_23\bin\java.exe".replace("\\", "/")
JENA_HOME = os.path.join(BASE_DIR, "apache-jena-5.3.0").replace("\\", "/")
OCP = Namespace("http://www.semanticweb.org/DigitalizeMe/ontologies/2025/3/OCP#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
EX = Namespace("http://www.example.de/example#")
TIME = Namespace("http://www.w3.org/2006/time#")
OWL = Namespace("http://www.w3.org/2002/07/owl#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")

def perform_reasoning(tbox_path, abox_path, output_path):
    """
    Perform OWL reasoning using Pellet to generate an inferred ABOX.
    Args:
        tbox_path (str): Path to the TBOX file.
        abox_path (str): Path to the ABOX file.
        output_path (str): Path to save the inferred ABOX.
    Returns:
        bool: True if reasoning was successful, False otherwise.
    """
    temp_tbox_path = None
    temp_time_path = None
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        logger.debug(f"Ensured output directory: {os.path.dirname(output_path)}")

        # Validate TBox syntax with RDFLib
        logger.debug(f"Validating TBox syntax: {tbox_path}")
        tbox_graph = Graph()
        with open(tbox_path, "r", encoding="utf-8") as f:
            tbox_graph.parse(data=f.read(), format="turtle")
        logger.debug("TBox syntax validated successfully")

        # Validate ABox syntax with RDFLib
        logger.debug(f"Validating ABox syntax: {abox_path}")
        abox_graph = Graph()
        with open(abox_path, "r", encoding="utf-8") as f:
            abox_graph.parse(data=f.read(), format="turtle")
        logger.debug("ABox syntax validated successfully")

        # Save TBox as RDF/XML temporarily
        logger.debug("Converting TBox to RDF/XML for owlready2")
        with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as temp_tbox:
            tbox_graph.serialize(temp_tbox.name, format="xml")
            temp_tbox_path = temp_tbox.name.replace("\\", "/")
        logger.debug(f"Temporary TBox saved: {temp_tbox_path}")

        # Validate and convert time.owl to RDF/XML if local
        time_graph = None
        if os.path.exists(TIME_OWL_PATH):
            logger.debug(f"Validating time.owl syntax: {TIME_OWL_PATH}")
            time_graph = Graph()
            with open(TIME_OWL_PATH, "r", encoding="utf-8") as f:
                time_graph.parse(data=f.read(), format="turtle")
            logger.debug("time.owl syntax validated successfully")

            logger.debug("Converting time.owl to RDF/XML")
            with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as temp_time:
                time_graph.serialize(temp_time.name, format="xml")
                temp_time_path = temp_time.name.replace("\\", "/")
            logger.debug(f"Temporary time.owl saved: {temp_time_path}")

        # Create a new world for owlready2
        logger.debug("Creating new owlready2 world")
        world = default_world

        # Load TBOX into owlready2
        logger.debug(f"Loading TBOX from: {temp_tbox_path}")
        onto = world.get_ontology(f"file://{temp_tbox_path}").load()
        logger.debug("TBOX loaded successfully")

        # Load ABOX
        logger.debug(f"Loading ABOX from: {abox_path}")
        abox_temp = tempfile.NamedTemporaryFile(suffix=".ttl", delete=False)
        abox_graph.serialize(abox_temp.name, format="turtle")
        onto.load(f"file://{abox_temp.name}", format="turtle")
        abox_temp.close()
        os.unlink(abox_temp.name)
        logger.debug("ABOX loaded successfully")

        # Log loaded ABOX instances
        logger.debug("Listing loaded ABOX instances:")
        for indiv in onto.individuals():
            logger.debug(f"Individual: {indiv}, Classes: {list(indiv.is_a)}")

        # Load OWL-Time ontology
        logger.debug(f"Checking for local OWL-Time ontology: {TIME_OWL_PATH}")
        if temp_time_path:
            logger.debug(f"Loading local OWL-Time ontology from: {temp_time_path}")
            onto.imported_ontologies.append(world.get_ontology(f"file://{temp_time_path}").load())
            logger.debug("Local OWL-Time ontology loaded successfully")
        else:
            logger.debug("Attempting to load OWL-Time ontology from web")
            try:
                onto.imported_ontologies.append(world.get_ontology("http://www.w3.org/2006/time").load())
                logger.debug("Online OWL-Time ontology loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load OWL-Time ontology: {e}")
                return False

        # Perform reasoning with Pellet
        logger.debug("Starting Pellet reasoning")
        with onto:
            sync_reasoner_pellet(debug=1)
        logger.debug("Pellet reasoning completed")

        # Log inferred classes for ABOX instances
        logger.debug("Listing inferred classes for ABOX instances:")
        for indiv in onto.individuals():
            classes = list(indiv.is_a)
            logger.debug(f"Individual: {indiv}, Inferred classes: {classes}")

        # Save inferred ABOX (only ABOX data)
        logger.debug(f"Saving inferred ABOX to: {output_path}")
        inferred_graph = Graph()
        for indiv in onto.individuals():
            indiv_uri = URIRef(str(indiv.iri))
            for cls in indiv.is_a:
                cls_uri = URIRef(str(cls.iri)) if hasattr(cls, "iri") else cls
                inferred_graph.add((indiv_uri, RDF.type, cls_uri))
            for prop in indiv.get_properties():
                prop_uri = URIRef(str(prop.iri))
                for value in prop[indiv]:
                    if isinstance(value, Thing):
                        inferred_graph.add((indiv_uri, prop_uri, URIRef(str(value.iri))))
                    elif isinstance(value, (str, int, float, bool)):
                        inferred_graph.add((indiv_uri, prop_uri, Literal(value)))
        inferred_graph.serialize(output_path, format="turtle")
        logger.info(f"Reasoner-inferred ABOX saved: {output_path}")

        # Verify output file
        if not os.path.exists(output_path):
            logger.error(f"Failed to create inferred ABOX: {output_path}")
            return False
        logger.debug(f"Verified inferred ABOX exists: {output_path}")

        return True
    except Exception as e:
        logger.error(f"Error during Pellet reasoning: {str(e)}")
        return False
    finally:
        if temp_tbox_path and os.path.exists(temp_tbox_path):
            os.unlink(temp_tbox_path)
            logger.debug(f"Cleaned up temporary TBox: {temp_tbox_path}")
        if temp_time_path and os.path.exists(temp_time_path):
            os.unlink(temp_time_path)
            logger.debug(f"Cleaned up temporary time.owl: {temp_time_path}")

def perform_shacl_jena_validation(data_file, shapes_path=OCP_SHAPES_PATH):
    """
    Perform SHACL validation using Apache Jena.
    Args:
        data_file (str): Path to the data file (inferred ABOX).
        shapes_path (str): Path to the SHACL shapes file.
    Returns:
        bool: True if the data conforms to the SHACL shapes, False otherwise.
    """
    try:
        # Ensure log4j2.properties exists and use it explicitly as a file URI
        log4j_props = os.path.join(JENA_HOME, "log4j2.properties")
        if not os.path.exists(log4j_props):
            with open(log4j_props, "w", encoding="utf-8") as f:
                f.write("""
status = warn
name = Log4j2Config

appenders = console

appender.console.type = Console
appender.console.name = STDOUT
appender.console.layout.type = PatternLayout
appender.console.layout.pattern = %d{yyyy-MM-dd HH:mm:ss} %-5p %c{1}:%L - %m%n

rootLogger.level = error
rootLogger.appenderRefs = stdout
rootLogger.appenderRef.stdout.ref = STDOUT
""")
            logger.debug(f"Created Log4j2 properties: {log4j_props}")

        # Build command to invoke Jena SHACL via Java to avoid batch file issues
        java_exec = JAVA_EXE if os.name == 'nt' else "java"
        classpath = os.path.join(JENA_HOME, "lib", "*")
        log4j_uri = f"file:///{log4j_props.replace(os.sep, '/')}"

        data_file_jena = data_file.replace("\\", "/")
        shapes_path_jena = shapes_path.replace("\\", "/")

        cmd = [
            java_exec,
            f"-Dlog4j.configurationFile={log4j_uri}",
            "-cp",
            classpath,
            "shacl.shacl",
            "validate",
            "--data",
            data_file_jena,
            "--shapes",
            shapes_path_jena,
        ]
        
        # Run validation and save report
        report_file = os.path.join(BASE_DIR, "validation_report.ttl").replace("\\", "/")
        with open(report_file, "w", encoding="utf-8") as f:
            env = os.environ.copy()
            env["JENA_HOME"] = JENA_HOME
            result = subprocess.run(
                cmd,
                stdout=f,
                stderr=subprocess.PIPE,
                text=True,
                env=env
            )

        # Log any stderr output
        if result.stderr:
            logger.debug(f"Jena SHACL validation stderr: {result.stderr}")

        # Check if validation was successful
        if result.returncode == 0:
            with open(report_file, "r", encoding="utf-8") as f:
                report_data = f.read()
            logger.debug(f"SHACL Report: {report_data}")
            report_graph = Graph()
            try:
                report_graph.parse(data=report_data, format="turtle")
            except Exception as e:
                logger.error(f"Failed to parse SHACL report: {e}")
                return False
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
    Load OCP TBOX and ABOX, perform reasoning, and SHACL validation.
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
        with open(OCP_TBOX_PATH, "r", encoding="utf-8") as f:
            tbox_graph.parse(data=f.read(), format="turtle")
        logger.info(f"Loaded TBox: {OCP_TBOX_PATH}")

        # Load ABox
        abox_graph = Graph()
        with open(OCP_ABOX_PATH, "r", encoding="utf-8") as f:
            abox_graph.parse(data=f.read(), format="turtle")
        logger.info(f"Loaded ABox: {OCP_ABOX_PATH}")

        # Perform reasoning with Pellet
        reasoner_inferred_file = os.path.join(REASONER_DIR, "Reasoner_inferred.ttl").replace("\\", "/")
        if not perform_reasoning(OCP_TBOX_PATH, OCP_ABOX_PATH, reasoner_inferred_file):
            logger.error("Reasoning failed, aborting validation.")
            return False

        # Perform SHACL validation on reasoner-inferred ABOX
        conforms = perform_shacl_jena_validation(reasoner_inferred_file)
        if conforms:
            logger.info("Validation successful: ABox conforms to SHACL.")
        else:
            logger.error("Validation failed.")
        return conforms

    except Exception as e:
        logger.error(f"Error during OCP validation: {e}")
        return False

if __name__ == "__main__":
    # Ensure POST_ABOX subdirectories exist
    os.makedirs(REASONER_DIR, exist_ok=True)
    os.makedirs(CONSTRUCT_DIR, exist_ok=True)
    
    # Run validation
    conforms = load_and_validate_ocp()
    print(f"Validation Conforms: {conforms}")