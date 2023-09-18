from datetime import *
import numpy as np
from models import Variables, Diseases, UsersAnswersCount, Pets

class DbRequests:
    def __init__(self):
        pass 

    # GETTING ALL DISEASE VARIABLES' IDS
    def getAllDiseaseVariablesIds(self):
        diseaseVariablesQuery = Variables.query.all()
        allDiseaseVariablesIds = []

        for diseaseVariable in diseaseVariablesQuery:
            diseaseVariable_dict = diseaseVariable.as_dict()
            allDiseaseVariablesIds.append(diseaseVariable_dict["id"])
        
        return allDiseaseVariablesIds

    # GETTING ALL DISEASES' IDS
    def getAllDiseasesIds(self):
        diseasesQuery = Diseases.query.all()
        allDiseasesIds = []

        for disease in diseasesQuery:
            disease_dict = disease.as_dict()
            allDiseasesIds.append(disease_dict["id"])
        
        return allDiseasesIds

    # GETTING ALL VARIABLES' IDS THAT TYPE IS TRUE
    def getAllTrueDefaultVariablesIds(self):
        true_default_variables = (
            Variables.query.filter_by(defaultQuestion=True).all()
        )
        all_true_default_variables = []

        for var in true_default_variables:
            var_dict = var.as_dict()
            all_true_default_variables.append(var_dict["id"])

        return all_true_default_variables

    def getAllFalseDefaultVariablesIds(self):
        false_default_variables = (
            Variables.query.filter_by(defaultQuestion=False).all()
        )
        # 
        all_false_default_variables = []

        for var in false_default_variables:
            var_dict = var.as_dict()
            all_false_default_variables.append(
                {"id": var_dict["id"], "question": var_dict["question"]}
            )

        return all_false_default_variables

    # def getAllDiseaseRules(self):
    #     diseaseRulesQuery =  UsersAnswersCount.query.all()
    #     lenDiseaseVariables = len(Variables.query.all())
    #     lenDiseases = len(Diseases.query.all())
    #     rulesMatrix = np.zeros((lenDiseases + 1, lenDiseaseVariables + 1))

    #     for rule in diseaseRulesQuery:
    #         rule_dict = rule.as_dict_for_probability_function()
    #         rulesMatrix[rule_dict["disease_id"]][
    #             rule_dict["diseasesVariables_id"]
    #         ] = calculateAnswer(rule_dict["rules"])
    #     print(rulesMatrix)
        return rulesMatrix
    
    def getFalseDiseaseRules(self):
        diseaseRulesQuery =  UsersAnswersCount.query.join(Variables, UsersAnswersCount.diseasesVariables_id == Variables.id).filter(Variables.defaultQuestion == False).all()
        diseasesRules = [] 

        for rule in diseaseRulesQuery:
            rule_dict = rule.as_dict_for_probability_function()
            diseasesRules.append(rule_dict)
        return diseasesRules

    # GET THE PET DETAILS BY ID
    def getPetDetailsbyId(self, petID):
        pet = Pets.query.filter_by(id=petID).all()
        selected_pet = None

        for p in pet:
            var_dict = p.as_dict()
            selected_pet = var_dict
        
        return selected_pet
    
   