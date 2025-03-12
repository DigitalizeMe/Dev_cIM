import owlready2
from rdflib import Graph, Namespace, RDF
from rdflib.namespace import SH, OWL
from pyshacl import validate
import logging
import os
import sys
from io import StringIO

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
TBOX_PATH = os.path.join(BASE_DIR, "OCCP_V0.3.ttl")
ABOX_DIR = os.path.join(BASE_DIR, "OCCP_ABox")
SHAPES_PATH = os.path.join(BASE_DIR, "OCCP_SHACL_min.ttl")
JAVA_EXE = r"G:\Java\JDK_23\bin\java.exe".replace("\\", "/")
OULD = Namespace("http://www.semanticweb.org/albrechtvaatz/ontologies/2024/OULD#")
OCCP = Namespace("http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#")

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
        # Generische Disjunktheitsprüfung
        logger.info("Prüfe Ontologie auf Disjunktheit...")
        disjoint_pairs = set()
        for s, p, o in data_graph.triples((None, OWL.disjointWith, None)):
            disjoint_pairs.add((s, o))
            disjoint_pairs.add((o, s))  # Bidirektional
        logger.debug(f"Disjunkte Klassenpaare: {disjoint_pairs}")
        for subj in data_graph.subjects(RDF.type, None):
            types = set(o for s, p, o in data_graph.triples((subj, RDF.type, None)))
            for class1, class2 in disjoint_pairs:
                if class1 in types and class2 in types:
                    logger.error(f"Disjunktheitsverletzung gefunden: {subj} hat Typen {class1} und {class2}")
                    raise Exception(f"Ontology is inconsistent: {subj} has disjoint types {class1} and {class2}")
        logger.info("Keine Disjunktheitsverletzungen gefunden.")
        return output_file
    except Exception as e:
        logger.error(f"Fehler beim Reasoning oder Disjunktheitsprüfung: {e}")
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
        shapes_uri = f"file:///{shapes_path_normalized}"
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
    ABOX_PATH = os.path.join(ABOX_DIR, "OCCP_Valid_LCycle_1.ttl")
    inferred_file = combine_and_reason(tbox_path=TBOX_PATH, abox_path=ABOX_PATH, java_exe=JAVA_EXE)
    debug_sparql(inferred_file)
    perform_shacl_validation(inferred_file)