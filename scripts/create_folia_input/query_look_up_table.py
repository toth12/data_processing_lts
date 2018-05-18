import sys
import os
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h
import pdb
import json

results=h.query('let_them_speak_data_processing', 'output_ushmm_metadata', {'look_up_table':{'$exists':True}}, {'unique_id':1,'look_up_table':1} )
query={result['unique_id']:json.loads(result['look_up_table']) for result in results}

pdb.set_trace()
