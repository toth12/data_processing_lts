import pprint
import pdb
import sys, os
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h
import concurrent.futures


# declare some constants
MALE = "Male"
FEMALE = "Female"
COUPLE = "Couple"
NO_GENDER = 0

# array of common pronouns that give away the interviewee's gender
MALE_WORDS = [' his ', 'His ', ' him ', 'He ', ' he ']
FEMALE_WORDS = [' her ','Her ', ' she ', 'She ']


#TODO deal with couples
def getGenderHelper(interview):
    '''
    Counts the number of occurences of common pronouns that give away the interviewee's
    gender. 
    Returns the gender of the interviewee based on the number of 
    ''' 
    # get interview summary
    summary = interview.get('interview_summary')
    male_counter = 0
    female_counter = 0

    # initialize counter variables
    male_counter = 0
    female_counter = 0

    # get total count of the occurrences of male and female pronouns, respectively
    for i in range(len(MALE_WORDS)):
        male_counter += summary.count(MALE_WORDS[i])
    
    for i in range(len(FEMALE_WORDS)):
        female_counter += summary.count(FEMALE_WORDS[i])
    
    # in case there was no cue in the summary
    if male_counter == 0 and female_counter == 0:
        return NO_GENDER

    # else return appropriate gender based on coutner
    elif male_counter > female_counter:
        return MALE
    else:
        return FEMALE

def getGender():
    """
    Returns a dictionary with the id of the interview as the key,
    and the gender of the interviewee as the value
    """
    # initialize dictionary
    interviewees_gender = dict()

    # Create a pool of processes. By default, one is created for each CPU in your machine.
    with concurrent.futures.ProcessPoolExecutor() as executor:
        
        # query for interview summaries
        result = h.query('Hol', 'undress_experiment', {'interview_summary': {'$exists': 'true'}}, {'id': 1, 'interview_summary': 1})
        
        # execute calls asynchronously
        for interview, gender in zip(result, executor.map(getGenderHelper, result)):

            # add known genders to the dictionary
            if gender != NO_GENDER:
                key = interview.get('id')
                interviewees_gender[key] = gender
    
    return interviewees_gender
        
if __name__ == "__main__":
    getGender()
