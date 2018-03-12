import pprint
import pdb
import sys, os
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h
pp = pprint.PrettyPrinter(indent=4)

def getProvenance():
    """
    Returns a dictionary with the historical provenance of 1514 entries in
    the USHMM database
    """
    # query for interview years
    result = h.query('Hol', 'undress_experiment', {}, {'historical_provenance': 1, 'id': 1})
    
    # initialize dictionary
    interviews_provenances = dict()

    # go through all the interviews
    for interview in result:
        # get keys
        key = interview.get('id')
        provenance = interview.get('historical_provenance')

        # get first element (it is always an one-element array)
        interviews_provenances[key] = provenance[0]
                
    return interviews_provenances

if __name__ == "__main__":
    getProvenance()

