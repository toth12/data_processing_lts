import pprint
import sys, os
import constants
import helper_mongo as h
pp = pprint.PrettyPrinter(indent=4)

# database info
DB = constants.DB
COLLECTION = constants.INPUT_COLLECTION_USHMM

def getShelfmark():
    """
    Returns a dictionary with the interview_year of 1462 entries in
    the USHMM database
    """
    # query for interview years
    result = h.query(DB, COLLECTION,  {}, {'rg_number': 1, 'id': 1})
    
    # initialize dictionary
    interviews_shelfmark = dict()

    # go through all the interviews
    for interview in result:
        key = interview.get('id')
        
        # access date object
        interviews_shelfmark[key] = 'USHMM '+interview.get('rg_number')

    return interviews_shelfmark

if __name__ == "__main__":
    getShelfmark()

