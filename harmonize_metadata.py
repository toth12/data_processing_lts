import sys, os
import constants
import pdb
from utils import helper_mongo as h
import pprint
import pandas as pd


DB = constants.OUTPUT_DB
COLLECTION = 'testimonies'

def getMetaData(field_name):
    """
    Queries undress_experiment for subject_corporate.
    Returns a dictionary with 529 entries, the keys being the 'id' of the interview
    and the value being an array with the names of the camps
    Returns a set of interview IDs with all 1514 entries
    """
    # query database
    result = h.query(DB, COLLECTION, {}, {field_name: 1,'id':1} )
    output= []
    for interview in result:
        output.append(interview[field_name])

        
    return output

if __name__ == "__main__":
    
    fields = ['camp_names','ghetto_names']
    for field in fields:
        result = getMetaData(field_name=field)
        final_result = []
        [final_result.extend(element) for element in result if len(element)>0]
        df = pd.DataFrame(final_result)
        df = df.drop_duplicates().sort_values(0)
        pdb.set_trace()

        df.to_csv(field+'.csv',encoding='utf-8')
    pdb.set_trace()


