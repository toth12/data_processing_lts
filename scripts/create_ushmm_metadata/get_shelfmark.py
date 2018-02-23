import pprint
import pdb
import sys, os
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h
pp = pprint.PrettyPrinter(indent=4)

def getShelfmark():
    """
    Returns a dictionary with the interview_year of 1462 entries in
    the USHMM database
    """
    # query for interview years
    result = h.query('Hol', 'undress_experiment',  {}, {'rg_number': 1, 'id': 1})
    
    # initialize dictionary
    interviews_shelfmark = dict()

    # go through all the interviews
    for interview in result:
        key = interview.get('id')
        
        # access date object
        interviews_shelfmark[key] = interview.get('rg_number')

    pp.pprint(interviews_shelfmark)
    return interviews_shelfmark

if __name__ == "__main__":
    getShelfmark()

