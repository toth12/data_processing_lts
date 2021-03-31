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


from urllib2 import urlopen


import pdb
import re

DB = constants.OUTPUT_DB
COLLECTION = 'testimonies'

def getMetaData():
    # query database
    result = h.query(DB, COLLECTION, {'collection':'USHMM'}, {'media_url':1,'testimony_id':1,'shelfmark':1})
 
        
    return result


def run():
    
    result = []
    base_url = 'https://oralhistory-assets.ushmm.org/'

    data = getMetaData()
    data = [element for element in data if len(element['media_url'])==0]





    for f,element in enumerate(data):
        url = "https://collections.ushmm.org/search/catalog/"+element['testimony_id']
        shelfmark = element['shelfmark'].split(' ')[1]

        shelfmark = '.'.join(shelfmark.split('*'))
        print f
        try:
            fp = urlopen(url)
        except:
            print (url)
            continue
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        fp.close()
        urls_mp3 = re.findall(r"\.mp3'", mystr, re.DOTALL)
        urls_mp4 = re.findall(r"\.mp4'", mystr, re.DOTALL)
        if len(urls_mp3)>0:
            media_urls = []
            for i,media_type in enumerate(urls_mp3):
                media_url = base_url+shelfmark+'.0'+str(i+1)+'.0'+str(len(urls_mp3))+'.mp3'
                media_urls.append(media_url)
            result.append({'testimony_id':element['testimony_id'],'media_url':media_urls})

        elif len(urls_mp4)>0:
            media_urls = []
            for i,media_type in enumerate(urls_mp4):
                media_url = base_url+shelfmark+'.0'+str(i+1)+'.0'+str(len(urls_mp4))+'.mp4'
                media_urls.append(media_url)
            result.append({'testimony_id':element['testimony_id'],'media_url':media_urls})
    pd.DataFrame(result).to_csv("USHMM_media_urls.csv")
    pdb.set_trace()

    

if __name__ == "__main__":
    run()
    






   
    


pdb.set_trace()