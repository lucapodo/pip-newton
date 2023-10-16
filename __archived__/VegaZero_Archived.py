

"""
    All moved to VegaZero2Vegalite.py file
"""
import re
# import pandas as pd
# import json
# import ast
# from itertools import product
# from collections import Counter
# from nltk.util import ngrams
# from vegazero.Utils import Utils as utils

# class VegaZero():

#     def __init__(self):
#         pass

#     def return_vega_zero_fields(vega_zero_query):
#         """
#         Function that returns the values corresponding to the vega zero keywords specified
        
#         Parameters
#         ----------
#         vega_zero_query : string
#             Vega zero string

#         Returns
#         -------
#         vega_zero_dict : dict
#             Dictionary that contains the kayrowds-values pairs of from a vega zero string

#         Notes
#         -----
#         This function has been used to convert the vega zero strings avaiable in NcNet dataset into a dictionary with the correspoding values for each keyword.
#         It focus only on the mark, data, encoding x and y aggregate keywords, the color and tranform are converted as a single string
#         """
#         vega_zero_fields = ['mark', 'data', 'encoding x', 'y aggregate', 'color', 'transform']
#         keywords = []

#         vega_zero_query = vega_zero_query.replace("\"", "\'")
    
#         for field in vega_zero_fields:
#             if(field in vega_zero_query):
#                 keywords.append(field)
#                 vega_zero_query = re.sub(r"\b%s\b" % field, '[UNK]', vega_zero_query)

#         vega_zero_query_tf = vega_zero_query.split('[UNK]')[1:]
#         vega_zero_query_tf = [val.strip() for val in vega_zero_query_tf]

#         vega_zero_dict = dict(zip(keywords, vega_zero_query_tf))
#         return vega_zero_dict

#     def train_test_split(df, col="hardness" ,p=20):
#         """
#         This function splits the original train and test by saving in test only the 20% of each unique values of hardness
        
#         Parameters
#         ----------
#         df : DataFrame
#             Original dataframe with col hardness
#         col: string
#             Column to consier when splitting
#         p: integer
#             Percentage to save for each col unqiue values

#         Returns
#         -------
#         df_test : DataFrame
#             Test dataframe
#         df: DataFrame
#             Train dataframe
#         """
#         df_test = pd.DataFrame(columns=df.columns)
#         for val in df['hardness'].unique().tolist():
#             foo = df[df[col] == val]
#             n_rows = int(len(foo) * p / 100)
#             rows = foo.sample(n=n_rows)
#             df=df.drop(rows.index.tolist())
#             df_test = pd.concat([df_test, rows], ignore_index=True)
#         return df, df_test
    
#     def parse_vegaZero(vega_zero, masked= False):

#         """
#         This function masked the data to get only the vega zero structure
#         """
#         def replace_empty_values_with_zero(json_data):
#             if isinstance(json_data, dict):
#                 for key, value in json_data.items():
#                     json_data[key] = replace_empty_values_with_zero(value)
#             elif isinstance(json_data, list):
#                 json_data = [replace_empty_values_with_zero(item) for item in json_data]
#             else:
#                 if json_data != '[-]':
#                     json_data = '[*]'
#             return json_data
        
#         vega_zero = re.sub(r'\s+', ' ', vega_zero) # tolgo possibili spazi multipli
        
#         parsed_vegaZero = Metrics.vegazero

        
#         vega_zero_keywords = vega_zero.split(' ')

#         try:
#             parsed_vegaZero['mark'] = vega_zero_keywords[vega_zero_keywords.index('mark') + 1]
#         except Exception as e:
#             parsed_vegaZero['mark'] = '[-]'

#         try:
#             parsed_vegaZero['data'] = vega_zero_keywords[vega_zero_keywords.index('data') + 1]
#         except Exception as e:
#             parsed_vegaZero['data'] = '[-]'

#         try:
#             assert ((vega_zero_keywords.index('x') + 1) == 6 and vega_zero_keywords[vega_zero_keywords.index('encoding')] == "encoding")
#             parsed_vegaZero['encoding']['x'] = vega_zero_keywords[vega_zero_keywords.index('x') + 1]
#         except Exception as e:
#             parsed_vegaZero['encoding']['x'] = '[-]'
        
#         try:
#             assert ((vega_zero_keywords.index('aggregate') ) == 8)
#             parsed_vegaZero['encoding']['y']['aggregate'] = vega_zero_keywords[vega_zero_keywords.index('aggregate') + 1]
#         except Exception as e:
#             parsed_vegaZero['encoding']['y']['aggregate'] = '[-]'

#         try:
#             assert ((vega_zero_keywords.index('y') ) == 7)
#             parsed_vegaZero['encoding']['y']['y'] = vega_zero_keywords[vega_zero_keywords.index('aggregate') + 2]
#         except Exception as e:
#             parsed_vegaZero['encoding']['y']['y'] = '[-]'
        

#         if ('color' in vega_zero_keywords):
#             parsed_vegaZero['encoding']['color']['z'] = vega_zero_keywords[vega_zero_keywords.index('color') + 1]

#         if 'topk' in vega_zero_keywords:
#             parsed_vegaZero['transform']['topk'] = vega_zero_keywords[vega_zero_keywords.index('topk') + 1]

#         if 'sort' in vega_zero_keywords:
#             parsed_vegaZero['transform']['sort']['axis'] = vega_zero_keywords[vega_zero_keywords.index('sort') + 1]
#             parsed_vegaZero['transform']['sort']['type'] = vega_zero_keywords[vega_zero_keywords.index('sort') + 2]

#         if 'group' in vega_zero_keywords:
#             parsed_vegaZero['transform']['group'] = vega_zero_keywords[vega_zero_keywords.index('group') + 1]

#         if 'bin' in vega_zero_keywords:
#             parsed_vegaZero['transform']['bin']['axis'] = vega_zero_keywords[vega_zero_keywords.index('bin') + 1]
#             parsed_vegaZero['transform']['bin']['type'] = vega_zero_keywords[vega_zero_keywords.index('bin') + 3]

#         if 'filter' in vega_zero_keywords:

#             filter_part_token = []
#             for each in vega_zero_keywords[vega_zero_keywords.index('filter') + 1:]:
#                 if each not in ['group', 'bin', 'sort', 'topk']:
#                     filter_part_token.append(each)
#                 else:
#                     break

#             if 'between' in filter_part_token:
#                 filter_part_token[filter_part_token.index('between') + 2] = 'and ' + filter_part_token[
#                     filter_part_token.index('between') - 1] + ' <='
#                 filter_part_token[filter_part_token.index('between')] = '>='

#             # replace 'and' -- 'or'
#             filter_part_token = ' '.join(filter_part_token).split()
#             filter_part_token = ['&' if x == 'and' else x for x in filter_part_token]
#             filter_part_token = ['|' if x == 'or' else x for x in filter_part_token]

#             if '&' in filter_part_token or '|' in filter_part_token:
#                 final_filter_part = ''
#                 each_conditions = []
#                 for i in range(len(filter_part_token)):
#                     each = filter_part_token[i]
#                     if each != '&' and each != '|':
#                         # ’=‘ in SQL --to--> ’==‘ in Vega-Lite
#                         if each == '=':
#                             each = '=='
#                         each_conditions.append(each)
#                     if each == '&' or each == '|' or i == len(filter_part_token) - 1:
#                         # each = '&' or '|'
#                         if 'like' == each_conditions[1]:
#                             # only consider this case: '%a%'
#                             if each_conditions[2][1] == '%' and each_conditions[2][len(each_conditions[2]) - 2] == '%':
#                                 final_filter_part += 'indexof(' + 'datum.' + each_conditions[0] + ',"' + \
#                                                      each_conditions[2][2:len(each_conditions[2]) - 2] + '") != -1'
#                         elif 'like' == each_conditions[2] and 'not' == each_conditions[1]:

#                             if each_conditions[3][1] == '%' and each_conditions[3][len(each_conditions[3]) - 2] == '%':
#                                 final_filter_part += 'indexof(' + 'datum.' + each_conditions[0] + ',"' + \
#                                                      each_conditions[3][2:len(each_conditions[3]) - 2] + '") == -1'
#                         else:
#                             final_filter_part += 'datum.' + ' '.join(each_conditions)

#                         if i != len(filter_part_token) - 1:
#                             final_filter_part += ' ' + each + ' '
#                         each_conditions = []

#                 parsed_vegaZero['transform']['filter'] = final_filter_part

#             else:
#                 # only single filter condition
#                 parsed_vegaZero['transform']['filter'] = 'datum.' + ' '.join(filter_part_token).strip()
        
#         if(masked):
#             return replace_empty_values_with_zero(parsed_vegaZero)

#         return parsed_vegaZero

#     def to_VegaLite(vega_zero, dataframe=None):
#         VegaLiteSpec = {
#             'bar': {
#                 "mark": "bar",
#                 "encoding": {
#                     "x": {"field": "x", "type": "nominal"},
#                     "y": {"field": "y", "type": "quantitative"}
#                 }
#             },
#             'arc': {
#                 "mark": "arc",
#                 "encoding": {
#                     "color": {"field": "x", "type": "nominal"},
#                     "theta": {"field": "y", "type": "quantitative"}
#                 }
#             },
#             'line': {
#                 "mark": "line",
#                 "encoding": {
#                     "x": {"field": "x", "type": "nominal"},
#                     "y": {"field": "y", "type": "quantitative"}
#                 }
#             },
#             'point': {
#                 "mark": "point",
#                 "encoding": {
#                     "x": {"field": "x", "type": "quantitative"},
#                     "y": {"field": "y", "type": "quantitative"}
#                 }
#             }
#         }

#         VegaZero = VegaZero.parse_vegaZero(vega_zero)

#         # assign some vega-zero keywords to the VegaLiteSpec object
#         if isinstance(dataframe, pd.core.frame.DataFrame):
#             VegaLiteSpec[VegaZero['mark']]['data'] = dict()
#             VegaLiteSpec[VegaZero['mark']]['data']['values'] = json.loads(dataframe.to_json(orient='records'))

#         if VegaZero['mark'] != 'arc':
#             VegaLiteSpec[VegaZero['mark']]['encoding']['x']['field'] = VegaZero['encoding']['x']
#             VegaLiteSpec[VegaZero['mark']]['encoding']['y']['field'] = VegaZero['encoding']['y']['y']
#             if VegaZero['encoding']['y']['aggregate'] != '' and VegaZero['encoding']['y']['aggregate'] != 'none':
#                 VegaLiteSpec[VegaZero['mark']]['encoding']['y']['aggregate'] = VegaZero['encoding']['y']['aggregate']
#         else:
#             VegaLiteSpec[VegaZero['mark']]['encoding']['color']['field'] = VegaZero['encoding']['x']
#             VegaLiteSpec[VegaZero['mark']]['encoding']['theta']['field'] = VegaZero['encoding']['y']['y']
#             if VegaZero['encoding']['y']['aggregate'] != '' and VegaZero['encoding']['y']['aggregate'] != 'none':
#                 VegaLiteSpec[VegaZero['mark']]['encoding']['theta']['aggregate'] = VegaZero['encoding']['y'][
#                     'aggregate']

#         if VegaZero['encoding']['color']['z'] != '':
#             VegaLiteSpec[VegaZero['mark']]['encoding']['color'] = {
#                 'field': VegaZero['encoding']['color']['z'], 'type': 'nominal'
#             }

#         # it seems that the group will be performed by VegaLite defaultly, in our cases.
#         if VegaZero['transform']['group'] != '':
#             pass

#         if VegaZero['transform']['bin']['axis'] != '':
#             if VegaZero['transform']['bin']['axis'] == 'x':
#                 VegaLiteSpec[VegaZero['mark']]['encoding']['x']['type'] = 'temporal'
#                 if VegaZero['transform']['bin']['type'] in ['date', 'year', 'week', 'month']:
#                     VegaLiteSpec[VegaZero['mark']]['encoding']['x']['timeUnit'] = VegaZero['transform']['bin']['type']
#                 elif VegaZero['transform']['bin']['type'] == 'weekday':
#                     VegaLiteSpec[VegaZero['mark']]['encoding']['x']['timeUnit'] = 'week'
#                 else:
#                     print('Unknown binning step.')

#         if VegaZero['transform']['filter'] != '':
#             if 'transform' not in VegaLiteSpec[VegaZero['mark']]:
#                 VegaLiteSpec[VegaZero['mark']]['transform'] = [{
#                     "filter": VegaZero['transform']['filter']
#                 }]
#             elif 'filter' not in VegaLiteSpec[VegaZero['mark']]['transform']:
#                 VegaLiteSpec[VegaZero['mark']]['transform'].append({
#                     "filter": VegaZero['transform']['filter']
#                 })
#             else:
#                 VegaLiteSpec[VegaZero['mark']]['transform']['filter'] += ' & ' + VegaZero['transform']['filter']

#         if VegaZero['transform']['topk'] != '':
#             if VegaZero['transform']['sort']['axis'] == 'x':
#                 sort_field = VegaZero['encoding']['x']
#             elif VegaZero['transform']['sort']['axis'] == 'y':
#                 sort_field = VegaZero['encoding']['y']['y']
#             else:
#                 print('Unknown sorting field: ', VegaZero['transform']['sort']['axis'])
#                 sort_field = VegaZero['transform']['sort']['axis']
#             if VegaZero['transform']['sort']['type'] == 'desc':
#                 sort_order = 'descending'
#             else:
#                 sort_order = 'ascending'
#             if 'transform' in VegaLiteSpec[VegaZero['mark']]:
#                 current_filter = VegaLiteSpec[VegaZero['mark']]['transform'][0]['filter']
#                 VegaLiteSpec[VegaZero['mark']]['transform'][0][
#                     'filter'] = current_filter + ' & ' + "datum.rank <= " + str(VegaZero['transform']['topk'])
#                 VegaLiteSpec[VegaZero['mark']]['transform'].insert(0, {
#                     "window": [{
#                         "field": sort_field,
#                         "op": "dense_rank",
#                         "as": "rank"
#                     }],
#                     "sort": [{"field": sort_field, "order": sort_order}]
#                 })
#             else:
#                 VegaLiteSpec[VegaZero['mark']]['transform'] = [
#                     {
#                         "window": [{
#                             "field": sort_field,
#                             "op": "dense_rank",
#                             "as": "rank"
#                         }],
#                         "sort": [{"field": sort_field, "order": sort_order}]
#                     },
#                     {
#                         "filter": "datum.rank <= " + str(VegaZero['transform']['topk'])
#                     }
#                 ]

#         if VegaZero['transform']['sort']['axis'] != '':
#             if VegaZero['transform']['sort']['axis'] == 'x':
#                 if VegaZero['transform']['sort']['type'] == 'desc':
#                     VegaLiteSpec[VegaZero['mark']]['encoding']['y']['sort'] = '-x'
#                 else:
#                     VegaLiteSpec[VegaZero['mark']]['encoding']['y']['sort'] = 'x'
#             else:
#                 if VegaZero['transform']['sort']['type'] == 'desc':
#                     VegaLiteSpec[VegaZero['mark']]['encoding']['x']['sort'] = '-y'
#                 else:
#                     VegaLiteSpec[VegaZero['mark']]['encoding']['x']['sort'] = 'y'

#         return VegaLiteSpec[VegaZero['mark']]
    
# class Metrics():

#     marks_rules = {
#             'scatter':{
#                 'x': ['quantitative'],
#                 'y': ['quantitative'],
#             },
#             'line':{
#                 'x': ['temporal'],
#                 'y': ['quantitative'],
#             },
#             'strip':{
#                 'x': ['quantitative', 'nominal', 'ordinal'],
#                 'y': ['quantitative', 'nominal', 'ordinal', 'temporal'],
#             } ,
#             'histogram':{
#                 'x': ['quantitative', 'nominal', 'ordinal'],
#                 'y': ['quantitative', 'nominal', 'ordinal', 'temporal'],
#             },
#             'bar':{
#                 'x': ['quantitative', 'nominal', 'ordinal'],
#                 'y': ['quantitative', 'nominal', 'ordinal', 'temporal'],
#             }
#     }

#     vegazero = {
#                     'mark': '[*]',
#                     'data': '[*]',
#                     'encoding': {
#                         'x': '[*]',
#                         'y': {
#                             'aggregate': '[*]',
#                             'y': '[*]'
#                         },
#                         'color': {
#                             'z': '[*]'
#                         }
#                     },
#                     'transform': {
#                         'filter': '[*]',
#                         'group': '[*]',
#                         'bin': {
#                             'axis': '[*]',
#                             'type': '[*]'
#                         },
#                         'sort': {
#                             'axis': '[*]',
#                             'type': '[*]'
#                         },
#                         'topk': '[*]'
#                     }
#                 }

#     def __init__():
#         pass 

    
#     #Reimplementata Archived
#     """def vega_zero_integrity_score(vegazero):
#         grammar_groundtruth = Metrics.vegazero

#         preidcted_grammar = VegaZero.parse_vegaZero(vegazero, True)
        

#         doc1 = json.dumps(grammar_groundtruth, sort_keys=True)
#         doc2 = json.dumps(preidcted_grammar, sort_keys=True)
#         pattern = r'[{},":;]'

#         doc1 = re.sub(pattern, "", doc1)
#         doc2 = re.sub(pattern, "", doc2)
        
#         # List the unique words in a document
#         words_doc1 = set(doc1.lower().split(" ")) 
#         words_doc2 = set(doc2.lower().split(" "))
        
#         # Find the intersection of words list of doc1 & doc2
#         intersection = words_doc1.intersection(words_doc2)

#         # Find the union of words list of doc1 & doc2
#         union = words_doc1.union(words_doc2)
            
#         # Calculate Jaccard similarity score 
#         # using length of intersection set divided by length of union set
#         return float(len(intersection)) / len(union)
#         # print(grammar_groundtruth)
#     """

#     """
#     Reimplementata Archived
#     """
#     # def attribute_integrity_score(predicted, groundtruth):
#     #     predicted_fileds = VegaZero.parse_vegaZero(predicted)
#     #     groundtruth_fileds = VegaZero.parse_vegaZero(groundtruth)
        
#     #     score = 0
#     #     if(predicted_fileds['encoding']['x'] == groundtruth_fileds['encoding']['x']):
#     #         score +=0.5
        
#     #     if(predicted_fileds['encoding']['y']['y'] == groundtruth_fileds['encoding']['y']['y']):
#     #         score +=0.5
        
#     #     return score
            
    
#     #reimplementata usando DRACO soft constraints e hard
#     """def visualization_integreity(predicted, groundtruth, dataset):

#         predicted_fileds = VegaZero.parse_vegaZero(predicted)
#         groundtruth_fileds = VegaZero.parse_vegaZero(groundtruth)

#         x_axes_pred = predicted_fileds['encoding']['x']
#         y_axes_pred = groundtruth_fileds['encoding']['y']['y']

#         mark = predicted_fileds['mark']

#         x_type = utils.get_attribute_type(x_axes_pred.lower(), dataset)
#         y_type = utils.get_attribute_type(y_axes_pred.lower(), dataset)

#         x_trype_mapped = utils.map_to_vis_domain(x_type[2], x_axes_pred)
#         y_trype_mapped = utils.map_to_vis_domain(y_type[2], y_axes_pred)

#         score = 0

#         if(x_trype_mapped in Metrics.marks_rules[mark]['x']):
#             score += 1
        
#         if(y_trype_mapped in Metrics.marks_rules[mark]['y']):
#             score += 1
        
#         return score - 1"""

#     """
#     Da ridefinere
#     """
    
#     def expliciteness_missed_score(query, vegazero):
#         vz_fields = VegaZero.parse_vegaZero(vegazero)
#         query = query.lower()
#         query = re.sub(' +', ' ', query)
#         query_splitted = query.split(" ")

#         score = 0
        
#         if (vz_fields['encoding']['x'] in query_splitted):
#             score += 1
        
#         if (vz_fields['encoding']['y']['y'] in query_splitted):
#             score += 1
        
#         if (vz_fields['mark'] in query_splitted):
#             score += 1
        
#         return score - 1