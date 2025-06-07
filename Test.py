from rdflib import Graph
g = Graph()
g.parse("G:/Promo/Dev_cIM/Onto/ABOX/OCP/OCP_ABOX_12.ttl", format="turtle")
print("ABOX parsed successfully")