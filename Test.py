from rdflib import Graph
try:
    g = Graph()
    g.parse("G:/Promo/Dev_cIM/Onto/TBOX/time.owl", format="turtle")
    print("time.owl parsed successfully")
except Exception as e:
    print(f"Error parsing time.owl: {e}")