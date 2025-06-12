# OCP_Main.py

import os
from ocp_construct_queries import enrich_time_types
from validate_shacl_OCP import load_and_validate_ocp

ABOX_FILENAME = "OCP_ABOX_14.ttl"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ABOX_PATH = os.path.join("Onto", "ABOX", "OCP", ABOX_FILENAME)
CONSTRUCTED_DIR = os.path.join("Onto", "ABOX", "OCP", "POST_ABOX", "CONSTRUCT")
CONSTRUCTED_ABOX_PATH = os.path.join(CONSTRUCTED_DIR, ABOX_FILENAME.replace(".ttl", "_TIME.ttl"))

# Step 1: Run CONSTRUCT-Queries 
os.makedirs(CONSTRUCTED_DIR, exist_ok=True)
enrich_time_types(ABOX_PATH, CONSTRUCTED_ABOX_PATH)

# Step 2: Validiation (Reasoning & SHACL) with inferred ABOX
print("\n=== Starting Validation ===")
conforms = load_and_validate_ocp(input_abox_path=CONSTRUCTED_ABOX_PATH)
print(f"\nSHACL Validation Result: {conforms}")
