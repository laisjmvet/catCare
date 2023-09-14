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
        # self.allVariables = self.dbRequests.getAllDiseaseVariablesIds()
        # self.allDiseases = self.dbRequests.getAllDiseasesIds()
        # self.allRules = self.dbRequests.getAllDiseaseRules()
        #self.falseVariableQuestions = self.dbRequests.getAllFalseDefaultVariablesIds()
        # self.bayesObj = Bayes(self.allVariables, self.allDiseases, self.allRules)
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

    def getDynamicQuestion(self, userResponse, questionsIDs):

        print("I got inside getDynamic Question")
        falseVariablesQuestions = self.dbRequests.getAllFalseDefaultVariablesIds() 
        print("After getting all falseVariables")   
        # self.dbRequests.closeSession()
        dynamicQuestion = []
        questionsIDs = [*questionsIDs]
        question_ID = rd.randint(0, len(falseVariablesQuestions) - 1)
        print(questionsIDs, "*************", question_ID)
        
        def findQuestionID(id, falseVariablesQuestions):
            #Sometimes the random id might not be in the falseVariablesQuestions, so i am creating a while loop if that id is not found
            id_not_found = True
            nonlocal question_ID
            while id_not_found:                
                for question in falseVariablesQuestions:
                    if question['id'] == id:                    
                        dynamicQuestion.append(question)
                        id_not_found = False         
                        return dynamicQuestion
                    else:
                        question_ID = rd.randint(0, len(falseVariablesQuestions) - 1)

        if userResponse == []:             
            findQuestionID(question_ID, falseVariablesQuestions)
            return dynamicQuestion  
        elif userResponse[-1]['questionNumber'] < self.maxIter:
            if question_ID not in questionsIDs:
                findQuestionID(question_ID, falseVariablesQuestions)
            else:
                id_already_used = True
                while id_already_used: 
                    question_ID = rd.randint(0, len(falseVariablesQuestions) - 1)
                    if question_ID not in questionsIDs:
                        dynamicQuestion.append(falseVariablesQuestions[question_ID])
                        id_already_used = False
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

    # def sendQuestion(self, userResponse, questionsIDs):
    #     falseVariableQuestions = DbRequests().getAllFalseDefaultVariablesIds()
    #     dynamicQuestion = self.getDynamicQuestion(userResponse, questionsIDs)
    #     return dynamicQuestion

    def findDiagnosis(
        self,
        pet_id=1,
        questionsAnswered=[1, 2, 3, 4, 5, 6, 7, 8, 13, 27, 25, 22, 21, 20, 19],
        answersUser=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5, 5, 5, 5],
    ):
        dbRequests = DbRequests()
        allVariables = dbRequests.getAllDiseaseVariablesIds()
        allDiseases = dbRequests.getAllDiseasesIds()
        allRules = dbRequests.getAllDiseaseRules()
        bayesObj = Bayes(allVariables, allDiseases, allRules)
        defaultVariableQuestions = dbRequests.getAllTrueDefaultVariablesIds()
        petDetails = dbRequests.getPetDetailsbyId(pet_id)
        answersTrueDefaultAnamnese = self.answerDefaultAnamnese(petDetails)
        self.setQuestionAnswer(defaultVariableQuestions, answersTrueDefaultAnamnese)
        answersDynamicQuestions = self.answersDynamicQuestions(answersUser)
        self.setQuestionAnswer(questionsAnswered, answersDynamicQuestions)
        probabilities = bayesObj.Solve(self.diseasesVariables_so_far, self.answers_so_far)
        return probabilities
