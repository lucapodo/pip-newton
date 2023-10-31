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

    version_newton = "0.0.1"

    def __init__(self):
        pass

    def version(self):
        print (f"Tool version {self.version_newton}")

    def NormalizeData(self, data, min=0, max=5):
        return (data - min) / (max - min)

    def sanitize_column_names(self, df):
        # Define a regular expression pattern to match non-alphabet characters
        pattern = re.compile(r'[^a-zA-Z]')

        # Use a lambda function to apply the pattern to each column name and replace non-alphabet characters with an empty string
        df.columns = df.columns.to_series().apply(lambda x: re.sub(pattern, '', x))

        return df

    def compute_score(self, df_path, vegazero, groundtruth):
        
        # df = pd.read_csv(df_path, index_col=0)
   
        # df = self.sanitize_column_names(df)

        isCompling = 0
        l_hard = 0.9
        l_sim = 0.5
        l_soft = 0.05
        l_acc = 1.5

        sim = 0
        isMarkCorrect = False
        isXCorrect =  False
        isYCorrect = False

        score= 0

        res = {
                "isCompiled": None, 
                "isVisCorrect": None,
                "sim": None,
                "violations": None,
                "isMarkCorrect": None,
                "isXCorrect": None,
                "isYCorrect": None,
                "score": None,
                "isCompiled_g": None
            }

        try:
            _, vegazero_spec_ = self.vz.to_VegaLite(vegazero)
            res['isCompiled'] = 1
        except Exception as e:
            res['isCompiled'] = 0
        
        try:
            _, vegazero_ground_spec_ = self.vz.to_VegaLite(groundtruth)
            res['isCompiled_g'] = 1
        except Exception as e:
            res['isCompiled_g'] = 0
        
        try:
            isMarkCorrect = vegazero_spec_['mark'] == vegazero_ground_spec_['mark']
            res['isMarkCorrect'] = isMarkCorrect
        except Exception as e:
            res['isMarkCorrect'] = False
        
        try:
            isXCorrect = vegazero_spec_['encoding']['x'] == vegazero_ground_spec_['encoding']['x']
            res['isXCorrect'] = isXCorrect
        except Exception as e:
            res['isXCorrect'] = False
        
        try:
            isYCorrect = vegazero_spec_['encoding']['y']['y'] == vegazero_ground_spec_['encoding']['y']['y']
            res['isYCorrect'] = isYCorrect
        except Exception as e:
            res['isYCorrect'] = False
        
        try:
            sim = self.vz.vega_zero_groundtruth_similarity_score(vegazero, groundtruth)
            res['sim'] = sim
        except Exception as e:
            res['sim'] = -1
            
        

        # if(res['isCompiled_g']==1 and res['isCompiled']==1):

        #     sim = self.vz.vega_zero_groundtruth_similarity_score(vegazero, groundtruth)
        #     res['sim'] = sim       

            # try:
            #     schema: dict = schema_from_dataframe(df) #Generating the data schema to extract the field types automatically
            #     spec = dict_to_facts(schema | vegalite_gen_) #converte in fact e concatena data e vis
            #     isVisCorrect = self.draco.check_spec(spec)
            #     res['isVisCorrect'] = isVisCorrect
            #     violations = len(self.draco.get_violations(spec))
            #     res['violations'] = violations
            # except Exception as e:
            #     res['isVisCorrect'] = False
            #     res['violations'] = False
            
        # score = l_sim * sim + l_acc * (isMarkCorrect + isXCorrect + isYCorrect)
        # score = -l_hard*(1-isVisCorrect)+ l_sim * sim - l_soft * violations + l_acc * (isMarkCorrect + isXCorrect + isYCorrect)

        # if (score>=0):
        #     res['score'] =  self.NormalizeData(1)
        # else:
        #     res['score'] = 0
        
       
       
        return res 
        
    def test(self, path):
        vegazero = "mark area data payments encoding x payment_type_code y aggregate average amount_paid group x"
        ground = "mark area data payments encoding x payment_type_code y aggregate average amount_paid group x"


        # print(self.compute_score(path, vegazero, ground)[0])
        # print(self.compute_score(path, vegazero, ground)[1])

    def test_draco(self):
        import pandas as pd
        import os
        eval_df = pd.read_csv("/Users/luca/Documents/Dottorato/LLM4VIS/Newton/data/raw/Newton/evaluation.csv")
        newton_df = pd.read_csv("/Users/luca/Documents/Dottorato/LLM4VIS/Newton/data/final/NewtonLLM dataset/newtow_test.csv")

        # for i in range(100, len(eval_df)):
        #     print(i)
        i=100
        try:
            ground = eval_df['groundtruth'][i]
            prediction = eval_df['prediction'][i]

            id = newton_df[newton_df['output'] == ground]['tvBench_id'].values[0]
            path = os.path.join('/Users/luca/Documents/Dottorato/LLM4VIS/Newton/data/final/NewtonLLM dataset/datasets', id +'.csv')
            df = pd.read_csv(path)

            vegalite_gen_, _ = self.vz.to_VegaLite(prediction)

            schema: dict = schema_from_dataframe(df) #Generating the data schema to extract the field types automatically
            spec = dict_to_facts(schema | vegalite_gen_) #converte in fact e concatena data e vis
          
            if self.draco.check_spec(spec):
                print('ciao')
            else: 
                print('errore')
            # if self.draco.check_spec(spec):
            #     print('cioa')
            #     yield spec
            # else: 
            #     print(id)
            
        except Exception as e:
            print(e)
            pass
            # break






# n = Newton()

# vegazero =  "mark area data apartment_bookings encoding x booking_start_date y aggregate count booking_start_date transform group x sort y asc"
# ground = "mark area data apartment_bookings encoding x booking_start_date y aggregate count booking_start_date transform group x sort y asc"

# n.test_draco()
    
    