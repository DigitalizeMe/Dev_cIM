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

# IFC-Viewer (openbim-components über HTTP-Server)
st.subheader("IFC-Modell")
html = f"""
<div style="width: 100%; height: 500px; border: 1px solid black;">
    <canvas id="three-canvas" style="width: 100%; height: 100%;"></canvas>
</div>
<script async src="http://localhost:8000/static/es-module-shims.js"></script>
<script type="importmap">
{{
    "imports": {{
        "three": "http://localhost:8000/static/three.module.min.js",
        "three/core/": "http://localhost:8000/static/",
        "three/addons/": "http://localhost:8000/static/addons/"
    }}
}}
</script>
<script type="module">
    try {{
        console.log('Starte Modul-Ladevorgang...');
        // Prüfe WebGL-Unterstützung
        const canvas = document.createElement('canvas');
        const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
        if (!gl) {{
            throw new Error('WebGL wird vom Browser nicht unterstützt');
        }}
        console.log('WebGL unterstützt');

        // Importe
        import * as THREE from 'three';
        console.log('THREE geladen:', THREE);
        const obcModule = await import('http://localhost:8000/static/components.js');
        const obcfModule = await import('http://localhost:8000/static/components-front.js');
        console.log('OBC-Module geladen:', obcModule, obcfModule);

        const OBC = obcModule.default || obcModule;
        const OBCF = obcfModule.default || obcfModule;

        if (!THREE || !OBC) {{
            throw new Error('THREE oder OBC nicht definiert');
        }}
        console.log('THREE:', THREE);
        console.log('OBC:', OBC);

        const container = document.getElementById('three-canvas');
        if (!container) {{
            throw new Error('Canvas-Element nicht gefunden');
        }}
        console.log('Canvas gefunden:', container);

        const components = new OBC.Components();
        console.log('Components initialisiert:', components);

        components.scene = new OBC.SimpleScene(components);
        components.renderer = new OBC.SimpleRenderer(components, container);
        components.camera = new OBC.SimpleCamera(components);
        components.raycaster = new OBC.SimpleRaycaster(components);
        components.init();
        console.log('Renderer initialisiert:', components.renderer);

        const ifcLoader = components.tools.get(OBC.IfcLoader);
        console.log('IFC-Loader abgerufen:', ifcLoader);
        await ifcLoader.setup().catch(e => {{
            throw new Error('IFC-Loader Setup fehlgeschlagen: ' + e.message);
        }});
        console.log('IFC-Loader bereit');

        const ifcUrl = 'http://localhost:8000/cmod_restored/{ifc_file}';
        console.log('Lade IFC von:', ifcUrl);

        const response = await fetch(ifcUrl);
        if (!response.ok) {{
            throw new Error('Fehler beim Laden der IFC-Datei: ' + response.statusText);
        }}
        console.log('IFC-Antwort erhalten:', response);

        const buffer = await response.arrayBuffer();
        console.log('IFC-Daten geladen, Buffer-Größe:', buffer.byteLength);

        const model = await ifcLoader.load(new Uint8Array(buffer)).catch(e => {{
            throw new Error('Fehler beim Parsen der IFC-Datei: ' + e.message);
        }});
        console.log('Modell geladen:', model);

        components.scene.setup();
        components.camera.controls.setLookAt(10, 10, 10, 0, 0, 0);
        console.log('Szene eingerichtet, Kamera positioniert');
    }} catch (e) {{
        console.error('Fehler beim Laden des IFC-Modells:', e);
    }}
</script>
"""
st.components.v1.html(html, height=600)

# IFC-Metadaten
st.subheader("IFC-Metadaten")
try:
    ifc = ifcopenshell.open(os.path.join(cmod_path, ifc_file))
    for element in ifc.by_type("IfcElement")[:5]:
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