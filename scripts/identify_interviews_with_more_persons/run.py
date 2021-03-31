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


def run():
    # get the relevant metadata
    result = h.query(DB, COLLECTION, {}, {'testimony_title': 1,'shelfmark':1,'collection':1} )

    result = [element for element in result if (('and' in element['testimony_title'].split()) or ( len(element['testimony_title'].split(','))>1))]
    df = pd.DataFrame(result)
    df = df.drop(columns=['_id'])
    df.to_csv(constants.OUTPUT_FOLDER_MISC+'interviews_with_multiple_interviewees.csv',encoding='utf-8')

    # modify the gender of these interviews
    for element in result:
        h.update_entry(DB,COLLECTION,element['_id'],{'gender':''})


    

if __name__ == '__main__':
    run()