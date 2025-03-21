import json
from rdflib import Graph, Literal, URIRef, Namespace
import os

# Namespaces definieren
OCCP = Namespace("http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#")
OULD = Namespace("http://www.semanticweb.org/albrechtvaatz/ontologies/2024/OULD#")
EX = Namespace("http://example.org/example#")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

def create_turtle_from_json(json_file, turtle_file, ifc_file_name):
    """
    Creates a Turtle file from the JSON structure, including the model hash and model hierarchy.
    
    Args:
        json_file (str): Path to the input JSON file.
        turtle_file (str): Path to the output Turtle file.
        ifc_file_name (str): Name of the IFC file to derive the model name.
    """
    # Load JSON data
    with open(json_file, "r") as f:
        data = json.load(f)

    # Initialize RDF graph
    g = Graph()
    g.bind("occp", OCCP)
    g.bind("ould", OULD)
    g.bind("ex", EX)
    g.bind("rdf", RDF)

    # Helper function to create a safe URI from a name
    def safe_uri(name):
        return name.replace(" ", "_").replace("#", "No_").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")

    # Step 1: Create the model entity (top-level)
    model_name = os.path.splitext(ifc_file_name)[0]  # Extract model name from IFC file (e.g., "Building-Architecture")
    model_uri = EX[f"{model_name}_parsed"]
    g.add((model_uri, RDF.type, OULD.UpdatableEntity))
    g.add((model_uri, OULD.hasIFCID, Literal("model_id_placeholder")))  # Placeholder for model IFCID
    g.add((model_uri, OULD.hasHash, Literal(data["model_hash"])))  # Add model hash

    # Step 2: Process each type (e.g., IfcBuildingElementProxy)
    for type_name, type_data in data["Types"].items():
        type_uri = EX[safe_uri(type_name)]  # e.g., ex:IfcBuildingElementProxy
        g.add((type_uri, RDF.type, OULD.UpdatableEntity))
        g.add((type_uri, OULD.hasIFCID, Literal(type_name)))  # Use type name as IFCID for now

        # Connect type to the model
        g.add((model_uri, OULD.consistsOf, type_uri))

        # Step 3: Process each element within the type
        for element_name, element_data in type_data.items():
            if element_name.startswith("_"):  # Skip metadata like _count1
                continue
            element_uri = EX[safe_uri(element_name)]  # e.g., ex:Group_No_18
            g.add((element_uri, RDF.type, OULD.UpdatableEntity))
            g.add((element_uri, OULD.hasIFCID, Literal(element_data["GlobalIds"][0])))
            
            # Connect element to its type
            g.add((type_uri, OULD.consistsOf, element_uri))

    # Save the Turtle file
    g.serialize(destination=turtle_file, format="turtle")
    print(f"Turtle file saved: {turtle_file}")

if __name__ == "__main__":
    json_file = "IFC/parsed/Building-Architecture_parsed.json"
    turtle_file = "IFC/parsed/Building-Architecture_parsed.ttl"
    ifc_file_name = "IFC/Building-Architecture.ifc"  
    create_turtle_from_json(json_file, turtle_file, ifc_file_name)