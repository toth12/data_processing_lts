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
    result = h.query(DB, COLLECTION, {}, {'interviewee_name': 1,'shelfmark':1,'collection':1} )

    df = pd.DataFrame(result)
    nan_value = float("NaN")
    df.replace("", nan_value, inplace=True)
    df.dropna(subset = ["interviewee_name"], inplace=True)
    df['shelfmark']=df['collection']+' '+df['shelfmark'].astype('string')
    df = df[df.interviewee_name.duplicated(keep=False)]
    df = df.groupby('interviewee_name')['shelfmark'].apply(list).reset_index(name='shelfmarks')
    df.to_csv(constants.OUTPUT_FOLDER_MISC+'interviewees_giving_more_interviews.csv')
    

if __name__ == '__main__':
    run()