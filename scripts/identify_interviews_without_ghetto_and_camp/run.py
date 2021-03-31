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
    result = h.query(DB, COLLECTION, {}, {'ghetto_names':1,'camp_names': 1,'shelfmark':1,'collection':1,'testimony_title':1} )
    df = pd.DataFrame(result)
    df = df.drop(columns=['_id'])
    nan_value = float("NaN")
    df.ghetto_names = df.ghetto_names.apply(lambda y: np.nan if len(y)==0 else y)
    df.camp_names = df.camp_names.apply(lambda y: np.nan if len(y)==0 else y)
    df_no_camps = df[~df['camp_names'].notna()]
    df_no_ghettos = df[~df['ghetto_names'].notna()]

    df_no_camps.replace(nan_value,"", inplace=True)
    df_no_camps.reset_index(drop=True,inplace=True)
    df_no_camps = df_no_camps.drop(columns=['ghetto_names','camp_names'])
    df_no_camps.to_csv(constants.OUTPUT_FOLDER_MISC+'interviews_without_camps.csv',encoding='utf-8')
    


    df_no_ghettos.replace(nan_value,"", inplace=True)
    df_no_ghettos.reset_index(drop=True,inplace=True)
    df_no_ghettos = df_no_ghettos.drop(columns=['ghetto_names','camp_names'])
    df_no_ghettos.to_csv(constants.OUTPUT_FOLDER_MISC+'interviews_without_ghettos.csv',encoding='utf-8')

if __name__ == '__main__':
    run()