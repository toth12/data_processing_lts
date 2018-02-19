import pprint
import pdb
import sys, os
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h
pp = pprint.PrettyPrinter(indent=4)

def getInterviewYear():
    """
    Returns a dictionary with the interview_year of 1462 entries in
    the USHMM database
    """
    # query for interview years
    result = h.query('Hol', 'undress_experiment', {'display_date': {'$exists': 'true'} }, {'display_date': 1, 'id': 1})
    
    # initialize dictionary
    interview_year = dict()

    for interview in result:
        key = interview.get('id')
        
        interview_year[key] = interview.get('display_date')
    

    return interview_year

