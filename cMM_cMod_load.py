from rdflib import Graph
import os
import shutil

repo_path = "./GIT_repo"  # GIT-Repository

def load_cmod(timepoint, output_path):
    """Lädt einen cMod basierend auf einem Zeitstempel."""
    cma_path = os.path.join(repo_path, "cMod", "CMA")
    for cma_file in os.listdir(cma_path):
        if not cma_file.endswith(".ttl"):
            continue
        g = Graph()
        g.parse(os.path.join(cma_path, cma_file), format="turtle")
        # SPARQL-Abfrage
        query = f"""
        PREFIX time: <http://www.w3.org/2006/time#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        SELECT ?state WHERE {{
            ?site a <http://example.org/occp#Site> ;
                  <http://example.org/occp#hasState> ?state .
            ?state time:hasTime "{timepoint}"^^xsd:date .
        }}
        """
        results = g.query(query)
        if results:
            # CMA gefunden, lade Dateien
            os.makedirs(output_path, exist_ok=True)
            shutil.copy(os.path.join(cma_path, cma_file), os.path.join(output_path, cma_file))
            # Lade IFC- und Linked Data-Dateien
            for s, p, o in g:
                if str(p) == "http://example.org/occp#filePath":
                    src_file = os.path.join(repo_path, "cMod", str(o))
                    dst_file = os.path.join(output_path, str(o).split("/")[-1])
                    shutil.copy(src_file, dst_file)
            return cma_file
    return None

# Test
cma_file = load_cmod("2025-01-01", "./cmod_restored")
print(f"Loaded cMod with CMA: {cma_file}")