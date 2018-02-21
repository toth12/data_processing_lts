import pprint
import pdb
import sys, os
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h
pp = pprint.PrettyPrinter(indent=4)

def getIntervieweeName():
    """
    Returns a dictionary with the names of 1503 entries total, 1302 entries directly from the
    the undress_experiment database's interviewee firled, and 201 with the backup method
    """

     # query for interview years
    result = h.query('Hol', 'undress_experiment', {}, {'interviewee': 1, 'id': 1, 'interview_summary': 1})
    
    # initialize dictionary
    interviewee_names = dict()

    # go over all the rows, extract title and store it in dictionary
    for interview in result:
        key = interview.get('id')
        name = interview.get('interviewee')
        if name is not None:
            interviewee_names[key] = name

        # backup method in case interviewee name was not registered
        else:
            summary = interview.get('interview_summary')

            # summaries always begin with the name of the interviewee
            if summary is not None:
                name_backup = ""
                whitespace_count = 0
                
                # iterate through the summary to get the name - use whitespace as proxy
                for i in range(len(summary)):
                    
                    if summary[i] == ",":
                        break
                    elif summary[i] == ' ':
                        if summary != "Dr.":
                            whitespace_count += 1
                        if whitespace_count == 2:
                            break

                    # else, just add character to backup name
                    name_backup += summary[i]
                
                interviewee_names[key] = name_backup

    return interviewee_names


if __name__ == "__main__":
    getIntervieweeName()