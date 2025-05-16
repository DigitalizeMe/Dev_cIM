import hashlib
import os
import shutil
from git import Repo
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF
from datetime import datetime

# Pfade
cmod_input_path = "./cmod_test"  # Hauptordner für Input
cmod_input_path_IFC = os.path.join(cmod_input_path, "IFC")
cmod_input_path_CMA = os.path.join(cmod_input_path, "CMA")
cmod_input_path_LD = os.path.join(cmod_input_path, "Linked_Data")
repo_path = "./GIT_repo"  # GIT-Repository
cmod_id = f"cmod_{datetime.now().strftime('%Y%m%d_%H%M%S')}"  # Eindeutige ID

# Initialisiere Repository
def init_repo(repo_path):
    """Initialisiert ein GIT-Repository oder verwendet ein bestehendes."""
    if os.path.exists(repo_path):
        try:
            repo = Repo(repo_path)
            if repo.bare or not os.path.exists(os.path.join(repo_path, ".git")):
                raise ValueError("Ungültiges GIT-Repository")
            return repo
        except:
            shutil.rmtree(repo_path, ignore_errors=True)  # Lösche ungültiges Repository
    os.makedirs(repo_path, exist_ok=True)
    return Repo.init(repo_path)

repo = init_repo(repo_path)

def calculate_file_hash(file_path):
    """Berechnet den SHA256-Hash einer Datei."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def save_cmod(cmod_input_path_IFC, cmod_input_path_LD, cmod_id, timepoint, commit_message):
    """Speichert einen cMod im GIT-Repository."""
    # Ziel-Ordner
    cmod_path = os.path.join(repo_path, "cMod")
    ifc_path = os.path.join(cmod_path, "IFC")
    cma_path = os.path.join(cmod_path, "CMA")
    linked_data_path = os.path.join(cmod_path, "Linked_Data")
    os.makedirs(ifc_path, exist_ok=True)
    os.makedirs(cma_path, exist_ok=True)
    os.makedirs(linked_data_path, exist_ok=True)

    # RDF-Graph für CMA
    g = Graph()
    OCCP = Namespace("http://example.org/occp#")
    TIME = Namespace("http://www.w3.org/2006/time#")
    XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
    OULD = Namespace("http://www.semanticweb.org/DigitalizeMe/ontologies/2024/OULD#")
    g.bind("occp", OCCP)
    g.bind("time", TIME)
    g.bind("ould", OULD)

    # Verarbeite IFC-Dateien
    ifc_files = [f for f in os.listdir(cmod_input_path_IFC) if f.endswith(".ifc")] if os.path.exists(cmod_input_path_IFC) else []
    for ifc_file in ifc_files:
        src_file = os.path.join(cmod_input_path_IFC, ifc_file)
        file_hash = calculate_file_hash(src_file)
        # Prüfe, ob Datei mit gleichem Hash existiert
        existing_file = None
        for existing in os.listdir(ifc_path):
            if calculate_file_hash(os.path.join(ifc_path, existing)) == file_hash:
                existing_file = existing
                break
        if existing_file:
            ifc_filename = existing_file
        else:
            ifc_filename = f"{ifc_file.replace('.ifc', '')}_{file_hash[:8]}.ifc"
            shutil.copy(src_file, os.path.join(ifc_path, ifc_filename))
        # Füge zur CMA hinzu
        g.add((OCCP.Site_123, RDF.type, OCCP.Site))
        g.add((OCCP.Site_123, OCCP.hasHash, Literal(file_hash)))
        g.add((OCCP.Site_123, OCCP.filePath, Literal(f"IFC/{ifc_filename}")))
        g.add((OCCP.Site_123, OCCP.hasState, OCCP.State_456))
        g.add((OCCP.State_456, TIME.hasTime, Literal(timepoint, datatype=XSD.date)))

    # Verarbeite Linked Data-Dateien
    linked_data_files = [f for f in os.listdir(cmod_input_path_LD) if f.endswith(".txt")] if os.path.exists(cmod_input_path_LD) else []
    for ld_file in linked_data_files:
        src_file = os.path.join(cmod_input_path_LD, ld_file)
        file_hash = calculate_file_hash(src_file)
        # Prüfe, ob Datei mit gleichem Hash existiert
        existing_file = None
        for existing in os.listdir(linked_data_path):
            if calculate_file_hash(os.path.join(linked_data_path, existing)) == file_hash:
                existing_file = existing
                break
        if existing_file:
            ld_filename = existing_file
        else:
            ld_filename = f"{ld_file.replace('.txt', '')}_{file_hash[:8]}.txt"
            shutil.copy(src_file, os.path.join(linked_data_path, ld_filename))
        # Füge zur CMA hinzu
        datasheet_id = f"Datasheet_{ld_filename.replace('.txt', '')}"
        g.add((OCCP.Roof_789, RDF.type, OCCP.Component))
        g.add((OCCP.Roof_789, OCCP.hasDatasheet, OCCP[datasheet_id]))
        g.add((OCCP[datasheet_id], OCCP.filePath, Literal(f"Linked_Data/{ld_filename}")))
        g.add((OCCP[datasheet_id], OCCP.hasHash, Literal(file_hash)))

    # Speichere CMA
    cma_file = os.path.join(cma_path, f"OCCP_Pre_{cmod_id}.ttl")
    g.serialize(cma_file, format="turtle")

    # Commit
    repo.index.add([os.path.join("cMod", "IFC", f) for f in os.listdir(ifc_path)])
    repo.index.add([os.path.join("cMod", "CMA", f) for f in os.listdir(cma_path)])
    repo.index.add([os.path.join("cMod", "Linked_Data", f) for f in os.listdir(linked_data_path)])
    repo.index.commit(commit_message)
    return repo.head.commit.hexsha

# Test
try:
    commit_hash = save_cmod(cmod_input_path_IFC, cmod_input_path_LD, cmod_id, "2025-01-02", "Save cMod")
    print(f"Saved cMod with commit hash: {commit_hash}")
except Exception as e:
    print(f"Error: {e}")