import owlready2
from rdflib import Graph
from pyshacl import validate

owlready2.JAVA_EXE = "G:\\Java\\JDK_23\\bin\\java.exe"  
TBOX_PATH = r"OCCP_TBx_V0.26.ttl"
ABOX_PATH = r"OCCP_Phase_A_inVALID_1.ttl"

print(f"Java-Pfad: {owlready2.JAVA_EXE}")

# Schritt 1: Ontologie laden und Reasoning mit Pellet durchführen
def perform_pellet_reasoning(ontology_file):
    # Ontologie laden
    onto = owlready2.get_ontology(f"file://{ontology_file}").load(format="turtle")
    
    # Reasoning mit Pellet durchführen
    with onto:
        owlready2.sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
    
    # Inferierte Ontologie speichern
    output_file = "inferred_ontology.ttl"
    onto.save(file=output_file, format="ntriples")  # ntriples, da pyshacl das bevorzugt
    return output_file

# Schritt 2: SHACL-Validierung
def perform_shacl_validation(data_file, shapes_file):
    # Datengraph (inferierte Ontologie) und Shapes-Graph laden
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
    print("Konformität:", conforms)
    print("Validierungsbericht:\n", report_text)
    return conforms

# Hauptprogramm
if __name__ == "__main__":
    # Dateipfade (anpassen!)
    ontology_file = "meine_ontologie.ttl"  # Deine TTL-Ontologie (TBox + ABox)
    shapes_file = "meine_shapes.ttl"       # Deine SHACL-Shapes
    
    # Schritt 1: Reasoning mit Pellet
    inferred_file = perform_pellet_reasoning(ontology_file)
    
    # Schritt 2: SHACL-Validierung der inferierten Ontologie
    perform_shacl_validation(inferred_file, shapes_file)


