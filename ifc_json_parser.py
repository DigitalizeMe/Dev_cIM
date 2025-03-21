import ifcopenshell
import json
import os
import hashlib

def parse_ifc_to_json(ifc_file_path, output_json_path):
    """
    Parses an IFC file and saves the structure as a clustered JSON file with type count and model hash.
    """
    try:
        # Load the IFC file
        ifc_file = ifcopenshell.open(ifc_file_path)
        print(f"IFC file successfully loaded: {ifc_file_path}")
    except Exception as e:
        print(f"Error loading IFC file: {e}")
        return
    
    # Calculate hash of the entire IFC file
    model_hash = calculate_file_hash(ifc_file_path)

    # Extract and cluster components
    components = {}
    for element in ifc_file.by_type("IfcProduct"):
        if element.is_a("IfcOpeningElement"):
            continue  # Ignore openings

        # Get element type, name, and GlobalId
        element_type = element.is_a()
        element_name = element.Name if hasattr(element, "Name") and element.Name else "Unnamed"
        element_global_id = element.GlobalId

        # Calculate hash value using GlobalId and name
        hash_value = hashlib.sha256(f"{element_global_id}{element_name}".encode()).hexdigest()

         # Cluster by type, then by name
        if element_type not in components:
            components[element_type] = {"_count1": 0}
        if element_name not in components[element_type]:
            components[element_type][element_name] = {"_count2": 0, "GlobalIds": [], "hash": hash_value}
            components[element_type]["_count1"] += 1  # Increment count for unique names

        components[element_type][element_name]["GlobalIds"].append(element_global_id)
        components[element_type][element_name]["_count2"] += 1

    # Add total type count and model hash to the JSON structure
    total_types = len(components)
    result = {
        "_total_type_count": total_types,
        "model_hash": model_hash,  # Store the hash of the entire model
        "Types": components
    }

    # Save the result to a JSON file
    try:
        os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
        with open(output_json_path, "w", encoding="utf-8") as json_file:
            json.dump(result, json_file, indent=4, ensure_ascii=False)
        print(f"JSON file successfully saved: {output_json_path}")
    except Exception as e:
        print(f"Error saving JSON file: {e}")

def calculate_file_hash(file_path):
    """
    Calculates the SHA-256 hash of the entire file.
    
    Args:
        file_path (str): Path to the file.
    Returns:
        str: The hexadecimal representation of the file's hash.
    """
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()        

if __name__ == "__main__":
    # Path to the IFC file
    ifc_file_path = "IFC/Building-Architecture.ifc"
    # Path to the output JSON file
    output_json_path = "IFC/parsed/Building-Architecture_parsed.json"

    # Parse the IFC file and save the structure as JSON
    parse_ifc_to_json(ifc_file_path, output_json_path)
