# construct_queries.py

# Base CONSTRUCT query for PhaseA and CycleA (as used in PreI_1.ttl)
CONSTRUCT_BASE = """
    PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
    CONSTRUCT {
        ?phase occp:hasActualBeginning ?instantStart .
        ?cycle occp:hasActualBeginning ?instantStart .
        ?cycle occp:isInPhase ?phase .
        ?cycle occp:hasCycleNumber ?cycleNumber .
        ?instantEnd occp:endsPhase ?phase .
        ?instantEnd occp:endsCycle ?cycle .
        ?phase occp:hasEstimatedEnd ?instantEnd .
        ?cycle occp:hasEstimatedEnd ?instantEnd .
    }
    WHERE {
        ?instantStart a occp:BeginningOfPlanning ;
            occp:startsPhase ?phase ;
            occp:startsCycle ?cycle ;
            occp:hasActualTime ?startTime .
        ?component occp:hasPhase ?phase ;
            occp:hasCycle ?cycle .
        ?instantEnd a occp:ReviewApproval ;
            occp:endsPhase ?phase ;
            occp:endsCycle ?cycle ;
            occp:hasEstimatedTime ?endTime .
        OPTIONAL {
            ?cycle occp:hasCycleNumber ?existingNumber .
        }
        BIND(COALESCE(?existingNumber, 1) AS ?cycleNumber)
    }
"""

# construct_queries.py
CONSTRUCT_EXTENDED = """
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