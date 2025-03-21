import rdflib
from rdflib import Graph, Literal, Namespace

# Define namespaces
OCCP = Namespace("http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#")
OULD = Namespace("http://www.semanticweb.org/albrechtvaatz/ontologies/2024/OULD#")
EX = Namespace("http://example.org/example#")
AE = Namespace("http://example.org/autoedit#")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

def create_preI_abox(parsed_file, output_file):
    """
    Creates a PreI-ABox from a parsed TTL file by adding phases and timestamps interactively.

    """
    # Load the parsed TTL file
    g = Graph()
    g.parse(parsed_file, format="turtle")
    g.bind("occp", OCCP)
    g.bind("ould", OULD)
    g.bind("ex", EX)
    g.bind("ae", AE)
    g.bind("rdf", RDF)

    # Ask user for phases
    phases_input = input("Which phases should be included (e.g., 'A, B')? ").strip()
    phases = [p.strip() for p in phases_input.split(",")]

    # Define phase mapping (example)
    phase_map = {"A": "PhaseA_Planning", "B": "PhaseB_Review"}
    for phase in phases:
        phase_uri = AE[f"phase{phase}"]
        g.add((phase_uri, RDF.type, OCCP[phase_map[phase]]))

    # Example instants for phases (hardcoded for simplicity)
    instants = {
        "A": [("1", "Beginning of Planning"), ("2", "Data Procurement")],
        "B": [("3", "Review Start"), ("4", "Review End")]
    }

    # Process elements without subcomponents
    for s in g.subjects(RDF.type, OULD.UpdatableEntity):
        if not list(g.objects(s, OULD.consistsOf)):  # No subcomponents
            print(f"\nProcessing component: {s}")
            for phase in phases:
                instant_options = instants.get(phase, [])
                print(f"Instants for Phase {phase}:")
                for num, label in instant_options:
                    print(f"{num} - {label}")
                selected = input(f"Which instants for {s} in Phase {phase}? (e.g., '1, 2') ").strip()
                selected_nums = [n.strip() for n in selected.split(",")]

                for num in selected_nums:
                    instant_label = next(label for n, label in instant_options if n == num)
                    timestamp = input(f"Enter timestamp (xsd:date) for '{instant_label}': ")
                    g.add((s, OCCP.hasState, Literal(f"{phase}_{instant_label}")))
                    g.add((s, OCCP.timestamp, Literal(timestamp, datatype=rdflib.XSD.date)))

    # Save the updated ABox
    g.serialize(destination=output_file, format="turtle")
    print(f"PreI-ABox saved to: {output_file}")

if __name__ == "__main__":
    parsed_file = "IFC/parsed/Building-Structural_parsed.ttl"
    output_file = "IFC/AE/Building-Structural_parsed_AE.ttl"
    create_preI_abox(parsed_file, output_file)