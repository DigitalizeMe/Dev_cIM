import owlready2
from rdflib import Graph
from pyshacl import validate
import logging

# Globale Pfade definieren
TBOX_PATH = r"OULD_V1.0.ttl"
ABOX_PATH = r"OULD_ABox.ttl"
SHAPES_PATH = r"OULD_V1.0.ttl"
JAVA_EXE = r"G:\Java\JDK_23\bin\java.exe"

# Logging einrichten
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def combine_and_reason(tbox_path=TBOX_PATH, abox_path=ABOX_PATH, java_exe=JAVA_EXE):
    try:
        # TBox und ABox laden
        onto = owlready2.get_ontology(f"file://{tbox_path}").load(format="turtle")
        abox_onto = owlready2.get_ontology(f"file://{abox_path}").load(format="turtle")
        
        # ABox-Instanzen in TBox-Ontologie integrieren
        with onto:
            for indiv in abox_onto.individuals():
                # Instanz vollständig kopieren
                new_indiv = onto.get_entities(indiv.name, indiv.__class__)
                if not new_indiv:
                    new_indiv = indiv.__class__(indiv.name, namespace=onto)
                for prop in indiv.get_properties():
                    for value in prop[indiv]:
                        prop[new_indiv] = value
            # Reasoning durchführen
            owlready2.sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
        
        # Kombinierten Graph mit rdflib erstellen
        data_graph = Graph()
        data_graph.parse(tbox_path, format="turtle")
        data_graph.parse(abox_path, format="turtle")
        
        # Inferierte Ontologie speichern
        output_file = "inferred_ontology.ttl"
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
    inferred_file = combine_and_reason()
    perform_shacl_validation(inferred_file)