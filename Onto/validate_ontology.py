import argparse
from rdflib import Graph
import org.apache.jena.shacl.Shapes
import org.apache.jena.shacl.validation.ShaclPlainValidator
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def validate_ontology(abox_path, shapes_path, output_format="json"):
    """
    Validates an ontology ABOX against SHACL shapes using Jena.
    Args:
        abox_path (str): Path to the ABOX file (Turtle format).
        shapes_path (str): Path to the SHACL shapes file (Turtle format).
        output_format (str): Output format for the report ("json" or "ttl").
    Returns:
        dict: Validation result and report.
    """
    try:
        logging.info(f"Loading ABOX: {abox_path}")
        abox = Graph()
        abox.parse(abox_path, format="turtle")

        logging.info(f"Loading shapes: {shapes_path}")
        shapes_graph = Graph()
        shapes_graph.parse(shapes_path, format="turtle")

        # Convert to Jena models
        jena_abox = org.apache.jena.rdf.model.ModelFactory.createModelForGraph(abox.graph)
        jena_shapes = org.apache.jena.rdf.model.ModelFactory.createModelForGraph(shapes_graph.graph)

        # Run SHACL validation
        logging.info("Running SHACL validation")
        shapes = Shapes.parse(jena_shapes)
        validator = ShaclPlainValidator()
        report = validator.validate(shapes, jena_abox)
        conforms = not report.contains(None, None, None)

        # Save report
        report_path = "validation_report.ttl"
        report.write(None, "TURTLE", report_path)
        logging.info(f"Validation report saved to {report_path}")

        result = {
            "conforms": conforms,
            "report": report.write(None, "TURTLE")
        }

        if output_format == "json":
            with open("validation_result.json", "w") as f:
                json.dump(result, f, indent=2)
            logging.info("Report saved to validation_result.json")

        return result
    except Exception as e:
        logging.error(f"Validation failed: {str(e)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate ontology with SHACL shapes.")
    parser.add_argument("--abox", required=True, help="Path to ABOX file")
    parser.add_argument("--shapes", required=True, help="Path to SHACL shapes file")
    parser.add_argument("--format", default="json", choices=["json", "ttl"], help="Output format")
    args = parser.parse_args()

    result = validate_ontology(args.abox, args.shapes, args.format)
    logging.info(f"Conforms: {result['conforms']}")