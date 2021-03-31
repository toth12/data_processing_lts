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
    result = h.query(DB, COLLECTION, {}, {'shelfmark':1,'collection':1} )
    # modify the shelfmark of interviews
    for element in result:
        if element ['collection'] !="USHMM":
            h.update_entry(DB,COLLECTION,element['_id'],{'shelfmark':element['collection']+' '+str(element['shelfmark'])})



if __name__ == '__main__':
    run()