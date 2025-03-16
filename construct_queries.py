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

# Extended CONSTRUCT query for multiple phases (e.g., PhaseA, PhaseB, PhaseC)
CONSTRUCT_EXTENDED = """
    PREFIX occp: <http://www.semanticweb.org/albrechtvaatz/ontologies/2022/9/cMod_V0.1#>
    CONSTRUCT {
        ?phase occp:hasActualBeginning ?startInstant .
        ?cycle occp:hasActualBeginning ?startInstant .
        ?cycle occp:isInPhase ?phase .
        ?cycle occp:hasCycleNumber ?cycleNumber .
        ?endInstant occp:endsPhase ?phase .
        ?endInstant occp:endsCycle ?cycle .
        ?phase occp:hasActualEnd ?endInstant .
        ?cycle occp:hasActualEnd ?endInstant .
        ?phase occp:hasEstimatedBeginning ?startInstant .
        ?cycle occp:hasEstimatedBeginning ?startInstant .
        ?phase occp:hasEstimatedEnd ?endInstant .
        ?cycle occp:hasEstimatedEnd ?endInstant .
    }
    WHERE {
        # Start instants (actual or estimated beginnings)
        { ?startInstant a ?startType ;
            occp:startsPhase ?phase ;
            occp:startsCycle ?cycle ;
            occp:hasActualTime ?startTime .
          VALUES ?startType { occp:BeginningOfPlanning occp:SubmissionToReview occp:BeginningOfConstruction }
        }
        UNION
        { ?startInstant a ?startType ;
            occp:startsPhase ?phase ;
            occp:startsCycle ?cycle ;
            occp:hasEstimatedTime ?startTime .
          VALUES ?startType { occp:BeginningOfPlanning occp:SubmissionToReview occp:BeginningOfConstruction }
        }
        ?component occp:hasPhase ?phase ;
            occp:hasCycle ?cycle .
        # End instants (actual or estimated ends)
        { ?endInstant a ?endType ;
            occp:endsPhase ?phase ;
            occp:endsCycle ?cycle ;
            occp:hasActualTime ?endTime .
          VALUES ?endType { occp:ReviewApproval occp:ReviewRejection occp:CompletionOfConstruction }
        }
        UNION
        { ?endInstant a ?endType ;
            occp:endsPhase ?phase ;
            occp:endsCycle ?cycle ;
            occp:hasEstimatedTime ?endTime .
          VALUES ?endType { occp:ReviewApproval occp:ReviewRejection occp:CompletionOfConstruction }
        }
        OPTIONAL {
            ?cycle occp:hasCycleNumber ?existingNumber .
        }
        BIND(COALESCE(?existingNumber, 1) AS ?cycleNumber)
    }
"""