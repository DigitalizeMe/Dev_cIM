import owlready2
from rdflib import Graph
from pyshacl import validate
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def combine_and_validate(tbox_file, abox_file, shapes_file, java_exe="java", use_reasoning=False):
    try:
        # Graph für kombinierte Daten erstellen
        data_graph = Graph()
        data_graph.parse(tbox_file, format="turtle")
        data_graph.parse(abox_file, format="turtle")
        
        if use_reasoning:
            # Reasoning mit Pellet (optional)
            owlready2.JAVA_EXE = java_exe
            onto = owlready2.get_ontology(f"file://{tbox_file}").load(format="turtle")
            abox_onto = owlready2.get_ontology(f"file://{abox_file}").load(format="turtle")
            with onto:
                for indiv in abox_onto.individuals():
                    indiv.namespace = onto
                owlready2.sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
            # Inferierte Daten in den Graph übernehmen
            inferred_file = "inferred_ontology.ttl"
            onto.save(file=inferred_file, format="turtle")
            data_graph = Graph().parse(inferred_file, format="turtle")
            logger.info(f"Inferierte Ontologie gespeichert: {inferred_file}")
        
        # Shapes laden
        shapes_graph = Graph().parse(shapes_file, format="turtle")
        
        # SHACL-Validierung
        result = validate(data_graph, shacl_graph=shapes_graph, inference="none", debug=True)
        conforms, report_graph, report_text = result
        logger.info("Konformität: %s", conforms)
        logger.info("Validierungsbericht:\n%s", report_text)
        
        # Debug: Graph speichern
        data_graph.serialize("combined_graph.ttl", format="turtle")
        logger.info("Kombinierter Graph gespeichert: combined_graph.ttl")
        return conforms
    except Exception as e:
        logger.error(f"Fehler bei der Validierung: {e}")
        raise

if __name__ == "__main__":
    TBOX_PATH = r"OULD_V1.0.ttl"
    ABOX_PATH = r"OULD_ABox.ttl"
    SHAPES_PATH = r"OULD_V1.0.ttl"
    JAVA_EXE = r"G:\Java\JDK_23\bin\java.exe"
    
    # Ohne Reasoning testen
    combine_and_validate(TBOX_PATH, ABOX_PATH, SHAPES_PATH, JAVA_EXE, use_reasoning=False)