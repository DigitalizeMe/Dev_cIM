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
PREFIX ex: <http://www.example.de/example#>
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

    # Sicherstellen, dass Parent- und Child-Phasen denselben Typ haben
    FILTER (?parentPhaseType = ?childPhaseType)
    
    # Alle Phasen-Typen explizit auflisten
    VALUES ?parentPhaseType {
        occp:PhaseA_Planning
        occp:PhaseB_Review
        occp:PhaseC_Construction
        occp:PhaseD_Usage
        occp:PhaseM_Deconstruction
    }
}
"""

CONSTRUCT_PARENT_PHASES_A = """
PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
PREFIX ould: <http://www.semanticweb.org/albrechtvaatz/ontologies/2024/OULD#>
CONSTRUCT {
    ?parentPhase occp:hasActualBeginning ?earliestActualStart .
    ?parentPhase occp:hasActualEnd ?latestActualEnd .
}
WHERE {
    ?parentComponent occp:hasPhase ?parentPhase .
    ?parentPhase a occp:PhaseA_Planning .  # Nur Phase A für Parent
    ?parentComponent ould:consistsOf ?childComponent .
    ?childComponent occp:hasPhase ?childPhase .
    ?childPhase a occp:PhaseA_Planning .  # Nur Phase A für Child-Phasen

    # Frühester Actual Beginning
    OPTIONAL {
        SELECT ?parentPhase ?earliestActualStart
        WHERE {
            ?parentComponent occp:hasPhase ?parentPhase .
            ?parentPhase a occp:PhaseA_Planning .
            ?parentComponent ould:consistsOf ?childComponent .
            ?childComponent occp:hasPhase ?childPhase .
            ?childPhase a occp:PhaseA_Planning .
            ?childPhase occp:hasActualBeginning ?startInstant .
            ?startInstant occp:hasActualTime ?startTime .
        }
        ORDER BY ?startTime
        LIMIT 1
    }

    # Spätester Actual End
    OPTIONAL {
        SELECT ?parentPhase ?latestActualEnd
        WHERE {
            ?parentComponent occp:hasPhase ?parentPhase .
            ?parentPhase a occp:PhaseA_Planning .
            ?parentComponent ould:consistsOf ?childComponent .
            ?childComponent occp:hasPhase ?childPhase .
            ?childPhase a occp:PhaseA_Planning .
            ?childPhase occp:hasActualEnd ?endInstant .
            ?endInstant occp:hasActualTime ?endTime .
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



def generate_post_graph(pre_file, output_file):
    # Lade pre_graph
    pre_graph = Graph().parse(pre_file, format="turtle")
    
    # Erstelle post_graph_1 mit den inferierten Child-Daten
    post_graph_1 = Graph()
    post_graph_1 += pre_graph.query(CONSTRUCT_PHASE_A1).graph
    post_graph_1 += pre_graph.query(CONSTRUCT_PHASE_A2).graph
    post_graph_1 += pre_graph.query(CONSTRUCT_PHASE_B).graph
    post_graph_1 += pre_graph.query(CONSTRUCT_PHASE_C).graph
    post_graph_1 += pre_graph.query(CONSTRUCT_PHASE_D).graph
    post_graph_1 += pre_graph.query(CONSTRUCT_PHASE_M).graph
    post_graph_1 += pre_graph.query(CONSTRUCT_CYCLE_A).graph

    post_graph_2 = pre_graph + post_graph_1

    # Weitere Abfragen (falls nötig)
    post_graph_2 += post_graph_2.query(CONSTRUCT_PARENT_PHASES).graph
    post_graph_2 += post_graph_2.query(CONSTRUCT_PARENT_CYCLES).graph
    post_graph_2 += post_graph_2.query(CONSTRUCT_CYCLENUMBER).graph

    # Speichere das Ergebnis
    post_graph_2.serialize(output_file, format="turtle")
    return post_graph_2

if __name__ == "__main__":
    generate_post_graph()