import owlready2
from rdflib import Graph
from pyshacl import validate
import logging
import os

# Logging einrichten
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Globale Pfade definieren
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Verzeichnis des Skripts
TBOX_PATH = os.path.join(BASE_DIR, "OULD_V1.0.ttl")  # TBox bleibt im Hauptordner
ABOX_DIR = os.path.join(BASE_DIR, "OULD_ABox")  # Neuer Ordner für ABoxes
SHAPES_PATH = os.path.join(BASE_DIR, "OULD_V1.0.ttl")  # Shapes bleiben bei TBox
JAVA_EXE = r"G:\Java\JDK_23\bin\java.exe"

def combine_and_reason(tbox_path=TBOX_PATH, abox_path=None, java_exe=JAVA_EXE):
    try:
        # TBox und ABox laden
        onto = owlready2.get_ontology(f"file://{tbox_path}").load(format="turtle")
        if abox_path:
            abox_onto = owlready2.get_ontology(f"file://{abox_path}").load(format="turtle")
            with onto:
                for indiv in abox_onto.individuals():
                    new_indiv = onto.get_entities(indiv.name, indiv.__class__)
                    if not new_indiv:
                        new_indiv = indiv.__class__(indiv.name, namespace=onto)
                    for prop in indiv.get_properties():
                        for value in prop[indiv]:
                            prop[new_indiv] = value
                owlready2.sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
        
        # Kombinierten Graph mit rdflib erstellen
        data_graph = Graph()
        data_graph.parse(tbox_path, format="turtle")
        if abox_path:
            data_graph.parse(abox_path, format="turtle")
        
        # Inferierte Ontologie speichern
        output_file = os.path.join(BASE_DIR, "inferred_ontology.ttl")
        data_graph.serialize(destination=output_file, format="turtle")
        logger.info(f"Inferierte Ontologie gespeichert: {output_file}")
        with open(output_file, "r") as f:
            logger.info(f"Inhalt von {output_file}:\n{f.read()}")
        return output_file
    except Exception as e:
        logger.error(f"Fehler beim Reasoning: {e}")
        raise

def perform_shacl_validation(data_file, shapes_path=SHAPES_PATH):
    try:
        data_graph = Graph().parse(data_file, format="turtle")
        shapes_graph = Graph().parse(shapes_path, format="turtle")
        result = validate(data_graph, shacl_graph=shapes_graph, inference="none", debug=True)
        conforms, report_graph, report_text = result
        logger.info("Konformität: %s", conforms)
        logger.info("Validierungsbericht:\n%s", report_text)
        return conforms
    except Exception as e:
        logger.error(f"Fehler bei der SHACL-Validierung: {e}")
        raise

if __name__ == "__main__":
    # Pfad zur ersten invaliden ABox
    ABOX_PATH = os.path.join(ABOX_DIR, "OULD_ABox.ttl")
    
    # Reasoning und Validierung
    inferred_file = combine_and_reason(tbox_path=TBOX_PATH, abox_path=ABOX_PATH, java_exe=JAVA_EXE)
    perform_shacl_validation(inferred_file, shapes_path=SHAPES_PATH)