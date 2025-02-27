import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.*;
import org.semanticweb.owlapi.reasoner.InferenceType;
import org.semanticweb.owlapi.reasoner.OWLReasoner;
import org.semanticweb.owlapi.reasoner.OWLReasonerFactory;
import com.clarkparsia.pellet.owlapiv3.PelletReasonerFactory;

import java.io.File;

public class PelletValidator {
    public static void main(String[] args) {
        try {
            // Lade die OWL-TBox und ABox
            File tboxFile = new File("OCCP_V0.26.ttl");
            File aboxFile = new File("OCCP_Phase_A_VALID_1.ttl");

            // OWL-Manager und Ontologie-Factory erstellen
            OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
            OWLOntology tbox = manager.loadOntologyFromOntologyDocument(tboxFile);
            OWLOntology abox = manager.loadOntologyFromOntologyDocument(aboxFile);

            // Kombiniere TBox und ABox in eine Gesamt-Ontologie
            manager.addAxioms(tbox, abox.getAxioms());

            // Pellet-Reasoner initialisieren
            OWLReasonerFactory reasonerFactory = new PelletReasonerFactory();
            OWLReasoner reasoner = reasonerFactory.createReasoner(tbox);

            // Inferenz aktivieren
            reasoner.precomputeInferences(InferenceType.CLASS_HIERARCHY);
            reasoner.precomputeInferences(InferenceType.OBJECT_PROPERTY_HIERARCHY);
            
            // Konsistenzprüfung der Ontologie
            System.out.println("🔍 Prüfe Konsistenz mit Pellet...");
            if (reasoner.isConsistent()) {
                System.out.println("✅ Die Ontologie ist konsistent!");
            } else {
                System.out.println("⚠️ Achtung: Die Ontologie ist inkonsistent!");
            }

        } catch (OWLOntologyCreationException e) {
            e.printStackTrace();
        }
    }
}
