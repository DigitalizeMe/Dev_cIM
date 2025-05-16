import rdflib
from rdflib import Graph, Literal, Namespace
import re

# Define namespaces
OCCP = Namespace("http://www.semanticweb.org/DigitalizeMe/ontologies/2022/9/cMod_V0.1#")
OULD = Namespace("http://www.semanticweb.org/DigitalizeMe/ontologies/2024/OULD#")
EX = Namespace("http://example.org/example#")
AE = Namespace("http://example.org/autoedit#")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")

def create_preI_abox(parsed_file, output_file):
    """
    Creates a PreI-ABox from a parsed TTL file by adding phases and instants interactively.
    
    Args:
        parsed_file (str): Path to the parsed TTL file.
        output_file (str): Path to the output PreI-ABox file.
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
    if phases_input.lower() == "abort":
        print("Process aborted.")
        return
    phases = [p.strip() for p in phases_input.split(",")]

    # Define phase mapping (example, later from TBox)
    phase_map = {"A": "PhaseA_Planning", "B": "PhaseB_Review"}

    # Example instants for phases (example, later from TBox)
    instants = {
        "A": [("1", "BeginningOfPlanning"), ("2", "DataProcurement")],
        "B": [("3", "ReviewStart"), ("4", "ReviewEnd")]
    }

    # Process elements without subcomponents
    for s in g.subjects(RDF.type, OULD.UpdatableEntity):
        if not list(g.objects(s, OULD.consistsOf)):  # No subcomponents
            component_name = str(s).split("#")[-1]  # Extract name from URI
            print(f"\nProcessing component: {component_name}")

            for phase in phases:
                instant_options = instants.get(phase, [])
                print(f"Instants for Phase {phase}:")
                for num, label in instant_options:
                    print(f"{num} - {label.replace('Of', ' of ')}")
                selected = input(f"Which instants for {component_name} in Phase {phase}? (e.g., '1, 2' or 'abort') ").strip()
                if selected.lower() == "abort":
                    g.serialize(destination=output_file, format="turtle")
                    print("Process aborted. Partial ABox saved to:", output_file)
                    return
                selected_nums = [n.strip() for n in selected.split(",")]

                # Only proceed if at least one instant is selected
                if selected_nums:
                    # Create individual phase for this component after instant selection
                    phase_uri = AE[f"phase{phase}_{component_name}"]
                    g.add((phase_uri, RDF.type, OCCP[phase_map[phase]]))
                    g.add((s, OCCP.hasPhase, phase_uri))  # Link component to its phase

                    for num in selected_nums:
                        instant_label = next(label for n, label in instant_options if n == num)
                        instant_uri = AE[f"instant_{instant_label}_{component_name}"]

                        # Create instant individual
                        g.add((instant_uri, RDF.type, OCCP[instant_label]))
                        g.add((instant_uri, OCCP.startsPhase, phase_uri))

                        # Get timestamp with validation
                        while True:
                            timestamp = input(f"Enter timestamp (xsd:date, e.g., '2025-01-01') for '{instant_label}': ").strip()
                            if timestamp.lower() == "abort":
                                g.serialize(destination=output_file, format="turtle")
                                print("Process aborted. Partial ABox saved to:", output_file)
                                return
                            if re.match(r"^\d{4}-\d{2}-\d{2}$", timestamp):
                                break
                            print("Invalid format. Please use 'YYYY-MM-DD'.")

                        # Ask if estimated or actual
                        while True:
                            est = input("Is this timestamp estimated (Y/N)? ").strip().upper()
                            if est.lower() == "abort":
                                g.serialize(destination=output_file, format="turtle")
                                print("Process aborted. Partial ABox saved to:", output_file)
                                return
                            if est in ["Y", "N"]:
                                break
                            print("Please enter 'Y' or 'N'.")
                        
                        time_prop = OCCP.hasEstimatedTime if est == "Y" else OCCP.hasActualTime
                        g.add((instant_uri, time_prop, Literal(timestamp, datatype=XSD.date)))

    # Save the updated ABox
    g.serialize(destination=output_file, format="turtle")
    print(f"PreI-ABox saved to: {output_file}")

if __name__ == "__main__":
    parsed_file = "IFC/parsed/Building-Structural_parsed.ttl"
    output_file = "IFC/AE/Building-Structural_parsed_AE.ttl"
    create_preI_abox(parsed_file, output_file)