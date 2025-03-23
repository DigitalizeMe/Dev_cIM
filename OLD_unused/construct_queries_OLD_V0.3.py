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
        VALUES ?endType { occp:ConstructionAcceptance occp:CompletionOfConstruction }
    }
    OPTIONAL {
        ?endInstantEstimated a ?endType ;
                            occp:endsPhase ?phase ;
                            occp:hasEstimatedTime ?endTimeEstimated .
        FILTER NOT EXISTS { ?endInstantEstimated occp:hasActualTime ?anyActualTime . }
        VALUES ?endType { occp:ConstructionAcceptance occp:CompletionOfConstruction }
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
    FILTER NOT EXISTS { ?component ould:consistsOf ?any }  # Child-Components only
    OPTIONAL {
        ?startInstantActual a occp:ReviewStart ;
                           occp:startsCycle ?cycle ;
                           occp:hasActualTime ?startTimeActual .
        FILTER NOT EXISTS { ?startInstantActual occp:hasEstimatedTime ?anyEstimatedTime . }
    }
    OPTIONAL {
        ?startInstantEstimated a occp:ReviewStart ;
                              occp:startsCycle ?cycle ;
                              occp:hasEstimatedTime ?startTimeEstimated .
        FILTER NOT EXISTS { ?startInstantEstimated occp:hasActualTime ?anyActualTime . }
    }
    OPTIONAL {
        ?endInstantActual a ?endType ;
                         occp:endsCycle ?cycle ;
                         occp:hasActualTime ?endTimeActual .
        FILTER NOT EXISTS { ?endInstantActual occp:hasEstimatedTime ?anyEstimatedTime . }
        VALUES ?endType { occp:ReviewApproval occp:ReviewRejection }
    }
    OPTIONAL {
        ?endInstantEstimated a ?endType ;
                            occp:endsCycle ?cycle ;
                            occp:hasEstimatedTime ?endTimeEstimated .
        FILTER NOT EXISTS { ?endInstantEstimated occp:hasActualTime ?anyActualTime . }
        VALUES ?endType { occp:ReviewApproval occp:ReviewRejection }
    }
    OPTIONAL { ?cycle occp:hasCycleNumber ?existingNumber . }
    BIND(COALESCE(?existingNumber, 1) AS ?cycleNumber)
}
"""

CONSTRUCT_CYCLE_A_ACTUAL = """
CONSTRUCT {
    ?cycle occp:hasActualBeginning ?startInstantActual .
    ?cycle occp:hasActualEnd ?endInstantActual .
}
WHERE {
    ?cycle a occp:CycleA_PlanningReview .
    ?component occp:hasCycle ?cycle .
    FILTER NOT EXISTS { ?component ould:consistsOf ?any }
    OPTIONAL {
        SELECT ?cycle ?startInstantActual
        WHERE {
            ?component occp:hasCycle ?cycle .
            ?startInstantActual a occp:ReviewStart ;
                               occp:startsCycle ?cycle ;
                               occp:hasActualTime ?startTimeActual .
            FILTER NOT EXISTS { ?startInstantActual occp:hasEstimatedTime ?anyEstimatedTime . }
        }
        ORDER BY ?startTimeActual
        LIMIT 1
    }
    OPTIONAL {
        SELECT ?cycle ?endInstantActual
        WHERE {
            ?component occp:hasCycle ?cycle .
            ?endInstantActual occp:endsCycle ?cycle ;
                             occp:hasActualTime ?endTimeActual .
            FILTER NOT EXISTS { ?endInstantActual occp:hasEstimatedTime ?anyEstimatedTime . }
            ?endInstantActual a ?endType .
            VALUES ?endType { occp:ReviewApproval occp:ReviewRejection }
        }
        ORDER BY DESC(?endTimeActual)
        LIMIT 1
    }
}
"""

CONSTRUCT_CYCLE_A_ESTIMATED = """
CONSTRUCT {
    ?cycle occp:hasEstimatedBeginning ?startInstantEstimated .
    ?cycle occp:hasEstimatedEnd ?endInstantEstimated .
}
WHERE {
    ?cycle a occp:CycleA_PlanningReview .
    ?component occp:hasCycle ?cycle .
    FILTER NOT EXISTS { ?component ould:consistsOf ?any }
    OPTIONAL {
        SELECT ?cycle ?startInstantEstimated
        WHERE {
            ?component occp:hasCycle ?cycle .
            ?startInstantEstimated a occp:ReviewStart ;
                                  occp:startsCycle ?cycle ;
                                  occp:hasEstimatedTime ?startTimeEstimated .
            FILTER NOT EXISTS { ?startInstantEstimated occp:hasActualTime ?anyActualTime . }
        }
        ORDER BY ?startTimeEstimated
        LIMIT 1
    }
    OPTIONAL {
        SELECT ?cycle ?endInstantEstimated
        WHERE {
            ?component occp:hasCycle ?cycle .
            ?endInstantEstimated occp:endsCycle ?cycle ;
                                occp:hasEstimatedTime ?endTimeEstimated .
            FILTER NOT EXISTS { ?endInstantEstimated occp:hasActualTime ?anyActualTime . }
            ?endInstantEstimated a ?endType .
            VALUES ?endType { occp:ReviewApproval occp:ReviewRejection }
        }
        ORDER BY DESC(?endTimeEstimated)
        LIMIT 1
    }
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

CONSTRUCT_PARENT_PHASES = """
PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
PREFIX ould: <http://www.semanticweb.org/albrechtvaatz/ontologies/2024/OULD#>
CONSTRUCT {
    ?parentPhase occp:hasActualBeginning ?earliestActualStart .
    ?parentPhase occp:hasActualEnd ?latestActualEnd .
    ?parentPhase occp:hasEstimatedBeginning ?earliestEstimatedStart .
    ?parentPhase occp:hasEstimatedEnd ?latestEstimatedEnd .
}
WHERE {
    ?parentComponent occp:hasPhase ?parentPhase .
    ?parentComponent ould:consistsOf ?childComponent .
    ?childComponent occp:hasPhase ?childPhase .

    # Earliest Actual Beginning
    OPTIONAL {
        SELECT ?parentPhase ?earliestActualStart
        WHERE {
            ?parentComponent occp:hasPhase ?parentPhase .
            ?parentComponent ould:consistsOf ?childComponent .
            ?childComponent occp:hasPhase ?childPhase .
            ?startInstant occp:startsPhase ?childPhase ;
                          occp:hasActualTime ?startTime .
            FILTER NOT EXISTS { ?startInstant occp:hasEstimatedTime ?anyEstimatedTime . }
        }
        ORDER BY ?startTime
        LIMIT 1
    }

    # Latest Actual End
    OPTIONAL {
        SELECT ?parentPhase ?latestActualEnd
        WHERE {
            ?parentComponent occp:hasPhase ?parentPhase .
            ?parentComponent ould:consistsOf ?childComponent .
            ?childComponent occp:hasPhase ?childPhase .
            ?endInstant occp:endsPhase ?childPhase ;
                        occp:hasActualTime ?endTime .
            FILTER NOT EXISTS { ?endInstant occp:hasEstimatedTime ?anyEstimatedTime . }
            VALUES ?endType { occp:ReviewApproval occp:ReviewRejection }
            ?endInstant a ?endType .
        }
        ORDER BY DESC(?endTime)
        LIMIT 1
    }

    # Earliest Estimated Beginning
    OPTIONAL {
        SELECT ?parentPhase ?earliestEstimatedStart
        WHERE {
            ?parentComponent occp:hasPhase ?parentPhase .
            ?parentComponent ould:consistsOf ?childComponent .
            ?childComponent occp:hasPhase ?childPhase .
            ?startInstant occp:startsPhase ?childPhase ;
                          occp:hasEstimatedTime ?startTime .
            FILTER NOT EXISTS { ?startInstant occp:hasActualTime ?anyActualTime . }
        }
        ORDER BY ?startTime
        LIMIT 1
    }

    # Latest Estimated End
    OPTIONAL {
        SELECT ?parentPhase ?latestEstimatedEnd
        WHERE {
            ?parentComponent occp:hasPhase ?parentPhase .
            ?parentComponent ould:consistsOf ?childComponent .
            ?childComponent occp:hasPhase ?childPhase .
            ?endInstant occp:endsPhase ?childPhase ;
                        occp:hasEstimatedTime ?endTime .
            FILTER NOT EXISTS { ?endInstant occp:hasActualTime ?anyActualTime . }
            VALUES ?endType { occp:ReviewApproval occp:ReviewRejection }
            ?endInstant a ?endType .
        }
        ORDER BY DESC(?endTime)
        LIMIT 1
    }
}
"""

CONSTRUCT_PARENT_CYCLES = """
PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
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
    OPTIONAL {
        ?startInstantActual a occp:ReviewStart ;
                           occp:startsCycle ?cycle ;
                           occp:hasActualTime ?startTimeActual .
        FILTER NOT EXISTS { ?startInstantActual occp:hasEstimatedTime ?anyEstimatedTime . }
    }
    OPTIONAL {
        ?endInstantActual a ?endType ;
                         occp:endsCycle ?cycle ;
                         occp:hasActualTime ?endTimeActual .
        FILTER NOT EXISTS { ?endInstantActual occp:hasEstimatedTime ?anyEstimatedTime . }
        VALUES ?endType { occp:ReviewRejection occp:ReviewApproval }
    }
    OPTIONAL {
        ?startInstantEstimated a occp:ReviewStart ;
                              occp:startsCycle ?cycle ;
                              occp:hasEstimatedTime ?startTimeEstimated .
        FILTER NOT EXISTS { ?startInstantEstimated occp:hasActualTime ?anyActualTime . }
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



def generate_post_graph(pre_file, output_file):
    pre_graph = Graph().parse(pre_file, format="turtle")
    post_graph = Graph()
    # Order of CONSTRUCT-Queries is imporant!
    post_graph += pre_graph.query(CONSTRUCT_PHASE_A1).graph
    post_graph += pre_graph.query(CONSTRUCT_PHASE_A2).graph
    post_graph += pre_graph.query(CONSTRUCT_PHASE_B).graph
    post_graph += pre_graph.query(CONSTRUCT_PHASE_C).graph
    post_graph += pre_graph.query(CONSTRUCT_PHASE_D).graph
    post_graph += pre_graph.query(CONSTRUCT_PHASE_M).graph
    post_graph += pre_graph.query(CONSTRUCT_CYCLE_A).graph
    
    parent_phases_result = post_graph.query(CONSTRUCT_PARENT_PHASES)
    post_graph += parent_phases_result.graph
    post_graph += pre_graph.query(CONSTRUCT_PARENT_CYCLES).graph
    post_graph += pre_graph.query(CONSTRUCT_CYCLENUMBER).graph

    post_graph.serialize(output_file, format="turtle")
    return post_graph

if __name__ == "__main__":
    generate_post_graph()