# hermit_reasoner_ocp.py

from owlready2 import get_ontology, onto_path, sync_reasoner_pellet
import os
import logging

# Logging Setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(
    filename=os.path.join(BASE_DIR, "reasoning.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w"
)
logger = logging.getLogger(__name__)

# Ontology-Dateien (relativ zum Projekt)
COMBINED_TBOX_PATH = os.path.join("Onto", "TBOX", "OCP_TBOX.owl")
OCP_ABOX_PATH = os.path.join("Onto", "ABOX", "OCP", "OCP_ABOX_13.owl")
INFERRED_OUT_PATH = os.path.join("Onto", "ABOX", "OCP", "POST_ABOX", "Reasoner", "OCP_ABOX_13_inferred.ttl")

# Set path for owlready2 to look for ontologies
onto_path.append(os.path.dirname(COMBINED_TBOX_PATH))

def run_reasoning():
    logger.info("Starte Reasoning mit HermiT über OWLReady2...")

    if not os.path.exists(COMBINED_TBOX_PATH):
        logger.error(f"Kombinierte TBox nicht gefunden: {COMBINED_TBOX_PATH}")
        return False
    if not os.path.exists(OCP_ABOX_PATH):
        logger.error(f"ABox nicht gefunden: {OCP_ABOX_PATH}")
        return False

    try:
        # Lade TBox und ABox
        onto_combined = get_ontology(f"file://{os.path.abspath(COMBINED_TBOX_PATH)}").load()
        abox = get_ontology(f"file://{os.path.abspath(OCP_ABOX_PATH)}").load()

        logger.info("Ontologien erfolgreich geladen. ABox-Axiome werden übertragen...")

        # ABox-Axiome in TBox übernehmen
        for ax in abox.axioms():
            onto_combined._add_axiom(ax)

        logger.info("Reasoning wird ausgeführt...")
        with onto_combined:
            sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)

        logger.info(f"Speichere Inferenz-ABox nach: {INFERRED_OUT_PATH}")
        onto_combined.save(file=INFERRED_OUT_PATH, format="turtle")
        logger.info("Reasoning abgeschlossen und Datei gespeichert.")
        return True

    except Exception as e:
        logger.error(f"Fehler beim Reasoning: {e}")
        return False


if __name__ == "__main__":
    result = run_reasoning()
    print(f"Reasoning erfolgreich: {result}")

