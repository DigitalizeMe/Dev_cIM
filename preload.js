const { contextBridge } = require('electron');
const fs = require('fs').promises;
const path = require('path');

contextBridge.exposeInMainWorld('electronAPI', {
    readdir: async (dir) => {
        try {
            return await fs.readdir(dir);
        } catch (err) {
            console.error('Error reading directory:', err);
            throw err;
        }
    },
    pathJoin: (...args) => path.join(__dirname, ...args),
    readFile: async (filePath) => {
        try {
            const buffer = await fs.readFile(filePath);
            return new Uint8Array(buffer);
        } catch (err) {
            console.error('Error reading file:', err);
            throw err;
        }
    },
    readWasm: async () => {
        try {
            const wasmPath = path.join(__dirname, 'static', 'web-ifc.wasm');
            console.log('Reading WASM file from:', wasmPath); // Debugging
            const buffer = await fs.readFile(wasmPath);
            return new Uint8Array(buffer);
        } catch (err) {
            console.error('Error reading WASM file:', err);
            throw err;
        }
    }
});