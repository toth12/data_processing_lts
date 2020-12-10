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
    result = h.query(DB, COLLECTION, {}, {'testimony_title':1,'recording_year': 1,'shelfmark':1,'collection':1} )
    df = pd.DataFrame(result)
    df = df.drop(columns=['_id'])
    nan_value = float("NaN")
    df.replace("", nan_value, inplace=True)
    df = df[~df['recording_year'].notna()]
    df.replace(nan_value,"", inplace=True)
    df.drop(columns =["recording_year"], inplace=True)
    df.reset_index(drop=True,inplace=True)
    df.to_csv(constants.OUTPUT_FOLDER_MISC+'interviews_without_recording_year.csv',encoding='utf-8')

if __name__ == '__main__':
    run()