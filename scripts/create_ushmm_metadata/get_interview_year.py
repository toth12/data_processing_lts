import pprint
import pdb
import sys, os
import constants
import helper_mongo as h
pp = pprint.PrettyPrinter(indent=4)

# database info
DB = constants.DB
COLLECTION = constants.INPUT_COLLECTION_USHMM

def getInterviewYear():
    """
    Returns a dictionary with the interview_year of 1462 entries in
    the USHMM database
    """
    # query for interview years
    result = h.query(DB, COLLECTION, {'display_date': {'$exists': 'true'} }, {'display_date': 1, 'id': 1})
    
    # initialize dictionary
    interview_year = dict()

    # go through all the interviews
    for interview in result:
        key = interview.get('id')
        
        # access date object
        date = interview.get('display_date')[0]

        # strip the year
        year  = date[0:4]

        # add to dict if it is a valid year
        if year != '':
            interview_year[key] = int(year)
    return interview_year

if __name__ == "__main__":
    getInterviewYear()

