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
PREFIX ould: <http://www.semanticweb.org/albrechtvaatz/ontologies/2024/OULD#>
CONSTRUCT {
    ?phase occp:hasActualBeginning ?startInstantActual .
    ?phase occp:hasActualEnd ?endInstantActual .
    ?phase occp:hasEstimatedBeginning ?startInstantEstimated .
    ?phase occp:hasEstimatedEnd ?endInstantEstimated .
}
WHERE {
    ?phase a occp:PhaseD_Usage .
    ?component occp:hasPhase ?phase .

    # Actual Beginning (direkt oder über Hierarchie)
    OPTIONAL {
        { ?startInstantActual a occp:UsageStart ; occp:startsPhase ?phase }
        UNION
        { ?component ould:consistsOf+ ?subComponent .
          ?subComponent occp:hasPhase ?subPhase .
          ?subPhase a occp:PhaseD_Usage .
          ?startInstantActual a occp:UsageStart ; occp:startsPhase ?subPhase }
        ?startInstantActual occp:hasActualTime ?startTimeActual .
        FILTER NOT EXISTS { ?startInstantActual occp:hasEstimatedTime ?anyEstimatedTime }
    }

    # Actual End (direkt oder über Hierarchie)
    OPTIONAL {
        { ?endInstantActual a occp:UsageEnd ; occp:endsPhase ?phase }
        UNION
        { ?component ould:consistsOf+ ?subComponent .
          ?subComponent occp:hasPhase ?subPhase .
          ?subPhase a occp:PhaseD_Usage .
          ?endInstantActual a occp:UsageEnd ; occp:endsPhase ?subPhase }
        ?endInstantActual occp:hasActualTime ?endTimeActual .
        FILTER NOT EXISTS { ?endInstantActual occp:hasEstimatedTime ?anyEstimatedTime }
    }

    # Estimated Beginning (direkt oder über Hierarchie)
    OPTIONAL {
        { ?startInstantEstimated a occp:UsageStart ; occp:startsPhase ?phase }
        UNION
        { ?component ould:consistsOf+ ?subComponent .
          ?subComponent occp:hasPhase ?subPhase .
          ?subPhase a occp:PhaseD_Usage .
          ?startInstantEstimated a occp:UsageStart ; occp:startsPhase ?subPhase }
        ?startInstantEstimated occp:hasEstimatedTime ?startTimeEstimated .
        FILTER NOT EXISTS { ?startInstantEstimated occp:hasActualTime ?anyActualTime }
    }

    # Estimated End (direkt oder über Hierarchie)
    OPTIONAL {
        { ?endInstantEstimated a occp:UsageEnd ; occp:endsPhase ?phase }
        UNION
        { ?component ould:consistsOf+ ?subComponent .
          ?subComponent occp:hasPhase ?subPhase .
          ?subPhase a occp:PhaseD_Usage .
          ?endInstantEstimated a occp:UsageEnd ; occp:endsPhase ?subPhase }
        ?endInstantEstimated occp:hasEstimatedTime ?endTimeEstimated .
        FILTER NOT EXISTS { ?endInstantEstimated occp:hasActualTime ?anyActualTime }
    }

    # Max 1 Actual Beginning/End
    FILTER NOT EXISTS {
        ?phase occp:hasActualBeginning ?otherStartActual .
        FILTER (?otherStartActual != ?startInstantActual)
    }
    FILTER NOT EXISTS {
        ?phase occp:hasActualEnd ?otherEndActual .
        FILTER (?otherEndActual != ?endInstantActual)
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

    # Zeitliche Instants
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
        VALUES ?endType { occp:ReviewApproval occp:ReviewRejection }
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
        VALUES ?endType { occp:ReviewApproval occp:ReviewRejection }
    }

    # CycleNumber aus untergeordneten Komponenten oder Standardwert 1
    OPTIONAL {
        ?component ould:consistsOf ?childComponent .
        ?childComponent occp:hasCycle ?childCycle .
        ?childCycle occp:hasCycleNumber ?childCycleNumber .
    }
    BIND(COALESCE(?childCycleNumber) AS ?cycleNumber)
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
    ?parentPhase occp:hasActualBeginning ?startInstant .
    ?parentPhase occp:hasActualEnd ?endInstant .
}
WHERE {
    ?parentComponent occp:hasPhase ?parentPhase .
    ?parentPhase a ?parentPhaseType .
    ?parentComponent ould:consistsOf ?childComponent .
    ?childComponent occp:hasPhase ?childPhase .
    ?childPhase a ?childPhaseType .
    ?childPhase occp:hasActualBeginning ?startInstant .
    ?childPhase occp:hasActualEnd ?endInstant .
    FILTER (?parentPhaseType = ?childPhaseType)
    VALUES ?parentPhaseType {
        occp:PhaseA_Planning
        occp:PhaseB_Review
        occp:PhaseC_Construction
        occp:PhaseD_Usage
        occp:PhaseM_Deconstruction
    }
}
"""

CONSTRUCT_PARENT_PHASES_ESTIMATED = """
PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
PREFIX ould: <http://www.semanticweb.org/albrechtvaatz/ontologies/2024/OULD#>
CONSTRUCT {
    ?parentPhase occp:hasEstimatedBeginning ?startInstant .
    ?parentPhase occp:hasEstimatedEnd ?endInstant .
}
WHERE {
    ?parentComponent occp:hasPhase ?parentPhase .
    ?parentPhase a ?parentPhaseType .
    ?parentComponent ould:consistsOf ?childComponent .
    ?childComponent occp:hasPhase ?childPhase .
    ?childPhase a ?childPhaseType .
    FILTER (?parentPhaseType = ?childPhaseType)
    VALUES ?parentPhaseType {
        occp:PhaseA_Planning
        occp:PhaseB_Review
        occp:PhaseC_Construction
        occp:PhaseD_Usage
        occp:PhaseM_Deconstruction
    }
    
    # Estimated Beginning
    OPTIONAL {
        ?childPhase occp:hasEstimatedBeginning ?startInstant .
        ?startInstant occp:hasEstimatedTime ?startTime .
    }
    
    # Estimated End
    OPTIONAL {
        ?childPhase occp:hasEstimatedEnd ?endInstant .
        ?endInstant occp:hasEstimatedTime ?endTime .
    }
}
"""

CONSTRUCT_PARENT_PHASES_FILTER = """
PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
CONSTRUCT {
    ?parentPhase occp:hasActualBeginning ?earliestStartInstant .
    ?parentPhase occp:hasActualEnd ?latestEndInstant .
}
WHERE {
    ?parentPhase a ?parentPhaseType .
    
    # Frühester Start
    {
        SELECT ?parentPhase (SAMPLE(?startInst) AS ?earliestStartInstant)
        WHERE {
            ?parentPhase occp:hasActualBeginning ?startInst .
            ?startInst occp:hasActualTime ?startTime .
            {
                SELECT ?parentPhase (MIN(?st) AS ?minStartTime)
                WHERE {
                    ?parentPhase occp:hasActualBeginning ?si .
                    ?si occp:hasActualTime ?st .
                }
                GROUP BY ?parentPhase
            }
            FILTER (?startTime = ?minStartTime)
        }
        GROUP BY ?parentPhase
    }
    
    # Spätestes Ende
    {
        SELECT ?parentPhase (MAX(?endTime) AS ?latestEndTime) (SAMPLE(?endInst) AS ?latestEndInstant)
        WHERE {
            ?parentPhase occp:hasActualEnd ?endInst .
            ?endInst occp:hasActualTime ?endTime .
        }
        GROUP BY ?parentPhase
        HAVING (COUNT(?endInst) > 0)
    }
}
"""

CONSTRUCT_PARENT_CYCLES_ACTUAL = """
PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
PREFIX ould: <http://www.semanticweb.org/albrechtvaatz/ontologies/2024/OULD#>
CONSTRUCT {
    ?parentCycle occp:hasActualBeginning ?startInstant .
    ?parentCycle occp:hasActualEnd ?endInstant .
}
WHERE {
    ?parentComponent occp:hasCycle ?parentCycle .
    ?parentCycle a ?parentCycleType .
    ?parentComponent ould:consistsOf ?childComponent .
    ?childComponent occp:hasCycle ?childCycle .
    ?childCycle a ?childCycleType .
    ?childCycle occp:hasActualBeginning ?startInstant .
    ?childCycle occp:hasActualEnd ?endInstant .
    FILTER (?parentCycleType = ?childCycleType)
    VALUES ?parentCycleType {
        occp:CycleA_PlanningReview
    }
}
"""

CONSTRUCT_PARENT_CYCLES_OLD = """
PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
CONSTRUCT {
    ?cycle occp:hasActualBeginning ?startInstantActual .
    ?cycle occp:hasActualEnd ?endInstantActual .
    ?cycle occp:hasEstimatedBeginning ?startInstantEstimated .
    ?cycle occp:hasEstimatedEnd ?endInstantEstimated .
    ?cycle occp:hasCycleNumber ?maxCycleNumber .
}
WHERE {
    ?cycle a occp:CycleA_PlanningReview .
    ?component occp:hasCycle ?cycle .

    # Ermittle den maximalen hasCycleNumber-Wert
    {
        SELECT ?cycle (MAX(?existingNumber) AS ?maxCycleNumber)
        WHERE {
            ?cycle a occp:CycleA_PlanningReview .
            ?component occp:hasCycle ?cycle .
            ?cycle occp:hasCycleNumber ?existingNumber .
        }
        GROUP BY ?cycle
    }

    # Bestehende OPTIONALS für Zeitstempel
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
}
"""

CONSTRUCT_FILTER_ACTUAL_BEGINNING = """
PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
PREFIX ould: <http://www.semanticweb.org/albrechtvaatz/ontologies/2024/OULD#>
CONSTRUCT {
    ?phase occp:hasActualBeginning ?earliestStartInstant .
}
WHERE {
    ?phase a occp:PhaseD_Usage .
    {
        SELECT ?phase ?earliestStartInstant
        WHERE {
            {
                SELECT ?phase ?startInstantActual ?startTimeActual
                WHERE {
                    { ?startInstantActual a occp:UsageStart ; occp:startsPhase ?phase }
                    UNION
                    { ?component occp:hasPhase ?phase .
                      ?component ould:consistsOf ?subComponent .
                      ?subComponent occp:hasPhase ?subPhase .
                      ?subPhase a occp:PhaseD_Usage .
                      ?startInstantActual a occp:UsageStart ; occp:startsPhase ?subPhase }
                    ?startInstantActual occp:hasActualTime ?startTimeActual .
                }
                ORDER BY ?startTimeActual
                LIMIT 1
            }
            BIND (?startInstantActual AS ?earliestStartInstant)
        }
        GROUP BY ?phase ?earliestStartInstant
    }
}
"""

CONSTRUCT_FILTER_ACTUAL_END = """
PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
CONSTRUCT {
    ?phase occp:hasActualBeginning ?startInstantActual .
    ?phase occp:hasActualEnd ?latestEndInstant .
    ?phase occp:hasEstimatedBeginning ?startInstantEstimated .
    ?phase occp:hasEstimatedEnd ?endInstantEstimated .
}
WHERE {
    # Bestehende Zuordnungen übernehmen
    ?phase occp:hasActualBeginning ?startInstantActual .
    ?phase occp:hasEstimatedBeginning ?startInstantEstimated .
    ?phase occp:hasEstimatedEnd ?endInstantEstimated .

    # Spätestes Actual End auswählen
    {
        SELECT ?phase ?latestEndInstant
        WHERE {
            ?phase occp:hasActualEnd ?endInstantActual .
            ?endInstantActual occp:hasActualTime ?endTimeActual .
            {
                SELECT ?phase (MAX(?et) AS ?maxEndTime)
                WHERE {
                    ?phase occp:hasActualEnd ?ei .
                    ?ei occp:hasActualTime ?et .
                }
                GROUP BY ?phase
            }
            FILTER (?endTimeActual = ?maxEndTime)
        }
        GROUP BY ?phase ?latestEndInstant
    }
}
"""

from rdflib import Graph

def generate_post_graph(pre_file, output_file):
    pre_graph = Graph().parse(pre_file, format="turtle")
    
    post_graph_1 = Graph()
    post_graph_1 += pre_graph.query(CONSTRUCT_PHASE_A1).graph
    post_graph_1 += pre_graph.query(CONSTRUCT_PHASE_A2).graph
    post_graph_1 += pre_graph.query(CONSTRUCT_PHASE_B).graph
    post_graph_1 += pre_graph.query(CONSTRUCT_PHASE_C).graph
    post_graph_1 += pre_graph.query(CONSTRUCT_PHASE_D).graph

    post_graph_1 += pre_graph.query(CONSTRUCT_PHASE_M).graph
    post_graph_1 += pre_graph.query(CONSTRUCT_CYCLE_A).graph

    post_graph_2 = pre_graph + post_graph_1
    post_graph_2 += post_graph_2.query(CONSTRUCT_PARENT_PHASES).graph
    post_graph_2 += post_graph_2.query(CONSTRUCT_PARENT_CYCLES_ACTUAL).graph


    post_graph_3 = pre_graph + post_graph_2 + post_graph_1
    post_graph_3 += post_graph_3.query(CONSTRUCT_PARENT_PHASES).graph
    post_graph_2 += post_graph_2.query(CONSTRUCT_PARENT_CYCLES_ACTUAL).graph


    post_graph_3 = post_graph_3.query(CONSTRUCT_PARENT_PHASES_FILTER).graph
    post_graph_3 += post_graph_3.query(CONSTRUCT_PARENT_PHASES_ESTIMATED).graph
    post_graph_3 += post_graph_3.query(CONSTRUCT_FILTER_ACTUAL_BEGINNING).graph


    post_graph_final = post_graph_3 + post_graph_2 + post_graph_1 + pre_graph

    post_graph_final.serialize(output_file, format="turtle")
    return post_graph_final