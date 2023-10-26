__author__ = "Luca Podo"

# from config.config import Config
from newtonmetrics.vegazero.VegaZero2VegaLite import VegaZero2VegaLite
import pandas as pd
import altair as alt
from draco import Draco
from draco.schema import schema_from_dataframe
import pandas as pd
from termcolor import colored
from draco.fact_utils import dict_to_facts, answer_set_to_dict
from draco.run import run_clingo
import re

class Newton(object):

    # config = Config('/src/config/config.yaml').read_config()
    vz = VegaZero2VegaLite()
    draco = Draco()

    def __init__(self):
        pass

    def NormalizeData(self, data, min=0, max=5):
        return (data - min) / (max - min)

    def sanitize_column_names(self, df):
        # Define a regular expression pattern to match non-alphabet characters
        pattern = re.compile(r'[^a-zA-Z]')

        # Use a lambda function to apply the pattern to each column name and replace non-alphabet characters with an empty string
        df.columns = df.columns.to_series().apply(lambda x: re.sub(pattern, '', x))

        return df

    def compute_score(self, df_path, vegazero, groundtruth):
        
        df = pd.read_csv(df_path, index_col=0)
        df = self.sanitize_column_names(df)

        isCompling = 0
        l_hard = 0.9
        l_sim = 0.5
        l_soft = 0.05
        l_acc = 1.5

        score= 0

        res = {
                "isCompiled": 0, 
                "isVisCorrect": None,
                "sim": None,
                "violations": None,
                "isMarkCorrect": None,
                "isXCorrect": None,
                "isYCorrect":None,
                "score": 0
            }

        try:
            vegalite_gen_, vegazero_spec_ = self.vz.to_VegaLite(vegazero)

            try:
                _, vegazero_ground_spec_ = self.vz.to_VegaLite(groundtruth)
                res['isCompiled'] = 1

                sim = self.vz.vega_zero_groundtruth_similarity_score(vegazero, groundtruth)
                res['sim'] = sim

                schema: dict = schema_from_dataframe(df) #Generating the data schema to extract the field types automatically
                spec = dict_to_facts(schema | vegalite_gen_) #converte in fact e concatena data e vis
                isVisCorrect = self.draco.check_spec(spec)
                res['isVisCorrect'] = isVisCorrect
                violations = len(self.draco.get_violations(spec))
                res['violations']=violations

                isMarkCorrect = vegazero_spec_['mark'] == vegazero_ground_spec_['mark']
                res['isMarkCorrect'] = isMarkCorrect
                isXCorrect = vegazero_spec_['encoding']['x'] == vegazero_ground_spec_['encoding']['x']
                res['isXCorrect'] = isXCorrect
                isYCorrect = vegazero_spec_['encoding']['y']['y'] == vegazero_ground_spec_['encoding']['y']['y']
                res['isYCorrect'] = isYCorrect

                score = -l_hard*(1-isVisCorrect)+ l_sim * sim - l_soft * violations + l_acc * (isMarkCorrect + isXCorrect + isYCorrect)
                if (score>=0):
                    res['score'] =  self.NormalizeData(score)
                else:
                    res['score'] = 0
            except:
                res['isCompiled'] = 0
        except Exception as e:
            res['isCompiled'] = 0

            
        # sim = vz.vega_zero_groundtruth_similarity_score(vegazero, groundtruth)
        
        # schema: dict = schema_from_dataframe(df) #Generating the data schema to extract the field types automatically
        # spec = dict_to_facts(schema | vegalite_gen_) #converte in fact e concatena data e vis
        # isVisCorrect = self.draco.check_spec(self.spec)
        # violations = len(self.draco.get_violations(self.spec))

        # isMarkCorrect = vegazero_spec_['mark'] == vegazero_ground_spec_['mark']
        # isXCorrect = vegazero_spec_['encoding']['x'] == vegazero_ground_spec_['encoding']['x']
        # isYCorrect = vegazero_spec_['encoding']['y']['y'] == vegazero_ground_spec_['encoding']['y']['y']

        # score = -l_hard*(1-isVisCorrect)+ l_sim * sim - l_soft * violations + l_acc * (isMarkCorrect + isXCorrect + isYCorrect)

        # res = {
        #     "isCompiled": 1, 
        #     "isVisCorrect": isVisCorrect,
        #     "sim": sim,
        #     "violations": violations,
        #     "isMarkCorrect": isMarkCorrect,
        #     "isXCorrect": isXCorrect,
        #     "isYCorrect":isYCorrect
        # }
        return res 
        # if (score>=0):
        #         return [self.NormalizeData(score), res]
        # else:
        #     return [0, res]

    def test(self, path):
        vegazero = "mark area data payments encoding x payment_type_code y aggregate average amount_paid group x"
        ground = "mark area data payments encoding x payment_type_code y aggregate average amount_paid group x"


        print(self.compute_score(path, vegazero, ground)[0])
        print(self.compute_score(path, vegazero, ground)[1])
    
    