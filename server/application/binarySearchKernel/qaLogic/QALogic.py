import os
import sys
from pathlib import Path
import random as rd

full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(str(Path(full_path).parents[2]))

from application.binarySearchKernel.numericLogic import Bayes
from application.binarySearchKernel.dbRequests import DbRequests
from datetime import *

class QALogic():
    def __init__(self, maxIter):
        self.dbRequests = DbRequests()
        self.maxIter = maxIter
        self.allVariables = self.dbRequests.getAllDiseaseVariablesIds()
        self.allDiseases = self.dbRequests.getAllDiseasesIds()
        self.allRules = self.dbRequests.getAllDiseaseRules()
        self.falseVariableQuestions = self.dbRequests.getAllFalseDefaultVariablesIds()
        self.bayesObj = Bayes(self.allVariables, self.allDiseases, self.allRules)
        self.diseasesVariables_so_far = []
        self.answers_so_far = []

    def as_dict(self):
        return {
            "diseasesVariables_so_far": self.diseasesVariables_so_far,
            "answers_so_far": self.answers_so_far,
        } 

    def setQuestionAnswer(self, variableID, answer):
            if type(variableID) == type(list()) or type(answer) == type(list()):
                if len(variableID) != len(answer):
                    print("Error: List with different sizes.")

                for var in variableID:
                    self.diseasesVariables_so_far.append(var)
                for ans in answer:
                    self.answers_so_far.append(ans)
            else:
                self.diseasesVariables_so_far.append(variableID)
                self.answers_so_far.append(answer)  

    def getDynamicQuestion(self, userResponse = [{'questionNumber': 3, 'questionID': 10, 'answer': 5}, {'questionNumber': 4, 'questionID': 1, 'answer': 4}, {'questionNumber': 5, 'questionID': 28, 'answer': 4}, {'questionNumber': 6, 'questionID': 21, 'answer': 4}], questionsIDs = [10, 1, 28, 21, 28]
    ):
            # Start with a random algorithm
            dynamicQuestion = []
            questionsIDs = [*questionsIDs]
            if userResponse[-1]['questionNumber'] < self.maxIter:
                question_ID = rd.randint(0, len(self.falseVariableQuestions) - 1)            
                if question_ID not in questionsIDs:
                    questionsIDs.append(question_ID)
                    dynamicQuestion.append(self.falseVariableQuestions[question_ID])
            return dynamicQuestion
    
    def answerDefaultAnamnese(self, obj):
        current_date = datetime.now().date()
        age = datetime.strptime(str(obj["dob"]), "%Y-%m-%d")
        age_in_years = ((current_date - datetime.date(age)).days) / 360
        sex = obj["sex"]
        diet = obj["diet"]
        outdoor = obj["outdoor"]
        contactWithOtherPets = obj["contactWithOtherPets"]
        neutered = obj["neutered"]
        answers = []

        if age_in_years < 1:
            answers.append(0.00)
        elif age_in_years >= 1 and age_in_years < 2:
            answers.append(0.25)
        elif age_in_years >= 2 and age_in_years < 5:
            answers.append(0.50)
        elif age_in_years >= 5 and age_in_years < 7:
            answers.append(0.75)
        else:
            answers.append(1.00)

        if sex == "Male":
            answers.append(1.00)
        else:
            answers.append(0.00)

        if outdoor == False:
            answers.append(0.00)
        else:
            answers.append(1.00)

        if contactWithOtherPets == True:
            answers.append(1.00)
        else:
            answers.append(0.00)

        if neutered == True:
            answers.append(1.00)
        else:
            answers.append(0.00)

        if diet == "Processed":
            answers.append(1.00)
        elif diet == "Mixed":
            answers.append(0.50)
        elif diet == "natural":
            answers.append(0.00)

        return answers

    def answersDynamicQuestions(self, answers):
        answersConverted = []
        for answer in answers:
            if answer == 1:
                answersConverted.append(0.0)
            elif answer == 2:
                answersConverted.append(0.25)
            elif answer == 3:
                answersConverted.append(0.5)
            elif answer == 4:
                answersConverted.append(0.75)
            elif answer == 5:
                answersConverted.append(1.0)
            else:
                raise TypeError("Numbers must be from 1 to 5")

        return answersConverted

    def sendQuestions(self):
        falseVariableQuestions = self.dbRequests.getAllFalseDefaultVariablesIds()
        dynamicQuestion = self.bayesObj.getDynamicQuestion(falseVariableQuestions)
        return dynamicQuestion

    def findDiagnosis(
        self,
        pet_id=1,
        questionsAnswered=[1, 2, 3, 4, 5, 6, 7, 8, 13, 27, 25, 22, 21, 20, 19],
        answersUser=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5, 5, 5, 5],
    ):
        defaultVariableQuestions = self.dbRequests.getAllTrueDefaultVariablesIds()
        petDetails = self.dbRequests.getPetDetailsbyId(pet_id)
        answersTrueDefaultAnamnese = self.answerDefaultAnamnese(petDetails)
        self.setQuestionAnswer(defaultVariableQuestions, answersTrueDefaultAnamnese)
        answersDynamicQuestions = self.answersDynamicQuestions(answersUser)
        self.setQuestionAnswer(questionsAnswered, answersDynamicQuestions)
        probabilities = self.bayesObj.Solve(self.diseasesVariables_so_far, self.answers_so_far)
        return probabilities

print(QALogic(15).findDiagnosis())
