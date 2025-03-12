import owlready2
from rdflib import Graph, Namespace, RDF
from pyshacl import validate
import logging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(
    filename=os.path.join(BASE_DIR, "validation.log"),
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w"
)
logger = logging.getLogger(__name__)

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
        chain1_types = list(data_graph.triples((OULD.Chain1, RDF.type, None)))
        logger.debug(f"Chain1 Typen nach Reasoning: {len(chain1_types)}")
        for s, p, o in chain1_types:
            logger.debug(f"Chain1 Typ-Triple: {s} {p} {o}")
        wall1_types = list(data_graph.triples((OULD.Wall1, RDF.type, None)))
        logger.debug(f"Wall1 Typen nach Reasoning: {len(wall1_types)}")
        for s, p, o in wall1_types:
            logger.debug(f"Wall1 Typ-Triple: {s} {p} {o}")
        return output_file
    except Exception as e:
        logger.error(f"Fehler beim Reasoning: {e}")
        raise

def debug_sparql(data_file):
    try:
        data_graph = Graph().parse(data_file, format="turtle")
        query = """
            PREFIX ould: <http://www.semanticweb.org/albrechtvaatz/ontologies/2024/OULD#>
            SELECT (COUNT(?u) AS ?updateCount)
            WHERE {
                ould:Chain1 a ould:UpdateChain .
                ould:Chain1 ould:hasUpdate ?u .
            }
        """
        logger.info("Starte spezifische SPARQL-Abfrage für Chain1...")
        results = data_graph.query(query)
        logger.info("SPARQL-Abfrage Ergebnisse für Chain1:")
        for row in results:
            logger.info(f"UpdateCount für Chain1: {row.updateCount}")
        return len(results) > 0
    except Exception as e:
        logger.error(f"Fehler bei der SPARQL-Abfrage: {e}")
        raise

def perform_shacl_validation(data_file, shapes_path=SHAPES_PATH):
    try:
        data_graph = Graph().parse(data_file, format="turtle")
        shapes_graph = Graph().parse(shapes_path, format="turtle")
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