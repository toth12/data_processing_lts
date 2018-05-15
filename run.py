import sys, os

#set utils path
helper_path = os.getcwd()+"/utils"
sys.path.insert(0, helper_path)

#set constants path
constants_path = os.getcwd()
sys.path.insert(0, constants_path)	

#import project specific scripts
from scripts.create_ushmm_metadata import run as create_ushmm_metadata
from scripts.transform_ushmm_transcripts_to_structured_units import run as create_ushmm_transcript_input




def process_data():

 #transform USHMM catalogue data to app specific metadata
 '''print ("The processing of USHMM metadata has started")
 create_ushmm_metadata.main()
 print ("The processing of USHMM metadata finished")'''

 #process USHMM transcripts
 print ("The processing of USHMM transcripts has started")
 create_ushmm_transcript_input.main()



 
if __name__ == '__main__':
	
	process_data()