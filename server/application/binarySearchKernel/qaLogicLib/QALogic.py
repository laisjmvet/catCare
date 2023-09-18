import random as rd
from datetime import *
from binarySearchKernel import DbRequests, QuestionSelection

class QALogic():
    def __init__(self, maxIter):
        self.dbRequests = DbRequests()
        self.maxIter = maxIter
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

        falseVariablesQuestions = self.dbRequests.getAllFalseDefaultVariablesIds() #getting all questions
        diseasesRules = self.dbRequests.getFalseDiseaseRules() #getting all rules from the questions that are not default
        dynamicQuestion = [] #keeping track of the questions already sent
        questionsIDs = [*questionsIDs] #keeping track of the questions ids already sent
        questionSelection = QuestionSelection(diseasesRules) #initializing the class

        if userResponse == [] or userResponse[-1]['questionNumber'] < self.maxIter:
            for key in questionSelection.findStandardDeviation().items():                
                for question in falseVariablesQuestions:
                    if question['id'] == key[0] and key[0] not in questionsIDs: #the questions sent must meet the id and not repeat
                        dynamicQuestion.append(question)
                        return dynamicQuestion
                    else:
                        continue 
        else:
            return 'no more questions'
            
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

    def findDiagnosis(
        self,
        pet_id=1,
        questionsAnswered=[1, 2, 3, 4, 5, 6, 7, 8, 13, 27, 25, 22, 21, 20, 19],
        answersUser=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5, 5, 5, 5],
    ):
        allVariables = self.dbRequests.getAllDiseaseVariablesIds()
        allDiseases = self.dbRequests.getAllDiseasesIds()
        allRules = self.dbRequests.getAllDiseaseRules()
        bayesObj = Bayes(allVariables, allDiseases, allRules)
        defaultVariableQuestions = self.dbRequests.getAllTrueDefaultVariablesIds()
        petDetails = self.dbRequests.getPetDetailsbyId(pet_id)
        answersTrueDefaultAnamnese = self.answerDefaultAnamnese(petDetails)
        self.setQuestionAnswer(defaultVariableQuestions, answersTrueDefaultAnamnese)
        answersDynamicQuestions = self.answersDynamicQuestions(answersUser)
        self.setQuestionAnswer(questionsAnswered, answersDynamicQuestions)
        probabilities = bayesObj.Solve(self.diseasesVariables_so_far, self.answers_so_far)
        return probabilities
