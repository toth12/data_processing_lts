import pprint
import pdb
import sys, os
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h
pp = pprint.PrettyPrinter(indent=4)

def getInterviewTitle():
    """
    Returns a dictionary with the title of all 1514 entries in
    the undress_experiment database
    """

     # query for interview years
    result = h.query('Hol', 'undress_experiment', {'title': {'$exists': 'true'} }, {'title': 1, 'id': 1})
    
    # initialize dictionary
    interview_titles = dict()

    # go over all the rows, extract title and store it in dictionary
    for interview in result:
        key = interview.get('id')
        title = interview.get('title')
        interview_titles[key] = title

    return interview_titles


if __name__ == "__main__":
    getInterviewTitle()