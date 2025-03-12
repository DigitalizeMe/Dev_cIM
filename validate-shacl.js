import rdf from '@zazuko/env-node';
import SHACLValidator from 'rdf-validate-shacl';
import { writeFileSync } from 'fs';

async function validate(dataFile, shapesFile) {
    try {
        const shapes = await rdf.dataset().import(rdf.fromFile(shapesFile));
        const data = await rdf.dataset().import(rdf.fromFile(dataFile));
        const validator = new SHACLValidator(shapes, { factory: rdf });
        const report = await validator.validate(data);

        // Ergebnis in eine Datei schreiben (für Python lesbar)
        const result = {
            conforms: report.conforms,
            results: report.results.map(result => ({
                message: result.message?.toString() || '',
                path: result.path?.toString() || '',
                focusNode: result.focusNode?.toString() || '',
                severity: result.severity?.toString() || '',
                sourceConstraintComponent: result.sourceConstraintComponent?.toString() || '',
                sourceShape: result.sourceShape?.toString() || ''
            }))
        };
        writeFileSync('validation-report.json', JSON.stringify(result, null, 2));
        console.log(JSON.stringify(result, null, 2));
        process.exit(report.conforms ? 0 : 1);
    } catch (error) {
        console.error('Error during validation:', error.message);
        process.exit(2);
    }
}

// Parameter aus der Kommandozeile lesen
const [,, dataFile, shapesFile] = process.argv;
if (!dataFile || !shapesFile) {
    console.error('Usage: node validate-shacl.js <data-file> <shapes-file>');
    process.exit(1);
}

validate(dataFile, shapesFile);