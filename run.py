import sys, os
import pdb
#set utils path
helper_path = os.getcwd()+"/utils"
sys.path.insert(0, helper_path)
import helper_mongo as h

#set constants path
constants_path = os.getcwd()
sys.path.insert(0, constants_path)
import constants


#import project specific scripts
from scripts.create_ushmm_metadata import run as create_ushmm_metadata
from scripts.transform_ushmm_transcripts import run as create_ushmm_transcript_input
from scripts.create_fortunoff_metadata import parse as create_fortunoff_metadata
from scripts.transform_fortunoff_transcripts import run as create_fortunoff_transcript_input
from scripts.create_usc_metadata import run as create_usc_metadata
from scripts.transform_usc_transcripts import run as create_usc_transcripts
from scripts.create_folia_input import run as create_folia_input


##Global Variables##

DB = constants.DB

output_collection_fortunoff=constants.OUTPUT_COLLECTION_FORTUNOFF
output_collection_usc=constants.OUTPUT_COLLECTION_USC
output_collection_ushmm=constants.OUTPUT_COLLECTION_USHMM



def process_data():
 
 '''#create the empty let_them_data_processing database
 os.system('mongo ' + DB + ' --eval "db.createCollection(\'test\')"')
 
 #transform USHMM catalogue data to app specific metadata
 print ("The processing of USHMM metadata has started")
 create_ushmm_metadata.main()
 print ("The processing of USHMM metadata finished")
 
 #process USHMM transcripts
 print ("The processing of USHMM transcripts has started")
 create_ushmm_transcript_input.main()
 print ("The processing of USHMM transcripts finished")
 
 
 #transform Fortunoff catalogue data to app specific metadata
 print ("The processing of Fortunoff metadata has started")
 create_fortunoff_metadata.main()
 print ("The processing of Fortunoff metadata finished")

 #process Fortunoff transcripts
 print ("The processing of Fortunoff transcripts has started")
 create_fortunoff_transcript_input.run()
 print ("The processing of Fortunoff transcripts has finished")
 
 #transform USC catalogue data to app specific metadata
 print ("The processing of USC metadata has started")
 create_usc_metadata.main()
 print ("The processing of USC metadata finished")
 
 #process USC transcripts
 print ("The processing of USC transcripts has started")
 create_usc_transcripts.run()
 print ("The processing of USC transcripts has finished")
 
 #test the output results
 print ("Testing of output has started; for a more detailed output run: python test_processing_outputs.py ")
 os.system('pytest test_processing_outputs.py')
 print ("Testing of output has finished")


 #copy the three collections into one
 '''
 os.system('mongo ' + DB + ' --eval "db.'+output_collection_fortunoff+'.copyTo(\'testimonies\')"')
 os.system('mongo ' + DB + ' --eval "db.'+output_collection_ushmm+'.copyTo(\'testimonies\')"')
 os.system('mongo ' + DB + ' --eval "db.'+output_collection_usc+'.copyTo(\'testimonies\')"')
 
 create_folia_input.main()

 '''

 #delete unprocessed entries

 h.delete(db,'testimonies',{'html_transcript': { '$exists': False } })

 '''
 
 





 
 







 
if __name__ == '__main__':
	
	process_data()