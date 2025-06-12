# OCP_construct_queries.py

from rdflib import Graph, Namespace, RDF

OCP = Namespace("http://www.semanticweb.org/DigitalizeMe/ontologies/2025/3/OCP#")
TIME = Namespace("http://www.w3.org/2006/time#")

CONSTRUCT_TIME_TYPES = """
PREFIX ocp: <http://www.semanticweb.org/DigitalizeMe/ontologies/2025/3/OCP#>
PREFIX time: <http://www.w3.org/2006/time#>
CONSTRUCT {
  ?x a time:Interval .
  ?x a time:TemporalEntity .
}
WHERE {
  ?x a ?ocpClass .
  FILTER(?ocpClass IN (ocp:Phase, ocp:Process, ocp:Cycle))
  FILTER NOT EXISTS { ?x a time:Interval }
  FILTER NOT EXISTS { ?x a time:TemporalEntity }
}
"""

CONSTRUCT_TIME_TYPES_TRANSITIONS = """
PREFIX ocp: <http://www.semanticweb.org/DigitalizeMe/ontologies/2025/3/OCP#>
PREFIX time: <http://www.w3.org/2006/time#>
CONSTRUCT {
  ?x a time:Instant .
  ?x a time:TemporalEntity .
}
WHERE {
  ?x a ocp:Transition .
  FILTER NOT EXISTS { ?x a time:Instant }
  FILTER NOT EXISTS { ?x a time:TemporalEntity }
}
"""

def enrich_time_types(input_ttl, output_ttl):
    g = Graph()
    g.parse(input_ttl, format="turtle")
    g += g.query(CONSTRUCT_TIME_TYPES).graph
    g += g.query(CONSTRUCT_TIME_TYPES_TRANSITIONS).graph
    g.serialize(output_ttl, format="turtle")
    print(f"[INFO] Added Time-classes and saved to: {output_ttl}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        enrich_time_types(sys.argv[1], sys.argv[2])
    else:
        print("Verwendung: python ocp_construct_queries.py <input_abox.ttl> <output_abox.ttl>")
