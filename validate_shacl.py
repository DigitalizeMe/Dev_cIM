import subprocess

TBOX_PATH = "OCCP_V0.26.ttl"
ABOX_PATH = "OCCP_Phase_A_VALID_1.ttl"

JENA_PATH = r"C:\Program Files (x86)\jena-5.2.0\apache-jena\bat\shacl.bat"

# Run Apache Jena SHACL-Validator 
def validate_shacl(tbox, abox):
    command = [
        "shaclvalidate",
        "-datafile", abox,
        "-shapesfile", tbox
    ]
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    if "Constraint Violation" in result.stdout:
        print("❌ SHACL Validation Failed:")
        print(result.stdout)
    else:
        print("✅ SHACL Validation Passed!")

# Run script
if __name__ == "__main__":
    validate_shacl(TBOX_PATH, ABOX_PATH)
