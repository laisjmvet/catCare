import os
import sys
from pathlib import Path

full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(str(Path(full_path).parents[2]))

# Import necessary modules
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from application.db import DATABASE_URL
from datetime import *
from application.models import Variables, Diseases, UsersAnswersCount, Pets
from BayesLib import CalculateAnswer
import numpy as np

# Create an engine and bind it to a session

class DbRequests:
    def __init__(self):
        self.dbURL = "postgresql://qbmdycoi:dvg0nKw0ZAZ5cvAZH7Z205BkJPhYpe4v@trumpet.db.elephantsql.com/qbmdycoi"
        self.engine = create_engine(self.dbURL)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()        

    # GETTING ALL DISEASE VARIABLES' IDS
    def getAllDiseaseVariablesIds(self):
        diseaseVariablesQuery = self.session.query(Variables).all()
        allDiseaseVariablesIds = []

        for diseaseVariable in diseaseVariablesQuery:
            diseaseVariable_dict = diseaseVariable.as_dict()
            allDiseaseVariablesIds.append(diseaseVariable_dict["id"])

        return allDiseaseVariablesIds

    # GETTING ALL DISEASES' IDS
    def getAllDiseasesIds(self):
        diseasesQuery = self.session.query(Diseases).all()
        allDiseasesIds = []

        for disease in diseasesQuery:
            disease_dict = disease.as_dict()
            allDiseasesIds.append(disease_dict["id"])

        return allDiseasesIds

    # GETTING ALL VARIABLES' IDS THAT TYPE IS TRUE
    def getAllTrueDefaultVariablesIds(self):
        true_default_variables = (
            self.session.query(Variables).filter_by(defaultQuestion=True).all()
        )
        all_true_default_variables = []

        for var in true_default_variables:
            var_dict = var.as_dict()
            all_true_default_variables.append(var_dict["id"])

        return all_true_default_variables


    def getAllFalseDefaultVariablesIds(self):
        false_default_variables = (
            self.session.query(Variables).filter_by(defaultQuestion=False).all()
        )
        all_false_default_variables = []

        for var in false_default_variables:
            var_dict = var.as_dict()
            all_false_default_variables.append(
                {"id": var_dict["id"], "question": var_dict["question"]}
            )

        return all_false_default_variables

    def getAllDiseaseRules(self):
        diseaseRulesQuery = self.session.query(UsersAnswersCount).all()
        lenDiseaseVariables = len(self.session.query(Variables).all())
        lenDiseases = len(self.session.query(Diseases).all())
        rulesMatrix = np.zeros((lenDiseases + 1, lenDiseaseVariables + 1))

        for rule in diseaseRulesQuery:
            rule_dict = rule.as_dict_for_probability_function()
            rulesMatrix[rule_dict["disease_id"]][
                rule_dict["diseasesVariables_id"]
            ] = CalculateAnswer(rule_dict["rules"])

        return rulesMatrix

    # GET THE PET DETAILS BY ID
    def getPetDetailsbyId(self, petID):
        pet = self.session.query(Pets).filter_by(id=petID).all()
        selected_pet = None

        for p in pet:
            var_dict = p.as_dict()
            selected_pet = var_dict

        return selected_pet
