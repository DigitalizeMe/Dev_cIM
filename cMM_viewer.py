import streamlit as st
import ifcopenshell
from rdflib import Graph
import os

# Streamlit-App
st.title("cMod-Manager Prototyp")

# Pfad zum geladenen cMod
cmod_path = "./cmod_restored"

# Finde CMA-, IFC- und Linked Data-Dateien
cma_files = [f for f in os.listdir(cmod_path) if f.endswith(".ttl")]
ifc_files = [f for f in os.listdir(cmod_path) if f.endswith(".ifc")]
linked_data_files = [f for f in os.listdir(cmod_path) if f.endswith(".txt")]

if not cma_files or not ifc_files:
    st.error("Keine CMA- oder IFC-Datei in cmod_restored gefunden. Bitte führe load_cmod aus.")
    st.stop()

cma_file = cma_files[0]
ifc_file = ifc_files[0]

# IFC-Viewer (web-ifc-viewer)
st.subheader("IFC-Modell")
html = f"""
<div style="width: 100%; height: 500px;">
    <canvas id="three-canvas"></canvas>
</div>
<script src="https://unpkg.com/three@0.126.1/build/three.min.js"></script>
<script src="https://unpkg.com/@thatopen/web-ifc-viewer@2.0.33/dist/web-ifc-viewer.min.js"></script>
<script>
    const container = document.getElementById('three-canvas');
    const viewer = new WebIFCViewer.IfcViewerAPI({{ container, backgroundColor: {{ r: 0.9, g: 0.9, b: 0.9 }} }});
    viewer.axes.setAxes();
    viewer.grid.setGrid();

    async function loadIfc() {{
        try {{
            const ifcUrl = '{os.path.join(cmod_path, ifc_file)}';
            await viewer.IFC.loadIfcUrl(ifcUrl);
            viewer.context.renderer.fitTo();
        }} catch (e) {{
            console.error('Fehler beim Laden des IFC-Modells:', e);
        }}
    }}
    loadIfc();
</script>
"""
st.components.v1.html(html, height=600)

# IFC-Metadaten
st.subheader("IFC-Metadaten")
try:
    ifc = ifcopenshell.open(os.path.join(cmod_path, ifc_file))
    for element in ifc.by_type("IfcElement")[:5]:  # Erste 5 Elemente
        st.write(f"Element: {element.Name or 'Unnamed'}, GUID: {element.GlobalId}")
except Exception as e:
    st.error(f"Fehler beim Laden der IFC-Datei: {e}")

# CMA-Informationen
st.subheader("CMA-Informationen")
try:
    g = Graph()
    g.parse(os.path.join(cmod_path, cma_file), format="turtle")
    for s, p, o in g:
        st.write(f"{s} {p} {o}")
except Exception as e:
    st.error(f"Fehler beim Parsen der CMA: {e}")

# Linked Data-Links
st.subheader("Linked Data")
if linked_data_files:
    for file in linked_data_files:
        file_path = os.path.join(cmod_path, file)
        st.markdown(f"[Download {file}]({file_path})")
else:
    st.write("Keine Linked Data-Dateien gefunden.")