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
import json 
import ast


DB = constants.OUTPUT_DB
COLLECTION = 'testimonies'


def run():
    file_name = 'USHMM_media_urls.csv'
    df = pd.read_csv(constants.INPUT_FOLDER_USHMM_METADATA+file_name)


    for row in df.iterrows():
        media_url = ast.literal_eval(row[1]['media_url']) 

        h.update_field(DB,COLLECTION,'testimony_id',row[1]['testimony_id'],'media_url',media_url)


    

if __name__ == '__main__':
    run()