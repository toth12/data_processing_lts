import pprint
import pdb
import sys, os
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h

pp = pprint.PrettyPrinter(indent=4)

def getGhettoNames():
    """
    Queries undress_experiment for subject_topical.
    Returns a dictionary with 529 entries, the keys being the 'id' of the interview
    and the value being an array with the names of the camps
    """
    # query for ghettos
    result = h.query('Hol', 'undress_experiment', {}, {'subject_topical': 1,'id':1} )

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
                    # add to temp aray
                    known_ghettos.add(item)

            # if any ghetto was found, add to return dictionary
            if len(known_ghettos) != 0:
                interview_mentioned_ghettos[key] = known_ghettos

    pp.pprint(len(interview_mentioned_ghettos))
    return interview_mentioned_ghettos

                
if __name__ == "__main__":
    getGhettoNames()