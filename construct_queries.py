# construct_queries.py
from rdflib import Graph

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
        VALUES ?startType { occp:BeginningOfPlanning }
    }
    OPTIONAL {
        ?startInstantEstimated a ?startType ;
                              occp:startsPhase ?phase ;
                              occp:hasEstimatedTime ?startTimeEstimated .
        FILTER NOT EXISTS { ?startInstantEstimated occp:hasActualTime ?anyActualTime . }
        VALUES ?startType { occp:BeginningOfPlanning }
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
        ?startInstantActual a ?startType ;
                           occp:startsCycle ?cycle ;
                           occp:hasActualTime ?startTimeActual .
        FILTER NOT EXISTS { ?startInstantActual occp:hasEstimatedTime ?anyEstimatedTime . }
        VALUES ?startType { occp:ReviewRejection }
    }
    OPTIONAL {
        ?startInstantEstimated a ?startType ;
                              occp:startsCycle ?cycle ;
                              occp:hasEstimatedTime ?startTimeEstimated .
        FILTER NOT EXISTS { ?startInstantEstimated occp:hasActualTime ?anyActualTime . }
        VALUES ?startType { occp:ReviewRejection }
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

CONSTRUCT_COMPONENTS = """
PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
CONSTRUCT {
      ?obj occp:hasPhase ?phaseA .
      ?phaseA a occp:PhaseA_Planning ;
              occp:hasActualBeginning ?beginA ;
              occp:hasActualEnd ?endA .
      ?beginA a occp:BeginningOfPlanning ;
              occp:hasActualTime "2023-01-01"^^xsd:date .
      ?endA a occp:CompletionOfPlanning ;
          occp:hasActualTime "2023-03-01"^^xsd:date .

      ?obj occp:hasPhase ?phaseB .
      ?phaseB a occp:PhaseB_Review ;
              occp:hasActualBeginning ?beginB ;
              occp:hasActualEnd ?endB .
      ?beginB a occp:SubmissionToReview ;
              occp:hasActualTime "2023-03-02"^^xsd:date .
      ?endB a occp:ReviewApproval ;
          occp:hasActualTime "2023-04-01"^^xsd:date .

      ?obj occp:hasPhase ?phaseC .
      ?phaseC a occp:PhaseC_Construction ;
              occp:hasActualBeginning ?beginC ;
              occp:hasActualEnd ?endC .
      ?beginC a occp:StartOfConstruction ;
              occp:hasActualTime "2023-04-02"^^xsd:date .
      ?endC a occp:CompletionOfConstruction ;
          occp:hasActualTime "2023-06-01"^^xsd:date .

      ?cycleA1 a occp:CycleA_PlanningReview ;
              occp:includesPhase ?phaseA ;
              occp:includesPhase ?phaseB .
      ?cycleA2 a occp:CycleA_Construction ;
              occp:includesPhase ?phaseC .
  }
  WHERE {
      ?obj a occp:DataObject .
      BIND(IRI(CONCAT(STR(?obj), "_phaseA")) AS ?phaseA)
      BIND(IRI(CONCAT(STR(?obj), "_phaseB")) AS ?phaseB)
      BIND(IRI(CONCAT(STR(?obj), "_phaseC")) AS ?phaseC)
      BIND(IRI(CONCAT(STR(?obj), "_beginA")) AS ?beginA)
      BIND(IRI(CONCAT(STR(?obj), "_endA")) AS ?endA)
      BIND(IRI(CONCAT(STR(?obj), "_beginB")) AS ?beginB)
      BIND(IRI(CONCAT(STR(?obj), "_endB")) AS ?endB)
      BIND(IRI(CONCAT(STR(?obj), "_beginC")) AS ?beginC)
      BIND(IRI(CONCAT(STR(?obj), "_endC")) AS ?endC)
      BIND(IRI(CONCAT(STR(?obj), "_cycleA1")) AS ?cycleA1)
      BIND(IRI(CONCAT(STR(?obj), "_cycleA2")) AS ?cycleA2)
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

    # Phase C
    post_graph += pre_graph.query(CONSTRUCT_PHASE_C).graph

    # Phase D
    post_graph += pre_graph.query(CONSTRUCT_PHASE_D).graph

    # Phase M
    post_graph += pre_graph.query(CONSTRUCT_PHASE_M).graph
    
    # Cycle A
    post_graph += pre_graph.query(CONSTRUCT_CYCLE_A).graph

    # Components
    post_graph += pre_graph.query(CONSTRUCT_COMPONENTS).graph
    
    # Speichern
    post_graph.serialize(output_file, format="turtle")
    return post_graph

if __name__ == "__main__":
    generate_post_graph()