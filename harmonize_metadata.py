# -*- coding: utf-8 -*-

import sys, os
import constants
import pdb
from utils import helper_mongo as h
import pprint
import pandas as pd
pd.set_option('display.max_rows', 500)
import numpy as np
import sklearn.cluster
import distance
import editdistance
import urllib

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
    result = h.query(DB, COLLECTION, {}, {field_name: 1,'id':1,'collection':1} )
    output= []
    for interview in result:
        output.append({'field':interview[field_name],'collection':interview['collection']})

        
    return output

if __name__ == "__main__":
    
    fields = ['ghetto_names','camp_names']
    fields = ['camp_names']
    for field in fields:
        result = getMetaData(field_name=field)

        #final_result = []
        #[final_result.extend(element) for element in result if len(element)>0]
        output = set()
        df = pd.DataFrame(result)

        for element in df.field.to_list():
            for city in element:
                output.add(city)

        for element in sorted(output):
            print element

            #text = "Dvar\xc4\x97ts (Hrodzenskaia voblasts')"
            #if text in element:
                #pdb.set_trace()
            #code=urllib.urlopen("https://en.wikipedia.org/wiki/"+element).getcode()
            #if code == 404:
             #   continue

        pdb.set_trace()
        df['Lo_1']=df['field'].apply(lambda x: True if 'Łódź' in x else False)
        df['Lo_2']=df['field'].apply(lambda x: True if 'Łódź' in x else False)

        print (df[df['Lo_1']==True])
        print(df[df['Lo_2']==True])
        
        df = df.drop_duplicates().sort_values(0)
        print df.reindex()
        pdb.set_trace()


        words = df[0].to_list()#So that indexing with a list will work
        groups = []
        for element in words:
            group = [element]
            for word in words:
                dist= editdistance.eval(element,word)
                if (dist <3) and (dist>0):
                    group.append(word)
            if len(group)>1:
                group.sort()
                groups.append(group)
        groups = set(tuple(x) for x in groups)

        for group in groups:
            print '\n'
            res = '|'.join(group)
            print res
            print '\n'
        print '-'*10


        words_with_dash_second_element = [word.split('-')[1] for word in words if '-' in word]

        for w in words_with_dash_second_element:
            if w in words:
                print w
        print '-'*10
        words_with_dash_first_element = [word.split('-')[0] for word in words if '-' in word]

        for w in words_with_dash_first_element:
            if w in words:
                print w


        pdb.set_trace()




