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

class Newton(object):

    # config = Config('/src/config/config.yaml').read_config()

    def __init__(self):
        pass

    def NormalizeData(self, data, min=0, max=5):
        return (data - min) / (max - min)

    def compute_score(self, df_path, vegazero, groundtruth):
        vz = VegaZero2VegaLite()
        draco = Draco()
        df = pd.read_csv(df_path)
        isCompling = 0
        l_hard = 0.9
        l_sim = 0.5
        l_soft = 0.05
        l_acc = 1.5

        try:
            vegalite_gen_, vegazero_spec_ = vz.to_VegaLite(vegazero)
            _, vegazero_ground_spec_ = vz.to_VegaLite(groundtruth)

            sim = vz.vega_zero_groundtruth_similarity_score(vegazero, groundtruth)
            
            schema: dict = schema_from_dataframe(df) #Generating the data schema to extract the field types automatically
            spec = dict_to_facts(schema | vegalite_gen_) #converte in fact e concatena data e vis
            isVisCorrect = draco.check_spec(spec)
            violations = len(draco.get_violations(spec))

            isMarkCorrect = vegazero_spec_['mark'] == vegazero_ground_spec_['mark']
            isXCorrect = vegazero_spec_['encoding']['x'] == vegazero_ground_spec_['encoding']['x']
            isYCorrect = vegazero_spec_['encoding']['y']['y'] == vegazero_ground_spec_['encoding']['y']['y']

            score = -l_hard*(1-isVisCorrect)+ l_sim * sim - l_soft * violations + l_acc * (isMarkCorrect + isXCorrect + isYCorrect)

            res = {
                "isCompiled": 1, 
                "isVisCorrect": isVisCorrect,
                "sim": sim,
                "violations": violations,
                "isMarkCorrect": isMarkCorrect,
                "isXCorrect": isXCorrect,
                "isYCorrect":isYCorrect
            }
            if (score>=0):
                return [self.NormalizeData(score), res]
            else:
                return [0, res]

        except Exception as e:
            print(colored(f'error vegalite compile : {e}', 'red'))

        return {
                "isCompiled": 0, 
                "isVisCorrect": 0,
                "sim": 0,
                "violations": 0,
                "isMarkCorrect": 0,
                "isXCorrect": 0,
                "isYCorrect":0
            }

    def test(self, path):
        vegazero = "mark area data payments encoding x payment_type_code y aggregate average amount_paid group x"
        ground = "mark area data payments encoding x payment_type_code y aggregate average amount_paid group x"


        print(self.compute_score(path, vegazero, ground)[0])
        print(self.compute_score(path, vegazero, ground)[1])
    
