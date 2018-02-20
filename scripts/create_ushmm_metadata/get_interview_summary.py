import pprint
import pdb
import sys, os
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h

def getInterviewSummary():
    """
    Queries for interview_summary in the undress_experiment database
    Returns a dictionary with 1065 entries, the keys being the 'id' of the interview
    and the value being the interview summary
    """
    # query for interview summaries and initialize dictionary
    result = h.query('Hol', 'undress_experiment', {'interview_summary': {'$exists': 'true'}}, {'id': 1, 'interview_summary': 1})
    interview_summaries = dict()
    
    # iterate through each interview to find the gender
    for interview in result:
        
        # get interview summary and key
        summary = interview.get('interview_summary')
        key = interview.get('id')
        
        # add key to dictionary
        interview_summaries[key] = summary
    
    return interview_summaries


           
if __name__ == "__main__":
    getInterviewSummary()