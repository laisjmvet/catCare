import numpy as np

class QuestionSelection():
    def __init__(self, diseasesRules):
        self.diseasesRules = diseasesRules
        self.questionsSTD = {}

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
        self.questionsSTD = {}
        
        for rule in self.diseasesRules:
            diseasesVariables_id = rule['diseasesVariables_id']
            rules = self.calculateAnswer(rule['rules'])

            # If the diseasesVariables_id is not already in the self.questionsSTD dictionary, create a new entry
            if diseasesVariables_id not in self.questionsSTD:
                self.questionsSTD[diseasesVariables_id] = []

            # Append the rules to the existing diseasesVariables_id entry
            self.questionsSTD[diseasesVariables_id].append(rules)

        #Calculate the std for each question
        for key, value in self.questionsSTD.items():
            std_deviation = np.std(value)
            self.questionsSTD[key] = std_deviation

        return dict(sorted(self.questionsSTD.items(), key=lambda item: item[1], reverse=True))


