import owlready2
from rdflib import Graph
from pyshacl import validate
import logging

# Logging einrichten
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def perform_pellet_reasoning(tbox_file, abox_file=None, java_exe="java"):
    """
    Führt Reasoning mit Pellet auf der Ontologie durch.
    
    Args:
        tbox_file (str): Pfad zur TBox-Datei (z. B. OULD.ttl)
        abox_file (str, optional): Pfad zur ABox-Datei (z. B. MsOCCP.ttl)
        java_exe (str): Pfad zur Java-Executable (Default: "java")
    
    Returns:
        str: Pfad zur inferierten Ontologie-Datei
    """
    owlready2.JAVA_EXE = java_exe
    try:
        # TBox laden
        onto = owlready2.get_ontology(f"file://{tbox_file}").load(format="turtle")
        # ABox optional importieren
        if abox_file:
            onto.imported_ontologies.append(owlready2.get_ontology(f"file://{abox_file}").load(format="turtle"))
        # Reasoning mit Pellet
        with onto:
            owlready2.sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
        # Inferierte Ontologie speichern
        output_file = "inferred_ontology.ttl"
        onto.save(file=output_file, format="ntriples")
        logger.info(f"Inferierte Ontologie gespeichert: {output_file}")
        return output_file
    except Exception as e:
        logger.error(f"Fehler beim Reasoning: {e}")
        raise

def perform_shacl_validation(data_file, shapes_file):
    """
    Validiert die inferierte Ontologie gegen SHACL-Shapes.
    
    Args:
        data_file (str): Pfad zur inferierten Ontologie (Datengraph)
        shapes_file (str): Pfad zur SHACL-Shapes-Datei
    
    Returns:
        bool: Konformität (True/False)
    """
    try:
        # Datengraph und Shapes-Graph laden
        data_graph = Graph().parse(data_file, format="ntriples")
        shapes_graph = Graph().parse(shapes_file, format="turtle")
        # SHACL-Validierung durchführen
        result = validate(
            data_graph,
            shacl_graph=shapes_graph,
            inference="none",  # Keine zusätzliche Inferenz, da Pellet schon lief
            debug=True
        )
        conforms, report_graph, report_text = result
        logger.info("Konformität: %s", conforms)
        logger.info("Validierungsbericht:\n%s", report_text)
        return conforms
    except Exception as e:
        logger.error(f"Fehler bei der SHACL-Validierung: {e}")
        raise

if __name__ == "__main__":
    # Beispiel-Dateipfade (anpassen!)
    TBOX_PATH = r"OCCP_TBx_V0.26.ttl"
    ABOX_PATH = r"OCCP_Phase_A_inVALID_1.ttl"
    SHAPES_PATH = r"OULD_shapes.ttl"
    JAVA_EXE = r"G:\Java\JDK_23\bin\java.exe"

    # Schritt 1: Reasoning mit Pellet
    inferred_file = perform_pellet_reasoning(TBOX_PATH, ABOX_PATH, JAVA_EXE)
    
    # Schritt 2: SHACL-Validierung der inferierten Ontologie
    perform_shacl_validation(inferred_file, SHAPES_PATH)