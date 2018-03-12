import pprint
import pdb
import sys, os
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h
import concurrent.futures
# Python 2.7
import urllib2
import json
import unicodedata
import requests



# declare some constants
MALE = "male"
FEMALE = "female"
COUPLE = "couple"
NO_GENDER = 0

# array of common pronouns that give away the interviewee's gender
MALE_WORDS = [' his ', 'His ', ' him ', 'He ', ' he ']
FEMALE_WORDS = [' her ','Her ', ' she ', 'She ']
TITLES_PREFIXES = ['Ms.', "Mr.", "Dr.", "Mrs."]

counter = True

#TODO deal with couples
def getGenderHelper(interview):
    '''
    Counts the number of occurences of common pronouns that give away the interviewee's
    gender. 
    Returns the gender of the interviewee based on the number of 
    ''' 
    global counter
    #print(interview)
    # get interview summary
    summary = interview.get('interview_summary')
    name = interview.get('interviewee')

    if summary != None:
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
    
    # use Genderize.io as a backup in case interview does not have an interview summary
    elif name != None : 
        # get the interviewee's name
        tokens = name[0].split()
        first_name = ""

        # get a valid first name - ignore possible title prefixes, e.g "Mr."        
        if tokens[0] in TITLES_PREFIXES:
            first_name = tokens[1]
        else:
            first_name = tokens[0]

        # endpoint to be called     
        url = 'https://api.genderize.io/?name=' + first_name
        
        # call API
        try:
            response = requests.get(url)
            
            data = response.json()
           
            if data is not None and "probability" in data:
                if data["probability"] > 0.9:
                    # convert from unicode to 
                    gender = data["gender"]
                    gender.encode('ascii','ignore')
                    return gender
            
        except Exception as e:
            print "Exception: " + first_name
            
    
    return NO_GENDER


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
        result = h.query('Hol', 'undress_experiment', {}, {'id': 1, 'interview_summary': 1, 'interviewee': 1})
        
        # execute calls asynchronously
        for interview, gender in zip(result, executor.map(getGenderHelper, result)):

            # add known genders to the dictionary
            if gender != NO_GENDER:
                key = interview.get('id')
                interviewees_gender[key] = gender
    
    return interviewees_gender
        
if __name__ == "__main__":
    getGender()
