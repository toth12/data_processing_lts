from pymongo import MongoClient
import pprint
import sys, glob, os
import constants
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h

pp = pprint.PrettyPrinter(indent=4)
DB = constants.DB
TRACKER = constants.TRACKER_COLLECTION
OUTPUT = constants.OUTPUT_COLLECTION

def checkProgress():
    # query for interview ids
    result = h.query(DB, TRACKER, {'extraction_method': 'transcribe_non_core_doc'}, {'id_':0} )

    for item in result:
        irn = item.get('id')

        # get units for this one
        q = h.query(DB, OUTPUT, {'testimony_id': irn}, {'id_': 0})

        pp.pprint(q)
        #item.
   # pp.pprint(result)

if __name__ == "__main__":
    checkProgress()