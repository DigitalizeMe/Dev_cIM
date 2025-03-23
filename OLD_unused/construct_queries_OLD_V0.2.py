# construct_queries.py
from rdflib import Graph

CONSTRUCT_PHASE_A1 = """
PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
CONSTRUCT {
    ?phase occp:hasActualBeginning ?startInstantActual .
    ?phase occp:hasActualEnd ?endInstantActual .
    }
    WHERE {
        ?phase a occp:PhaseA_Planning .
        ?component occp:hasPhase ?phase .
        OPTIONAL {
            ?startInstantActual a occp:BeginningOfPlanning ;
                                occp:startsPhase ?phase ;
                                occp:hasActualTime ?startTimeActual .
        }
        OPTIONAL {
            ?endInstantActual a occp:ReviewApproval ;
                            occp:endsPhase ?phase ;
                            occp:hasActualTime ?endTimeActual .
        }
    }
"""
    
CONSTRUCT_PHASE_A2 = """
PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
CONSTRUCT {
        ?phase occp:hasEstimatedBeginning ?startInstantEstimated .
        ?phase occp:hasEstimatedEnd ?endInstantEstimated .
    }
    WHERE {
        ?phase a occp:PhaseA_Planning .
        ?component occp:hasPhase ?phase .
        OPTIONAL {
            ?startInstantEstimated a occp:BeginningOfPlanning ;
                                occp:startsPhase ?phase ;
                                occp:hasEstimatedTime ?startTimeEstimated .
        }
        OPTIONAL {
            ?endInstantEstimated a occp:ReviewApproval ;
                                occp:endsPhase ?phase ;
                                occp:hasEstimatedTime ?endTimeEstimated .
        }
    }
"""

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
        VALUES ?startType { occp:ReviewStart }
    }
    OPTIONAL {
        ?startInstantEstimated a ?startType ;
                              occp:startsPhase ?phase ;
                              occp:hasEstimatedTime ?startTimeEstimated .
        FILTER NOT EXISTS { ?startInstantEstimated occp:hasActualTime ?anyActualTime . }
        VALUES ?startType { occp:ReviewStart }
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

CONSTRUCT_PHASE_C = """
PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
CONSTRUCT {
    ?phase occp:hasActualBeginning ?startInstantActual .
    ?phase occp:hasActualEnd ?endInstantActual .
    ?phase occp:hasEstimatedBeginning ?startInstantEstimated .
    ?phase occp:hasEstimatedEnd ?endInstantEstimated .
}
WHERE {
    ?phase a occp:PhaseC_Construction .
    ?component occp:hasPhase ?phase .
    OPTIONAL {
        ?startInstantActual a ?startType ;
                           occp:startsPhase ?phase ;
                           occp:hasActualTime ?startTimeActual .
        FILTER NOT EXISTS { ?startInstantActual occp:hasEstimatedTime ?anyEstimatedTime . }
        VALUES ?startType { occp:ConstructionStart }
    }
    OPTIONAL {
        ?startInstantEstimated a ?startType ;
                              occp:startsPhase ?phase ;
                              occp:hasEstimatedTime ?startTimeEstimated .
        FILTER NOT EXISTS { ?startInstantEstimated occp:hasActualTime ?anyActualTime . }
        VALUES ?startType { occp:ConstructionStart }
    }
    OPTIONAL {
        ?endInstantActual a ?endType ;
                         occp:endsPhase ?phase ;
                         occp:hasActualTime ?endTimeActual .
        FILTER NOT EXISTS { ?endInstantActual occp:hasEstimatedTime ?anyEstimatedTime . }
        VALUES ?endType { occp:ConstructionAcceptance }
    }
    OPTIONAL {
        ?endInstantEstimated a ?endType ;
                            occp:endsPhase ?phase ;
                            occp:hasEstimatedTime ?endTimeEstimated .
        FILTER NOT EXISTS { ?endInstantEstimated occp:hasActualTime ?anyActualTime . }
        VALUES ?endType { occp:ConstructionAcceptance }
    }
}
"""

CONSTRUCT_PHASE_D = """
PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
CONSTRUCT {
    ?phase occp:hasActualBeginning ?startInstantActual .
    ?phase occp:hasActualEnd ?endInstantActual .
    ?phase occp:hasEstimatedBeginning ?startInstantEstimated .
    ?phase occp:hasEstimatedEnd ?endInstantEstimated .
}
WHERE {
    ?phase a occp:PhaseD_Usage .
    ?component occp:hasPhase ?phase .
    OPTIONAL {
        ?startInstantActual a ?startType ;
                           occp:startsPhase ?phase ;
                           occp:hasActualTime ?startTimeActual .
        FILTER NOT EXISTS { ?startInstantActual occp:hasEstimatedTime ?anyEstimatedTime . }
        VALUES ?startType { occp:UsageStart }
    }
    OPTIONAL {
        ?startInstantEstimated a ?startType ;
                              occp:startsPhase ?phase ;
                              occp:hasEstimatedTime ?startTimeEstimated .
        FILTER NOT EXISTS { ?startInstantEstimated occp:hasActualTime ?anyActualTime . }
        VALUES ?startType { occp:UsageStart  }
    }
      OPTIONAL {
        ?startInstantActual a ?startType ;
                           occp:startsPhase ?phase ;
                           occp:hasActualTime ?startTimeActual .
        FILTER NOT EXISTS { ?startInstantActual occp:hasEstimatedTime ?anyEstimatedTime . }
        VALUES ?startType { occp:UsageChange }
    }
    OPTIONAL {
        ?startInstantEstimated a ?startType ;
                              occp:startsPhase ?phase ;
                              occp:hasEstimatedTime ?startTimeEstimated .
        FILTER NOT EXISTS { ?startInstantEstimated occp:hasActualTime ?anyActualTime . }
        VALUES ?startType { occp:UsageChange  }
    }
    OPTIONAL {
        ?endInstantActual a ?endType ;
                         occp:endsPhase ?phase ;
                         occp:hasActualTime ?endTimeActual .
        FILTER NOT EXISTS { ?endInstantActual occp:hasEstimatedTime ?anyEstimatedTime . }
        VALUES ?endType { occp:UsageEnd }
    }
    OPTIONAL {
        ?endInstantEstimated a ?endType ;
                            occp:endsPhase ?phase ;
                            occp:hasEstimatedTime ?endTimeEstimated .
        FILTER NOT EXISTS { ?endInstantEstimated occp:hasActualTime ?anyActualTime . }
        VALUES ?endType { occp:UsageEnd }
    }
    OPTIONAL {
        ?endInstantActual a ?endType ;
                         occp:endsPhase ?phase ;
                         occp:hasActualTime ?endTimeActual .
        FILTER NOT EXISTS { ?endInstantActual occp:hasEstimatedTime ?anyEstimatedTime . }
        VALUES ?endType { occp:UsageChange }
    }
    OPTIONAL {
        ?endInstantEstimated a ?endType ;
                            occp:endsPhase ?phase ;
                            occp:hasEstimatedTime ?endTimeEstimated .
        FILTER NOT EXISTS { ?endInstantEstimated occp:hasActualTime ?anyActualTime . }
        VALUES ?endType { occp:UsageChange }
    }
}
"""

CONSTRUCT_PHASE_M = """
PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
CONSTRUCT {
    ?phase occp:hasActualBeginning ?startInstantActual .
    ?phase occp:hasActualEnd ?endInstantActual .
    ?phase occp:hasEstimatedBeginning ?startInstantEstimated .
    ?phase occp:hasEstimatedEnd ?endInstantEstimated .
}
WHERE {
    ?phase a occp:PhaseM_Deconstruction .
    ?component occp:hasPhase ?phase .
    OPTIONAL {
        ?startInstantActual a ?startType ;
                           occp:startsPhase ?phase ;
                           occp:hasActualTime ?startTimeActual .
        FILTER NOT EXISTS { ?startInstantActual occp:hasEstimatedTime ?anyEstimatedTime . }
        VALUES ?startType { occp:DeconstructionStart }
    }
    OPTIONAL {
        ?startInstantEstimated a ?startType ;
                              occp:startsPhase ?phase ;
                              occp:hasEstimatedTime ?startTimeEstimated .
        FILTER NOT EXISTS { ?startInstantEstimated occp:hasActualTime ?anyActualTime . }
        VALUES ?startType { occp:DeconstructionStart }
    }
    OPTIONAL {
        ?endInstantActual a ?endType ;
                         occp:endsPhase ?phase ;
                         occp:hasActualTime ?endTimeActual .
        FILTER NOT EXISTS { ?endInstantActual occp:hasEstimatedTime ?anyEstimatedTime . }
        VALUES ?endType { occp:DeconstructionCompletion }
    }
    OPTIONAL {
        ?endInstantEstimated a ?endType ;
                            occp:endsPhase ?phase ;
                            occp:hasEstimatedTime ?endTimeEstimated .
        FILTER NOT EXISTS { ?endInstantEstimated occp:hasActualTime ?anyActualTime . }
        VALUES ?endType { occp:DeconstructionCompletion }
    }
}
"""

CONSTRUCT_CYCLE_A = """
PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
PREFIX ould: <http://www.semanticweb.org/albrechtvaatz/ontologies/2024/OULD#>
CONSTRUCT {
    ?cycle occp:hasActualBeginning ?startInstantActual .
    ?cycle occp:hasActualEnd ?endInstantActual .
    ?cycle occp:hasEstimatedBeginning ?startInstantEstimated .
    ?cycle occp:hasEstimatedEnd ?endInstantEstimated .
    ?cycle occp:hasCycleNumber ?cycleNumber .
}
WHERE {
    ?cycle a occp:CycleA_PlanningReview .
    ?component occp:hasCycle ?cycle .
    FILTER NOT EXISTS { ?component ould:consistsOf ?any }  # Nur Blattkomponenten
    OPTIONAL {
        ?startInstantActual a occp:SubmissionToReview ;
                           occp:startsCycle ?cycle ;
                           occp:hasActualTime ?startTimeActual .
        FILTER NOT EXISTS { ?startInstantActual occp:hasEstimatedTime ?anyEstimatedTime . }
    }
    OPTIONAL {
        ?startInstantEstimated a occp:SubmissionToReview ;
                              occp:startsCycle ?cycle ;
                              occp:hasEstimatedTime ?startTimeEstimated .
        FILTER NOT EXISTS { ?startInstantEstimated occp:hasActualTime ?anyActualTime . }
    }
    OPTIONAL {
        ?endInstantActual a ?endType ;
                         occp:endsCycle ?cycle ;
                         occp:hasActualTime ?endTimeActual .
        FILTER NOT EXISTS { ?endInstantActual occp:hasEstimatedTime ?anyEstimatedTime . }
        VALUES ?endType { occp:ReviewRejection occp:ReviewApproval }
    }
    OPTIONAL {
        ?endInstantEstimated a ?endType ;
                            occp:endsCycle ?cycle ;
                            occp:hasEstimatedTime ?endTimeEstimated .
        FILTER NOT EXISTS { ?endInstantEstimated occp:hasActualTime ?anyActualTime . }
        VALUES ?endType { occp:ReviewRejection occp:ReviewApproval }
    }
    OPTIONAL { ?cycle occp:hasCycleNumber ?existingNumber . }
    BIND(COALESCE(?existingNumber, 1) AS ?cycleNumber)
}
"""

CONSTRUCT_CYCLENUMBER = """
PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
PREFIX ould: <http://www.semanticweb.org/albrechtvaatz/ontologies/2024/OULD#>
CONSTRUCT {
    ?parentCycle occp:hasCycleNumber ?parentCycleNumber .
}
WHERE {
    {
        SELECT ?parentCycle (COUNT(DISTINCT ?childCycle) AS ?parentCycleNumber)
        WHERE {
            ?parentComponent occp:hasCycle ?parentCycle .
            ?parentComponent ould:consistsOf ?childComponent .
            ?childComponent occp:hasCycle ?childCycle .
            ?childCycle occp:hasCycleNumber ?childCycleNumber .
        }
        GROUP BY ?parentCycle
    }
}
"""

CONSTRUCT_COMPONENTS = """
PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
CONSTRUCT {
    ?phase occp:hasActualBeginning ?startInstantActual .
    ?phase occp:hasActualEnd ?endInstantActual .
    ?phase occp:hasEstimatedBeginning ?startInstantEstimated .
    ?phase occp:hasEstimatedEnd ?endInstantEstimated .
    ?cycle occp:hasActualBeginning ?startInstantActual .
    ?cycle occp:hasActualEnd ?endInstantActual .
    ?cycle occp:hasEstimatedBeginning ?startInstantEstimated .
    ?cycle occp:hasEstimatedEnd ?endInstantEstimated .
    ?cycle occp:hasCycleNumber ?existingNumber .
}
WHERE {
    ?component occp:hasPhase ?phase .
    OPTIONAL {
        ?startInstantActual a ?startType ;
                            occp:startsPhase ?phase ;
                            occp:hasActualTime ?startTimeActual .
        FILTER NOT EXISTS { ?startInstantActual occp:hasEstimatedTime ?anyEstimatedTime . }
        VALUES ?startType { occp:BeginningOfPlanning occp:SubmissionToReview occp:BeginningOfConstruction }
    }
    OPTIONAL {
        ?startInstantEstimated a ?startType ;
                               occp:startsPhase ?phase ;
                               occp:hasEstimatedTime ?startTimeEstimated .
        FILTER NOT EXISTS { ?startInstantEstimated occp:hasActualTime ?anyActualTime . }
        VALUES ?startType { occp:BeginningOfPlanning occp:SubmissionToReview occp:BeginningOfConstruction }
    }
    OPTIONAL {
        ?endInstantActual a ?endType ;
                          occp:endsPhase ?phase ;
                          occp:hasActualTime ?endTimeActual .
        FILTER NOT EXISTS { ?endInstantActual occp:hasEstimatedTime ?anyEstimatedTime . }
        VALUES ?endType { occp:ReviewApproval occp:ReviewRejection occp:CompletionOfConstruction }
    }
    OPTIONAL {
        ?endInstantEstimated a ?endType ;
                             occp:endsPhase ?phase ;
                             occp:hasEstimatedTime ?endTimeEstimated .
        FILTER NOT EXISTS { ?endInstantEstimated occp:hasActualTime ?anyActualTime . }
        VALUES ?endType { occp:ReviewApproval occp:ReviewRejection occp:CompletionOfConstruction }
    }
    OPTIONAL {
        ?startInstantActual occp:startsCycle ?cycle .
        ?component occp:hasCycle ?cycle .
        ?endInstantActual occp:endsCycle ?cycle .
    }
    OPTIONAL {
        ?startInstantEstimated occp:startsCycle ?cycle .
        ?component occp:hasCycle ?cycle .
        ?endInstantEstimated occp:endsCycle ?cycle .
    }
    OPTIONAL { ?cycle occp:hasCycleNumber ?existingNumber . }
}
"""

def generate_post_graph(pre_file, output_file):
    pre_graph = Graph().parse(pre_file, format="turtle")
    post_graph = Graph()
    
    post_graph += pre_graph.query(CONSTRUCT_PHASE_A1).graph
    post_graph += pre_graph.query(CONSTRUCT_PHASE_A2).graph
    post_graph += pre_graph.query(CONSTRUCT_PHASE_B).graph
    post_graph += pre_graph.query(CONSTRUCT_PHASE_C).graph
    post_graph += pre_graph.query(CONSTRUCT_PHASE_D).graph
    post_graph += pre_graph.query(CONSTRUCT_PHASE_M).graph
    post_graph += pre_graph.query(CONSTRUCT_CYCLE_A).graph
    post_graph += pre_graph.query(CONSTRUCT_CYCLENUMBER).graph

    post_graph.serialize(output_file, format="turtle")
    return post_graph

if __name__ == "__main__":
    generate_post_graph()