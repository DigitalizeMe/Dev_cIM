#validate_sparql.py

from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery
from pyshacl import validate
import logging

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dateipfade
pre_abox_file = "OCCP_Pre_1.ttl"
post_abox_file = "OCCP_Post_1.ttl"
shacl_file = "OCCP_SHACL_V1.1.ttl"
sparql_file = "OCCP_SPARQL_V1.0.ttl"

# 1. PreI-ABox laden und validieren
pre_g = Graph()
pre_g.parse(pre_abox_file, format="turtle")
logger.info("PreI-ABox geladen.")

pre_result = validate(pre_g, shacl_graph=shacl_file, inference="none")
if not pre_result[0]:
    logger.error(f"PreI-Validierung fehlgeschlagen:\n{pre_result[2]}")
    exit(1)
logger.info("PreI-ABox validiert: Conforms = True")

# 2. SPARQL-Construct ausführen
sparql_g = Graph()
sparql_g.parse(sparql_file, format="turtle")
construct_query_text = str(sparql_g.query("""
    PREFIX osh: <http://www.example.de/shapes#>
    SELECT ?query WHERE {
        osh:beginningOfPlanningConstruct osh:queryText ?query .
    }
""").bindings[0]["query"])
construct_query = prepareQuery(construct_query_text, initNs={"occp": "http://www.semanticweb.org/DigitalizeMe/ontologies/2022/9/cMod_V0.1#"})

post_g = pre_g.query(construct_query)
post_abox = Graph()
for triple in pre_g:
    post_abox.add(triple)
for triple in post_g:
    post_abox.add(triple)
post_abox.serialize(post_abox_file, format="turtle")
logger.info("PostI-ABox erzeugt und gespeichert.")

# 3. PostI-ABox validieren
post_result = validate(post_abox, shacl_graph=shacl_file, inference="none")
if not post_result[0]:
    logger.error(f"PostI-Validierung fehlgeschlagen:\n{post_result[2]}")
    exit(1)
logger.info("PostI-ABox validiert: Conforms = True")