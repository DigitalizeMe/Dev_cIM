# validate_shacl_OCP.py 

import os
import logging
import subprocess

# === Konfigurierbare Pfade (zentral) ===
COMBINED_TBOX_PATH = os.path.join("Onto", "TBOX", "TIME+OCP_TBOX_clean.ttl")
OCP_SHAPES_PATH = os.path.join("Onto", "TBOX", "OCP_SHACL-Shapes.ttl")
REASONER_OUT_DIR = os.path.join("Onto", "ABOX", "OCP", "POST_ABOX", "Reasoner")

# === Logging ===
logging.basicConfig(
    filename="validation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w"
)
logger = logging.getLogger(__name__)

# === Reasoning-Schritt (Jena via CLI) ===
def perform_jena_reasoning(input_abox, tbox, output_abox):
    # Passe ggf. Pfad zu infer.bat an!
    jena_cmd = os.path.join("apache-jena-5.3.0", "bat", "infer.bat")
    cmd = f'"{jena_cmd}" --data "{input_abox}" --tbox "{tbox}" --out TTL > "{output_abox}"'
    logger.info(f"Starte Jena Reasoning: {cmd}")
    ret = subprocess.call(cmd, shell=True)
    if os.path.exists(output_abox):
        logger.info(f"Inferred ABox erstellt: {output_abox}")
        return True
    else:
        logger.error(f"Inferred ABox wurde NICHT erstellt: {output_abox}")
        return False

# === SHACL-Validation (Jena via CLI) ===
def perform_shacl_jena_validation(input_abox):
    shacl_cmd = os.path.join("apache-jena-5.3.0", "bat", "shacl.bat")
    cmd = f'"{shacl_cmd}" validate --data "{input_abox}" --shapes "{OCP_SHAPES_PATH}"'
    logger.info(f"Starte SHACL Validierung: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    logger.info(f"SHACL-Output: {result.stdout}")
    return "conforms: true" in result.stdout.lower()

# === Hauptfunktion: alles steuern ===
def load_and_validate_ocp(input_abox_path):
    os.makedirs(REASONER_OUT_DIR, exist_ok=True)
    input_abox = input_abox_path
    output_abox = os.path.join(REASONER_OUT_DIR,
                               os.path.basename(input_abox).replace(".ttl", "_inferred.ttl"))

    if not all(os.path.exists(p) for p in [input_abox, COMBINED_TBOX_PATH, OCP_SHAPES_PATH]):
        logger.error("Input-Dateien fehlen!")
        return False

    logger.info("==== Reasoning + Validation Workflow gestartet ====")
    if not perform_jena_reasoning(input_abox, COMBINED_TBOX_PATH, output_abox):
        logger.error("Reasoning fehlgeschlagen. Abbruch.")
        return False

    result = perform_shacl_jena_validation(output_abox)
    logger.info(f"SHACL Validation result: {result}")
    return result

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        load_and_validate_ocp(sys.argv[1])
    else:
        print("Verwendung: python validate_shacl_35_OCP.py <input_abox.ttl>")