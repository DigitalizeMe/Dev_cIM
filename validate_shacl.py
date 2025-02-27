import subprocess
import os

# Absoluter Pfad zur OCCP TBox und ABox
TBOX_PATH = r"OCCP_TBx_V0.26.ttl"
ABOX_PATH = r"OCCP_Phase_A_inVALID_1.ttl"

# Pfad zur Jena SHACL-Validierung (in doppelte Anführungszeichen setzen!)
JENA_PATH = r"G:\Promo\Apache_Jena\jena-5.2.0\apache-jena"
PELLET_REASONER = os.path.join(JENA_PATH, "bat", "jena_version.bat")  # Pellet in Jena
SHACL_VALIDATE = os.path.join(JENA_PATH, "bat", "shacl.bat")  # SHACL-Validierung

#  Funktion für Pellet-Reasoning
def run_pellet_reasoning(tbox_path, abox_path):
    """ Führt den Pellet-Reasoner in Jena auf der TBox und ABox aus. """
    command = [PELLET_REASONER, "--reasoner", "pellet", "--inf", "--data", abox_path, "--schema", tbox_path]
    result = subprocess.run(command, capture_output=True, text=True)
    print("\n🔍 Pellet Reasoning Output:\n", result.stdout)
    if result.stderr:
        print("\n⚠️ Pellet Fehler:\n", result.stderr)
    return result.stdout

#  Funktion für SHACL-Validierung
def validate_shacl(tbox_path, abox_path):
    """ Führt die SHACL-Validierung mit Jena auf der TBox und ABox aus. """
    command = [SHACL_VALIDATE, "--data", abox_path, "--shapes", tbox_path]
    result = subprocess.run(command, capture_output=True, text=True)
    print("\n✅ SHACL-Validierung Output:\n", result.stdout)
    if result.stderr:
        print("\n⚠️ SHACL Fehler:\n", result.stderr)
    return result.stdout

#  Hauptprogramm: Erst Reasoning, dann Validierung
if __name__ == "__main__":
    print("\n🚀 Starte Pellet-Reasoning...")
    run_pellet_reasoning(TBOX_PATH, ABOX_PATH)

    print("\n🚀 Starte SHACL-Validierung...")
    validate_shacl(TBOX_PATH, ABOX_PATH)