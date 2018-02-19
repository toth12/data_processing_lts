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
NO_GENDER = 0

# array of common pronouns that give away the interviewee's gender
MALE_WORDS = [' his ', 'His ', ' him ', 'He ', ' he ']
FEMALE_WORDS = [' her ','Her ', ' she ', 'She ']


#TODO deal with couples
def getGenderHelper(interview):
       
    # get interview summary
    summary = interview.get('interview_summary')
    male_counter = 0
    female_counter = 0
    if summary is  None:
        return NO_GENDER 
    elif summary is not None:
        male_counter = 0
        female_counter = 0
        # get count of use of his and her
        for i in range(len(MALE_WORDS)):
         
            male_counter += summary.count(MALE_WORDS[i])
        
        for i in range(len(FEMALE_WORDS)):
            female_counter += summary.count(FEMALE_WORDS[i])
    
    if male_counter == 0 and female_counter == 0:
        return NO_GENDER
    elif male_counter > female_counter:
        return MALE
    else:
        return FEMALE

def getGender():
    # initialize dictionary
    interviewees_gender = dict()
    # Create a pool of processes. By default, one is created for each CPU in your machine.
    with concurrent.futures.ProcessPoolExecutor() as executor:
        
        # query for interview summaries
        result = h.query('Hol', 'undress_experiment', {'interview_summary': {'$exists': 'true'}}, {'id': 1, 'interview_summary': 1})
        
        for interview, gender in zip(result, executor.map(getGenderHelper, result)):
            # add known genders to the dictionary
            if gender != NO_GENDER:
                key = interview.get('id')
                interviewees_gender[key] = gender
        
    return interviewees_gender
        
        
            

  

if __name__ == "__main__":
    getGender()
