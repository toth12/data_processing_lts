from pymongo import MongoClient
import pprint
import sys, glob, os
import constants
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h

DB = constants.DB
TRACKER = constants.TRACKER_COLLECTION

def createStructuredTranscript():
    # query for interview ids
    result = h.query(DB, TRACKER, {'status': 'not processed'}, {'id_':0} )
    print(len(result))

if __name__ == "__main__":
    createStructuredTranscript()