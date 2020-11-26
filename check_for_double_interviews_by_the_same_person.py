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
    result = h.query(DB, COLLECTION, {}, {field_name: 1,'id':1,'collection':1,'testimony_id':1,'shelfmark':1} )
    output= []
    for interview in result:
        if interview['interviewee_name']!='':
            output.append({field_name:interview[field_name],'collection':interview['collection'],'shelfmark':interview['shelfmark']})

        
    return output

if __name__ == "__main__":
    
    fields = ['ghetto_names','camp_names']
    fields = ['interviewee_name']
    for field in fields:
        result = getMetaData(field_name=field)
        '''
        names = [element['interviewee_name'] for element in result if element['collection']!="Fortunoff"]
        groups = []
        print "close variants"
        for element in names:
            if element== '':
                    continue
            group = [element]
            for name in names:
                if name == '':
                    continue
                dist= editdistance.eval(element,name)

                #exclude the possibility that the shared first name gives rise to similarity
                dist_first_name =editdistance.eval(element.split()[0],name.split()[0])
                dist_last_name =editdistance.eval(element.split()[-1:],name.split()[-1:])

                if (dist <3) and (dist>0):
                    if dist_first_name>0:
                        if dist_last_name<3:
                            group.append(name)
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

        '''

        df = pd.DataFrame(result)
        df['shelfmark']=df['collection']+' '+df['shelfmark']
        df = df[df.interviewee_name.duplicated(keep=False)]
        df = df.groupby('interviewee_name')['shelfmark'].apply(list).reset_index(name='shelfmarks')

        pdb.set_trace()




