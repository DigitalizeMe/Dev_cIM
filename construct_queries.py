# construct_queries.py
from rdflib import Graph

# Abfrage für Phase A
CONSTRUCT_PHASE_A = """
PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
CONSTRUCT {
    ?phase occp:hasActualBeginning ?startInstantActual .
    ?phase occp:hasActualEnd ?endInstantActual .
    ?phase occp:hasEstimatedBeginning ?startInstantEstimated .
    ?phase occp:hasEstimatedEnd ?endInstantEstimated .
}
WHERE {
    ?phase a occp:PhaseA_Planning .
    ?component occp:hasPhase ?phase .
    OPTIONAL {
        ?startInstantActual a ?startType ;
                           occp:startsPhase ?phase ;
                           occp:hasActualTime ?startTimeActual .
        FILTER NOT EXISTS { ?startInstantActual occp:hasEstimatedTime ?anyEstimatedTime . }
        VALUES ?startType { occp:BeginningOfPlanning occp:SubmissionToReview }
    }
    OPTIONAL {
        ?startInstantEstimated a ?startType ;
                              occp:startsPhase ?phase ;
                              occp:hasEstimatedTime ?startTimeEstimated .
        FILTER NOT EXISTS { ?startInstantEstimated occp:hasActualTime ?anyActualTime . }
        VALUES ?startType { occp:BeginningOfPlanning occp:SubmissionToReview }
    }
    OPTIONAL {
        ?endInstantActual a ?endType ;
                         occp:endsPhase ?phase ;
                         occp:hasActualTime ?endTimeActual .
        FILTER NOT EXISTS { ?endInstantActual occp:hasEstimatedTime ?anyEstimatedTime . }
        VALUES ?endType { occp:ReviewApproval occp:CompletionOfPlanning }
    }
    OPTIONAL {
        ?endInstantEstimated a ?endType ;
                            occp:endsPhase ?phase ;
                            occp:hasEstimatedTime ?endTimeEstimated .
        FILTER NOT EXISTS { ?endInstantEstimated occp:hasActualTime ?anyActualTime . }
        VALUES ?endType { occp:ReviewApproval occp:CompletionOfPlanning }
    }
}
"""

# Abfrage für Phase B
CONSTRUCT_PHASE_B = """
PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
CONSTRUCT {
    ?phase occp:hasActualBeginning ?startInstantActual .
    ?phase occp:hasActualEnd ?endInstantActual .
    ?phase occp:hasEstimatedBeginning ?startInstantEstimated .
    ?phase occp:hasEstimatedEnd ?endInstantEstimated .
}
WHERE {
    ?phase a occp:PhaseB_Review .
    ?component occp:hasPhase ?phase .
    OPTIONAL {
        ?startInstantActual a ?startType ;
                           occp:startsPhase ?phase ;
                           occp:hasActualTime ?startTimeActual .
        FILTER NOT EXISTS { ?startInstantActual occp:hasEstimatedTime ?anyEstimatedTime . }
        VALUES ?startType { occp:SubmissionToReview }
    }
    OPTIONAL {
        ?startInstantEstimated a ?startType ;
                              occp:startsPhase ?phase ;
                              occp:hasEstimatedTime ?startTimeEstimated .
        FILTER NOT EXISTS { ?startInstantEstimated occp:hasActualTime ?anyActualTime . }
        VALUES ?startType { occp:SubmissionToReview }
    }
    OPTIONAL {
        ?endInstantActual a ?endType ;
                         occp:endsPhase ?phase ;
                         occp:hasActualTime ?endTimeActual .
        FILTER NOT EXISTS { ?endInstantActual occp:hasEstimatedTime ?anyEstimatedTime . }
        VALUES ?endType { occp:ReviewApproval }
    }
    OPTIONAL {
        ?endInstantEstimated a ?endType ;
                            occp:endsPhase ?phase ;
                            occp:hasEstimatedTime ?endTimeEstimated .
        FILTER NOT EXISTS { ?endInstantEstimated occp:hasActualTime ?anyActualTime . }
        VALUES ?endType { occp:ReviewApproval }
    }
}
"""

# Abfrage für Cycle A
CONSTRUCT_CYCLE_A = """
PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
CONSTRUCT {
    ?cycle occp:hasActualBeginning ?startInstantActual .
    ?cycle occp:hasActualEnd ?endInstantActual .
    ?cycle occp:hasEstimatedBeginning ?startInstantEstimated .
    ?cycle occp:hasEstimatedEnd ?endInstantEstimated .
    ?cycle occp:isInPhase ?phase .
    ?cycle occp:hasCycleNumber ?cycleNumber .
}
WHERE {
    ?cycle a occp:CycleA_PlanningReview .
    ?component occp:hasCycle ?cycle .
    OPTIONAL {
        ?startInstantActual a ?startType ;
                           occp:startsCycle ?cycle ;
                           occp:hasActualTime ?startTimeActual .
        FILTER NOT EXISTS { ?startInstantActual occp:hasEstimatedTime ?anyEstimatedTime . }
        VALUES ?startType { occp:BeginningOfPlanning }
    }
    OPTIONAL {
        ?startInstantEstimated a ?startType ;
                              occp:startsCycle ?cycle ;
                              occp:hasEstimatedTime ?startTimeEstimated .
        FILTER NOT EXISTS { ?startInstantEstimated occp:hasActualTime ?anyActualTime . }
        VALUES ?startType { occp:BeginningOfPlanning }
    }
    OPTIONAL {
        ?endInstantActual a ?endType ;
                         occp:endsCycle ?cycle ;
                         occp:hasActualTime ?endTimeActual .
        FILTER NOT EXISTS { ?endInstantActual occp:hasEstimatedTime ?anyEstimatedTime . }
        VALUES ?endType { occp:ReviewApproval }
    }
    OPTIONAL {
        ?endInstantEstimated a ?endType ;
                            occp:endsCycle ?cycle ;
                            occp:hasEstimatedTime ?endTimeEstimated .
        FILTER NOT EXISTS { ?endInstantEstimated occp:hasActualTime ?anyActualTime . }
        VALUES ?endType { occp:ReviewApproval }
    }
    OPTIONAL { ?cycle occp:isInPhase ?phase . }
    OPTIONAL { ?cycle occp:hasCycleNumber ?existingNumber . }
    BIND(COALESCE(?existingNumber, 1) AS ?cycleNumber)
}
"""

def generate_post_graph(pre_file="OCCP_Pre_1B.ttl", output_file="OCCP_Post_1B_inferred.ttl"):
    """
    Führt phasenspezifische CONSTRUCT-Abfragen aus und kombiniert die Ergebnisse.
    """
    pre_graph = Graph().parse(pre_file, format="turtle")
    post_graph = Graph()
    
    # Phase A
    post_graph += pre_graph.query(CONSTRUCT_PHASE_A).graph
    
    # Phase B
    post_graph += pre_graph.query(CONSTRUCT_PHASE_B).graph
    
    # Cycle A
    post_graph += pre_graph.query(CONSTRUCT_CYCLE_A).graph
    
    # Speichern
    post_graph.serialize(output_file, format="turtle")
    return post_graph

if __name__ == "__main__":
    generate_post_graph()