import owlready2
from rdflib import Graph, Namespace, RDF
from pyshacl import validate
import logging
import os
import sys

# Konfiguration des Loggings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(
    filename=os.path.join(BASE_DIR, "validation.log"),
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w"
)
logger = logging.getLogger(__name__)

# Pfade und Namespace
TBOX_PATH = os.path.join(BASE_DIR, "OULD_V1.0.ttl")
ABOX_DIR = os.path.join(BASE_DIR, "OULD_ABox")
SHAPES_PATH = os.path.join(BASE_DIR, "OULD_V1.0.ttl")
JAVA_EXE = r"G:\Java\JDK_23\bin\java.exe".replace("\\", "/")
OULD = Namespace("http://www.semanticweb.org/albrechtvaatz/ontologies/2024/OULD#")

def combine_and_reason(tbox_path=TBOX_PATH, abox_path=None, java_exe=JAVA_EXE):
    try:
        tbox_path_normalized = tbox_path.replace("\\", "/")
        abox_path_normalized = abox_path.replace("\\", "/") if abox_path else None
        onto = owlready2.get_ontology(f"file://{tbox_path_normalized}").load(format="turtle")
        if abox_path:
            abox_onto = owlready2.get_ontology(f"file://{abox_path_normalized}").load(format="turtle")
            with onto:
                for indiv in abox_onto.individuals():
                    new_indiv = onto.get_entities(indiv.name, indiv.__class__)
                    if not new_indiv:
                        new_indiv = indiv.__class__(indiv.name, namespace=onto)
                    for prop in indiv.get_properties():
                        for value in prop[indiv]:
                            prop[new_indiv] = value
                owlready2.sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True, debug=2)
        data_graph = Graph()
        data_graph.parse(tbox_path, format="turtle")
        if abox_path:
            data_graph.parse(abox_path, format="turtle")
        output_file = os.path.join(BASE_DIR, "inferred_ontology.ttl")
        data_graph.serialize(destination=output_file, format="turtle")
        logger.info(f"Inferierte Ontologie gespeichert: {output_file}")
        return output_file
    except Exception as e:
        logger.error(f"Fehler beim Reasoning: {e}")
        raise

def debug_sparql(data_file):
    try:
        data_graph = Graph().parse(data_file, format="turtle")
        query = """
            PREFIX ould: <http://www.semanticweb.org/albrechtvaatz/ontologies/2024/OULD#>
            SELECT ?chain (COUNT(?u) AS ?updateCount)
            WHERE {
                ?chain a ould:UpdateChain .
                ?chain ould:hasUpdate ?u .
            }
            GROUP BY ?chain
        """
        logger.info("Starte SPARQL-Abfrage für alle UpdateChains...")
        results = data_graph.query(query)
        logger.info("SPARQL-Abfrage Ergebnisse:")
        for row in results:
            logger.info(f"Chain: {row.chain}, UpdateCount: {row.updateCount}")
        return len(results) > 0
    except Exception as e:
        logger.error(f"Fehler bei der SPARQL-Abfrage: {e}")
        raise

def perform_shacl_validation(data_file, shapes_path=SHAPES_PATH):
    try:
        data_graph = Graph().parse(data_file, format="turtle")
        shapes_path_normalized = shapes_path.replace("\\", "/")
        shapes_uri = f"file:///{shapes_path_normalized}"  # Fix für lokalen Pfad
        logger.debug(f"Versuche Shapes von URI zu laden: {shapes_uri}")
        shapes_graph = Graph().parse(shapes_uri, format="turtle")
        result = validate(data_graph, shacl_graph=shapes_graph, inference="none", debug=2)
        conforms, report_graph, report_text = result
        logger.info(f"Konformität (inference=none): {conforms}")
        if not conforms:
            logger.info("Validierungsbericht (inference=none):")
            report_lines = report_text.splitlines()
            logger.info("\n".join(report_lines))
        return conforms
    except Exception as e:
        logger.error(f"Fehler bei der SHACL-Validierung: {e}")
        raise

if __name__ == "__main__":
    ABOX_PATH = os.path.join(ABOX_DIR, "OULD_ABox_invalid_typemix.ttl")
    inferred_file = combine_and_reason(tbox_path=TBOX_PATH, abox_path=ABOX_PATH, java_exe=JAVA_EXE)
    debug_sparql(inferred_file)
    perform_shacl_validation(inferred_file)