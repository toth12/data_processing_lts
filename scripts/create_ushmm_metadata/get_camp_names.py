import sys, os
import constants
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import pdb
import helper_mongo as h


DB = constants.DB
COLLECTION = constants.INPUT_COLLECTION

def getCampNames():
    """
    Queries undress_experiment for subject_corporate.
    Returns a dictionary with 529 entries, the keys being the 'id' of the interview
    and the value being an array with the names of the camps
    Returns a set of interview IDs with all 1514 entries
    """
    # query database
    result = h.query(DB, COLLECTION, {}, {'subject_corporate': 1,'id':1} )

    # initialize variables
    unknown_camps = []
    interview_known_camps = dict()

    # check for camps in subject_corporate
    for interview in result:
        # retrieve object key
        mongo_key = interview.get('_id')

        # get id of interview
        key = interview.get('id')

        # check for subject_corporate key
        if 'subject_corporate' in interview:
            
            # get array of possible camps
            subj_arr = interview.get('subject_corporate')
            known_camps = set([])

            # iterate through subjects array and check for (Concentration camp)
            for item in subj_arr:

                # check if it is a camp entry
                if '(Concentration camp)' in item:
                    
                    camp_name = ""
                    # split string items into tokens
                    words = item.split()
                    
                    # get camp_name
                    for i in range(len(words)):
                        if words[i] != '(Concentration':
                            if i != 0:
                                camp_name += ' '
                            camp_name += words[i]
                        else:
                            break
                    
                    # add camp_name
                    known_camps.add(camp_name)
            
            # create entry for that interview if there were any camps
            interview_known_camps[key] = list(known_camps)

            # else, add the mongo objectId to the list of unkown camps  
            if len(known_camps) == 0:
                unknown_camps.append(mongo_key)
        else:
            # keep track of camps without the subject corporate field
            unknown_camps.append(mongo_key)
    
    
    return interview_known_camps

if __name__ == "__main__":
    getCampNames()