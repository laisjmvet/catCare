import numpy as np

class QuestionSelection():
    def __init__(self, diseasesRules):
        self.diseasesRules = diseasesRules
        self.answersMatrix = np.zeros((len(self.diseasesRules[0]), len(self.diseasesRules)))
        self.questionsSTD = []

    def findStandardDeviation(self):
        for i in range(len(self.diseasesRules)):
            for j in range(len(self.diseasesRules[i])):
                self.answersMatrix[j][i] = self.diseasesRules[i][j]
        
        for arr in self.answersMatrix:
            self.questionsSTD.append(np.std(arr))
        return np.argmax(self.questionsSTD)

                


