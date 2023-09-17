import numpy as np

class QuestionSelection():
    def __init__(self, diseasesRules):
        self.diseasesRules = diseasesRules
        self.answersMatrix = []
        self.questionsSTD = []

    def calculateAnswer(self, AnswerCounts):
        if sum(AnswerCounts) == 0.0:
            # Disease nor cataloged yet.
            return 0.5

        AvgAnswer = (
            AnswerCounts[0] * 0.00
            + AnswerCounts[1] * 0.25
            + AnswerCounts[2] * 0.50
            + AnswerCounts[3] * 0.75
            + AnswerCounts[4] * 1.0
        )
        AvgAnswer /= sum(AnswerCounts)
        return AvgAnswer

    def findStandardDeviation(self):
        organized_data = {}
        # print(self.diseasesRules)
        for rule in self.diseasesRules:
            diseasesVariables_id = rule['diseasesVariables_id']
            rules = self.calculateAnswer(rule['rules'])

            # If the diseasesVariables_id is not already in the organized_data dictionary, create a new entry
            if diseasesVariables_id not in organized_data:
                organized_data[diseasesVariables_id] = []

            # Append the rules to the existing diseasesVariables_id entry
            organized_data[diseasesVariables_id].append(rules)
        
        print(organized_data)


