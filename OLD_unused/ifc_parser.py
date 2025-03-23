import ifcopenshell

def parse_ifc_to_turtle(ifc_file_path, output_turtle_path):
    """
    Parses an IFC file and saves the structure as a Turtle file.
    """
    try:
        # IFC-Datei öffnen
        ifc_file = ifcopenshell.open(ifc_file_path)
        print(f"IFC-file successfully loaded: {ifc_file_path}")
    except Exception as e:
        print(f"Error while loading IFC-file: {e}")
        return

    # Bauteile extrahieren
    components = {}
    for element in ifc_file.by_type("IfcProduct"):
        if element.is_a("IfcOpeningElement"):
            continue  # Öffnungen ignorieren

        element_type = element.is_a()  # z. B. IfcWall
        element_name = element.Name if hasattr(element, "Name") and element.Name else "Unnamed"
        element_global_id = element.GlobalId

        # Bauteile nach Typ sammeln
        if element_type not in components:
            components[element_type] = []
        components[element_type].append((element_global_id, element_name))

    # Turtle-Datei schreiben
    with open(output_turtle_path, "w", encoding="utf-8") as turtle_file:
        # Präfixe definieren (anpassbar je nach deiner Ontologie)
        turtle_file.write("@prefix occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#> .\n")
        turtle_file.write("@prefix ould: <http://www.semanticweb.org/albrechtvaatz/ontologies/2024/OULD#> .\n")
        turtle_file.write("@prefix ex: <http://example.org/example#> .\n\n")

        # Bauteile als Turtle-Tripel schreiben
        for element_type, elements in components.items():
            for global_id, name in elements:
                turtle_file.write(f"ex:{name} a ould:UpdatableEntity ;\n")
                turtle_file.write(f"    ould:hasIFCID \"{global_id}\" ;\n")
                turtle_file.write(f"    occp:type \"{element_type}\" .\n\n")

    print(f"Turtle-Datei erfolgreich gespeichert: {output_turtle_path}")

if __name__ == "__main__":
    # Pfad zur IFC-Datei
    ifc_file_path = "IFC/Building-Architecture.ifc"
    # Pfad zur Ausgabe-Turtle-Datei
    output_turtle_path = "IFC/parsed/Building-Architecture_parsed.ttl"

    # IFC-Datei parsen und Turtle-Datei erzeugen
    parse_ifc_to_turtle(ifc_file_path, output_turtle_path)