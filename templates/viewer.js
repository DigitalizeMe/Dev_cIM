import * as OBC from '@thatopen/components';
import * as OBF from '@thatopen/components-front';
import * as THREE from 'three';

console.log('OBC loaded:', OBC);
console.log('OBF loaded:', OBF);
console.log('THREE loaded:', THREE);

function showToast(message, type = "info") {
    Toastify({
        text: message,
        duration: 3000,
        gravity: "top",
        position: "right",
        style: {
            background: type === "error" ? "#ff4444" : "#00C851"
        }
    }).showToast();
}

async function populateIfcSelector() {
    try {
        const ifcDir = await window.electronAPI.pathJoin('cmod_restored');
        const files = await window.electronAPI.readdir(ifcDir);
        const ifcFiles = files.filter(file => file.endsWith('.ifc'));
        const selector = document.getElementById('ifcSelector');
        ifcFiles.forEach(file => {
            const option = document.createElement('option');
            option.value = file;
            option.textContent = file;
            selector.appendChild(option);
        });
        console.log('IFC files loaded:', ifcFiles);
    } catch (error) {
        console.error('Error loading IFC files:', error);
        showToast('Failed to load IFC files', "error");
    }
}

async function initViewer() {
    try {
        const container = document.getElementById("viewer-container");
        if (!container) {
            throw new Error("Viewer container not found");
        }
        console.log('Viewer container found:', container);

        const components = new OBC.Components();
        console.log('Components initialized:', components);

        const worlds = components.get(OBC.Worlds);
        const world = worlds.create();
        console.log('World created:', world);

        world.scene = new OBC.SimpleScene(components);
        world.renderer = new OBC.SimpleRenderer(components, container);
        world.camera = new OBC.SimpleCamera(components);
        console.log('Scene, renderer, camera set:', world.scene, world.renderer, world.camera);
        console.log('Renderer three.domElement:', world.renderer.three.domElement);

        components.init();
        world.camera.controls.setLookAt(12, 6, 8, 0, 0, -10);
        world.scene.setup();

        const ifcLoader = components.get(OBC.IfcLoader);
        console.log('IfcLoader:', ifcLoader);
        await ifcLoader.setup();
        ifcLoader.settings.wasm = {
            path: './static/',
            absolute: false
        };
        console.log('IfcLoader configured:', ifcLoader.settings.wasm);

        console.log('Viewer initialized:', components);
        return { components, world, ifcLoader };
    } catch (error) {
        console.error('Error initializing viewer:', error);
        showToast('Failed to initialize viewer: ' + error.message, "error");
        throw error;
    }
}

async function loadIFC(filename) {
    if (!filename) {
        showToast("Please select an IFC file", "error");
        return;
    }
    try {
        showToast(`Loading ${filename}...`, "info");
        const { components, world, ifcLoader } = await initViewer();
        const filePath = await window.electronAPI.pathJoin('cmod_restored', filename);
        const buffer = await window.electronAPI.readFile(filePath);
        const model = await ifcLoader.load(buffer);
        world.scene.three.add(model);
        showToast(`${filename} loaded successfully`, "info");

        const highlighter = components.get(OBF.Highlighter);
        console.log('Highlighter loaded:', highlighter);
        await highlighter.setup({
            world,
            selection: { default: {} } // Automatische Standardauswahl
        });
        console.log('Highlighter configured with default selection');

        if (world.renderer && world.renderer.three && world.renderer.three.domElement) {
            console.log('Adding click event listener to:', world.renderer.three.domElement);
            world.renderer.three.domElement.addEventListener('click', async () => {
                const result = await highlighter.highlight('default');
                if (result) {
                    const { fragment, id } = result;
                    showToast(`Selected component: ${id}`, "info");
                }
            });
        } else {
            console.error('Renderer three.domElement not available:', world.renderer);
            showToast('Click interaction not available: Renderer not initialized', "error");
        }
    } catch (error) {
        console.error('Error loading IFC:', error);
        showToast(`Failed to load ${filename}: ${error.message}`, "error");
    }
}

document.addEventListener('DOMContentLoaded', () => {
    populateIfcSelector();
    const selector = document.getElementById('ifcSelector');
    if (selector) {
        selector.addEventListener('change', (event) => {
            const filename = event.target.value;
            console.log('Selected IFC file:', filename);
            loadIFC(filename);
        });
        console.log('Dropdown event listener attached');
    } else {
        console.error('Dropdown element not found');
        showToast('Dropdown element not found', "error");
    }
});