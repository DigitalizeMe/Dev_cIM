import { defineConfig } from 'vite';
import path from 'path';
import copy from 'rollup-plugin-copy';

export default defineConfig({
    root: './templates',
    base: './', // Relative Basis-URL
    plugins: [
        copy({
            targets: [
                { src: 'static/web-ifc.wasm', dest: 'dist/static' }
            ],
            hook: 'writeBundle',
            verbose: true
        })
    ],
    build: {
        outDir: '../dist',
        emptyOutDir: true,
        chunkSizeWarningLimit: 1000,
        rollupOptions: {
            output: {
                manualChunks: {
                    vendor: ['three', '@thatopen/components', '@thatopen/components-front', 'web-ifc']
                }
            }
        },
        assetsInclude: ['../static/web-ifc.wasm']
    },
    resolve: {
        alias: {
            '@thatopen/components': path.resolve(__dirname, 'node_modules/@thatopen/components/dist/index.mjs'),
            '@thatopen/components-front': path.resolve(__dirname, 'node_modules/@thatopen/components-front/dist/index.js'),
            'three': path.resolve(__dirname, 'node_modules/three/build/three.module.js'),
            '@thatopen/fragments': path.resolve(__dirname, 'node_modules/@thatopen/fragments/dist/index.mjs'),
            'web-ifc': path.resolve(__dirname, 'node_modules/web-ifc/web-ifc-api.js')
        }
    },
    optimizeDeps: {
        include: ['@thatopen/components', '@thatopen/components-front', 'three', '@thatopen/fragments', 'web-ifc']
    }
});