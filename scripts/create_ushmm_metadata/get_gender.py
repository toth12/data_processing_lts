import pprint
import pdb
import sys, os
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h
from pymongo import MongoClient


pp = pprint.PrettyPrinter(indent=4)
import ast
from bson.objectid import ObjectId

def getGender():

    
    result = h.query('Hol', 'undress_experiment', {'id': 'irn36918'}, {'_id': 0})
     # query for ghettos
    #result = h.query('Hol', 'undress_experiment', {}, {} )
    #result = h.query('Hol', 'undress')
    pp.pprint(result)


           
if __name__ == "__main__":
    getGender()