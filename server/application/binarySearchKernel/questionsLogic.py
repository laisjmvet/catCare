import os
import sys
from pathlib import Path

full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(str(Path(full_path).parents[1]))

from application.binarySearchKernel import logicUtilityFunctions, BayesLib
from logicUtilityFunctions import *

allVariables = getAllDiseaseVariablesIds()
allDiseases = getAllDiseasesIds()
allRules = getAllDiseaseRules()

# Initiate BayesLib
BayesLibObj = BayesLib(allVariables, allDiseases, allRules, maxIter=15)


def sendQuestions():
    falseVariableQuestions = getAllFalseDefaultVariablesIds()
    randomQuestions = BayesLibObj.getRandomQuestions(falseVariableQuestions)
    return randomQuestions

def sendQuestions2():
    falseVariableQuestions = getAllFalseDefaultVariablesIds()
    randomQuestions = BayesLibObj.getDynamicQuestion(falseVariableQuestions)
    return randomQuestions

print(sendQuestions2(), "<<<<<<<<<<<<")

def findDiagnosis(
    pet_id=1,
    questionsAnswered=[1, 2, 3, 4, 5, 6, 7, 8, 13, 27, 25, 22, 21, 20, 19],
    answersUser=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5, 5, 5, 5],
):
    defaultVariableQuestions = getAllTrueDefaultVariablesIds()
    petDetails = getPetDetailsbyId(pet_id)
    answersTrueDefaultAnamnese = answerDefaultAnamnese(petDetails)
    BayesLibObj.setQuestionAnswer(defaultVariableQuestions, answersTrueDefaultAnamnese)
    answersRandomAnamnese = answerRandomAnamnese(answersUser)
    BayesLibObj.setQuestionAnswer(questionsAnswered, answersRandomAnamnese)
    probabilities = BayesLibObj.Solve()
    return probabilities
