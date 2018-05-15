import pprint
import pdb
import sys, os
import constants
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h

pp = pprint.PrettyPrinter(indent=4)

# database info
DB = constants.DB
COLLECTION = constants.INPUT_COLLECTION_USHMM

def getGhettoNames():
    """
    Queries undress_experiment for subject_topical.
    Returns a dictionary with 529 entries, the keys being the 'id' of the interview
    and the value being an array with the names of the camps
    """
    # query for ghettos
    result = h.query(DB, COLLECTION, {}, {'subject_topical': 1,'id':1} )

    # initialize dictionary
    interview_mentioned_ghettos = dict()

    # check for ghetto names
    for interview in result:
        
        # get id of interview

        key = interview.get('id')
        # check if interview has a topical term
        if 'subject_topical' in interview: 

            # get array of possible ghettos
            subj_arr = interview.get('subject_topical')

            # initialize temp set that will store the names of unique ghettos
            known_ghettos = set([])

            # iterate over the array under 'subject_topical'
            for item in subj_arr:
                # check for pattern
                if 'ghetto' in item:

                    # e.g u'Jewish ghettos--Poland--Warsaw.'
                    item_parts = item.split('--')

                    # if ghetto name is available, e.g Warsaw, add it
                    if len(item_parts) > 2:
                        name = item_parts[2]

                        # remove '.' from name if it is the last character
                        if name[len(name) - 1] == '.':
                            name =  name.replace(name, name[:-1])

                        # add to temp aray
                        known_ghettos.add(name)

            # add ghetto_names, even if empty
            interview_mentioned_ghettos[key] = list(known_ghettos)

    
    return interview_mentioned_ghettos

                
if __name__ == "__main__":
    getGhettoNames()
