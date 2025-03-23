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
        VALUES ?startType { occp:SubmissionToReview }
    }
    OPTIONAL {
        ?startInstantEstimated a ?startType ;
                              occp:startsCycle ?cycle ;
                              occp:hasEstimatedTime ?startTimeEstimated .
        FILTER NOT EXISTS { ?startInstantEstimated occp:hasActualTime ?anyActualTime . }
        VALUES ?startType { occp:SubmissionToReview}
    }
    OPTIONAL {
        ?endInstantActual a ?endType ;
                         occp:endsCycle ?cycle ;
                         occp:hasActualTime ?endTimeActual .
        FILTER NOT EXISTS { ?endInstantActual occp:hasEstimatedTime ?anyEstimatedTime . }
        VALUES ?endType { occp:ReviewRejection }
    }
    OPTIONAL {
        ?endInstantEstimated a ?endType ;
                            occp:endsCycle ?cycle ;
                            occp:hasEstimatedTime ?endTimeEstimated .
        FILTER NOT EXISTS { ?endInstantEstimated occp:hasActualTime ?anyActualTime . }
        VALUES ?endType { occp:ReviewRejection }
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
    OPTIONAL { ?cycle occp:hasCycleNumber ?existingNumber . }
    BIND(COALESCE(?existingNumber, 1) AS ?cycleNumber)
}
"""

CONSTRUCT_CYCLENUMBER = """
    PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
    CONSTRUCT {
        ?phase occp:hasActualBeginning ?startInstant .
        ?phase occp:hasActualEnd ?endInstant .
        ?phase occp:hasEstimatedBeginning ?startInstant .
        ?phase occp:hasEstimatedEnd ?endInstant .
        ?cycle occp:hasActualBeginning ?startInstant .
        ?cycle occp:hasActualEnd ?endInstant .
        ?cycle occp:hasEstimatedBeginning ?startInstant .
        ?cycle occp:hasEstimatedEnd ?endInstant .
        ?cycle occp:isInPhase ?phase .
        ?cycle occp:hasCycleNumber ?cycleNumber .
    }
    WHERE {
        # Start instants
        { ?startInstant a ?startType ;
            occp:startsPhase ?phase ;
            occp:hasActualTime ?startTime .
          VALUES ?startType { occp:BeginningOfPlanning occp:SubmissionToReview occp:BeginningOfConstruction }
        }
        UNION
        { ?startInstant a ?startType ;
            occp:startsPhase ?phase ;
            occp:hasEstimatedTime ?startTime .
          VALUES ?startType { occp:BeginningOfPlanning occp:SubmissionToReview occp:BeginningOfConstruction }
        }
        ?component occp:hasPhase ?phase .
        # End instants
        { ?endInstant a ?endType ;
            occp:endsPhase ?phase ;
            occp:hasActualTime ?endTime .
          VALUES ?endType { occp:ReviewApproval occp:ReviewRejection occp:CompletionOfConstruction }
        }
        UNION
        { ?endInstant a ?endType ;
            occp:endsPhase ?phase ;
            occp:hasEstimatedTime ?endTime .
          VALUES ?endType { occp:ReviewApproval occp:ReviewRejection occp:CompletionOfConstruction }
        }
        # Optional cycles
        OPTIONAL {
            ?startInstant occp:startsCycle ?cycle .
            ?component occp:hasCycle ?cycle .
            ?endInstant occp:endsCycle ?cycle .
            OPTIONAL { ?cycle occp:hasCycleNumber ?existingNumber . }
            BIND(COALESCE(?existingNumber, 1) AS ?cycleNumber)
        }
    }
"""

CONSTRUCT_COMPONENTS = """
    PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
    CONSTRUCT {
        ?phase occp:hasActualBeginning ?startInstant .
        ?phase occp:hasActualEnd ?endInstant .
        ?phase occp:hasEstimatedBeginning ?startInstant .
        ?phase occp:hasEstimatedEnd ?endInstant .
        ?cycle occp:hasActualBeginning ?startInstant .
        ?cycle occp:hasActualEnd ?endInstant .
        ?cycle occp:hasEstimatedBeginning ?startInstant .
        ?cycle occp:hasEstimatedEnd ?endInstant .
        ?cycle occp:isInPhase ?phase .
        ?cycle occp:hasCycleNumber ?cycleNumber .
    }
    WHERE {
        # Start instants
        { ?startInstant a ?startType ;
            occp:startsPhase ?phase ;
            occp:hasActualTime ?startTime .
          VALUES ?startType { occp:BeginningOfPlanning occp:SubmissionToReview occp:BeginningOfConstruction }
        }
        UNION
        { ?startInstant a ?startType ;
            occp:startsPhase ?phase ;
            occp:hasEstimatedTime ?startTime .
          VALUES ?startType { occp:BeginningOfPlanning occp:SubmissionToReview occp:BeginningOfConstruction }
        }
        ?component occp:hasPhase ?phase .
        # End instants
        { ?endInstant a ?endType ;
            occp:endsPhase ?phase ;
            occp:hasActualTime ?endTime .
          VALUES ?endType { occp:ReviewApproval occp:ReviewRejection occp:CompletionOfConstruction }
        }
        UNION
        { ?endInstant a ?endType ;
            occp:endsPhase ?phase ;
            occp:hasEstimatedTime ?endTime .
          VALUES ?endType { occp:ReviewApproval occp:ReviewRejection occp:CompletionOfConstruction }
        }
        # Optional cycles
        OPTIONAL {
            ?startInstant occp:startsCycle ?cycle .
            ?component occp:hasCycle ?cycle .
            ?endInstant occp:endsCycle ?cycle .
            OPTIONAL { ?cycle occp:hasCycleNumber ?existingNumber . }
        }
    }
"""

def generate_post_graph(pre_file, output_file):
    """
    Führt phasenspezifische CONSTRUCT-Abfragen aus und kombiniert die Ergebnisse.
    """
    pre_graph = Graph().parse(pre_file, format="turtle")
    post_graph = Graph()
    
    # Phase A1
    post_graph += pre_graph.query(CONSTRUCT_PHASE_A1).graph

    # Phase A2
    post_graph += pre_graph.query(CONSTRUCT_PHASE_A2).graph
    
    # Phase B
    post_graph += pre_graph.query(CONSTRUCT_PHASE_B).graph

    # Phase C
    post_graph += pre_graph.query(CONSTRUCT_PHASE_C).graph

    # Phase D
    post_graph += pre_graph.query(CONSTRUCT_PHASE_D).graph

    # Phase M
    post_graph += pre_graph.query(CONSTRUCT_PHASE_M).graph
    
    # Cycle A
    post_graph += pre_graph.query(CONSTRUCT_CYCLE_A).graph
    print("Nach CONSTRUCT_CYCLE_A:\n", post_graph.serialize(format="turtle"))
    
    # Cycle Number
    post_graph += pre_graph.query(CONSTRUCT_CYCLENUMBER).graph
    print("Nach CONSTRUCT_CYCLENUMBER:\n", post_graph.serialize(format="turtle"))
    
    # Components
    post_graph += pre_graph.query(CONSTRUCT_COMPONENTS).graph
    print("Nach CONSTRUCT_COMPONENTS:\n", post_graph.serialize(format="turtle"))

    # Save
    post_graph.serialize(output_file, format="turtle")
    return post_graph

if __name__ == "__main__":
    generate_post_graph()