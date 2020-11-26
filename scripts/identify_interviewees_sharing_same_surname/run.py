# -*- coding: utf-8 -*-

import sys, os
import constants
import pdb
from utils import helper_mongo as h
import pprint
import pandas as pd
pd.set_option('display.max_rows', 10)
import numpy as np
import sklearn.cluster
import distance
import editdistance
import urllib

DB = constants.OUTPUT_DB
COLLECTION = 'testimonies'


def run():
    # get the relevant metadata
    result = h.query(DB, COLLECTION, {}, {'interviewee_name': 1,'shelfmark':1,'collection':1} )

    
    df = pd.DataFrame(result)
    df = df.drop(columns=['_id'])
    df = df.drop_duplicates(subset=['interviewee_name'],keep=False)
    df = df[df.collection!='Fortunoff']

    nan_value = float("NaN")

    df.replace("", nan_value, inplace=True)

    df.dropna(subset = ["interviewee_name"], inplace=True)
    df['surname'] = df.interviewee_name.apply(lambda x: x.split()[-1])
    filter = df['surname'].str.contains('\.') 
    df = df[~filter]
    df = df.groupby('surname').filter(lambda x: len(x) > 2).groupby('surname')['interviewee_name'].apply(list).reset_index(name='interviewee_names')
    df['interviewee_names'] = df.interviewee_names.apply(lambda x: ','.join(x))
    df.to_csv(constants.OUTPUT_FOLDER_MISC+'interviews_sharing_surnames.csv',encoding='utf-8')


    


    



    

if __name__ == '__main__':
    run()