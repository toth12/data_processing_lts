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
    # query database
    result = h.query(DB, COLLECTION, {}, {field_name: 1,'id':1,'collection':1,'testimony_title':1})
   
        
    return result

if __name__ == "__main__":
    
    fields = ['shelfmark']
    for field in fields:
        result = getMetaData(field_name=field)
        df = pd.DataFrame(result)
        df = df.drop(columns="_id")
        df.to_csv(constants.OUTPUT_FOLDER_MISC+'all_interviews_with_titles_shelfmarks.csv',encoding='utf-8')