import subprocess

# Absoluter Pfad zur OCCP TBox und ABox
TBOX_PATH = r"OCCP_TBx_V0.26.ttl"
ABOX_PATH = r"OCCP_Phase_A_VALID_1.ttl"

# Pfad zur Jena SHACL-Validierung (in doppelte Anführungszeichen setzen!)
JENA_PATH = r'"C:\Program Files (x86)\jena-5.2.0\apache-jena\bat\shacl.bat"'

def validate_shacl(tbox, abox):
    # Der eigentliche Befehl für SHACL-Validierung
    command = f'{JENA_PATH} validate --data {abox} --shapes {tbox}'

    # Starte den Befehl über subprocess und fange die Ausgabe ab
    result = subprocess.run(command, capture_output=True, text=True, shell=True)

    if "Constraint Violation" in result.stdout:
        print("❌ SHACL Validation Failed:")
        print(result.stdout)
    else:
        print("✅ SHACL Validation Passed!")

if __name__ == "__main__":
    validate_shacl(TBOX_PATH, ABOX_PATH)