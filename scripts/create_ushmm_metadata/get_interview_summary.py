import pprint
import pdb
import sys, os
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h

# 1065
def getInterviewSummary():

    # query for interview summaries
    result = h.query('Hol', 'undress_experiment', {'interview_summary': {'$exists': 'true'}}, {'id': 1, 'interview_summary': 1})

    interview_summaries = dict()
    
    # iterate through each interview to find the gender
    for interview in result:
        
        # get interview summary and key
        summary = interview.get('interview_summary')
        key = interview.get('id')

        interview_summaries[key] = summary
    
    return interview_summaries


           
if __name__ == "__main__":
    getInterviewSummary()