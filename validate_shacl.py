import owlready2
from rdflib import Graph
from pyshacl import validate
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def perform_pellet_reasoning(tbox_file, abox_file=None, java_exe="java"):
    owlready2.JAVA_EXE = java_exe
    try:
        # TBox laden
        onto = owlready2.get_ontology(f"file://{tbox_file}").load(format="turtle")
        if abox_file:
            # ABox laden und vollständig integrieren
            abox_onto = owlready2.get_ontology(f"file://{abox_file}").load(format="turtle")
            with onto:
                # ABox-Instanzen in die TBox-Ontologie kopieren
                for indiv in abox_onto.individuals():
                    indiv.namespace = onto
                owlready2.sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
        # Inferierte Ontologie speichern
        output_file = "inferred_ontology.ttl"
        onto.save(file=output_file, format="ntriples")
        logger.info(f"Inferierte Ontologie gespeichert: {output_file}")
        # Debug: Inhalt prüfen
        with open(output_file, "r") as f:
            logger.info(f"Inhalt von {output_file}:\n{f.read()}")
        return output_file
    except Exception as e:
        logger.error(f"Fehler beim Reasoning: {e}")
        raise

def perform_shacl_validation(data_file, shapes_file):
    try:
        data_graph = Graph().parse(data_file, format="ntriples")
        shapes_graph = Graph().parse(shapes_file, format="turtle")
        result = validate(data_graph, shacl_graph=shapes_graph, inference="none", debug=True)
        conforms, report_graph, report_text = result
        logger.info("Konformität: %s", conforms)
        logger.info("Validierungsbericht:\n%s", report_text)
        return conforms
    except Exception as e:
        logger.error(f"Fehler bei der SHACL-Validierung: {e}")
        raise

if __name__ == "__main__":
    TBOX_PATH = r"OULD_V1.0.ttl"
    ABOX_PATH = r"OULD_ABox.ttl"
    SHAPES_PATH = r"OULD_V1.0.ttl"
    JAVA_EXE = r"G:\Java\JDK_23\bin\java.exe"
    
    inferred_file = perform_pellet_reasoning(TBOX_PATH, ABOX_PATH, JAVA_EXE)
    perform_shacl_validation(inferred_file, SHAPES_PATH)