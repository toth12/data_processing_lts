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
    result = h.query(DB, COLLECTION, {}, {'gender': 1,'shelfmark':1,'collection':1,'testimony_title':1} )
    df = pd.DataFrame(result)
    df = df.drop(columns=['_id'])
    nan_value = float("NaN")
    df.gender = df.gender.apply(lambda y: np.nan if len(y)==0 else y)
    df_no_gender = df[~df['gender'].notna()]
    df_no_gender = df_no_gender.drop(columns=['gender'])
    df_no_gender.to_csv(constants.OUTPUT_FOLDER_MISC+'interviews_without_gender_info.csv',encoding='utf-8')


if __name__ == '__main__':
    run()