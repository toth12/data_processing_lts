import pdb
import os
import json
import sys
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h


#get the id of those documents that has a structured_transcript field does not exist

if __name__ == "__main__":
    results=h.query('let_them_speak_data_processing', 'output_ushmm_metadata', {'structured_transcript':{'$exists':False}}, {'interview_id':1})
    pdb.set_trace()

    #update them with the sample input

    with open('sample_input.json') as json_data:
        sample_data = json.load(json_data)

    for result in results:
        h.update_field('let_them_speak_data_processing', 'output_ushmm_metadata', "interview_id", result['interview_id'], "structured_transcript", sample_data)
