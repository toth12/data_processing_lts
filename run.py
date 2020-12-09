import sys, os
import pdb
import shutil
#set utils path
helper_path = os.getcwd()+"/utils"
sys.path.insert(0, helper_path)
import helper_mongo as h
import transform_fragments_in_csv_to_json_for_fragments_collection


#parse argument for debugging
import argparse
parser = argparse.ArgumentParser(description="Only the first ten interviews are processed from every collection")
parser.add_argument('-debug', action='store_true')
args = parser.parse_args()
debug = args.debug


#set constants path
constants_path = os.getcwd()
sys.path.insert(0, constants_path)
import constants
from make_output_pathes import make_output_pathes



#import project specific scripts
from scripts.create_ushmm_metadata import run as create_ushmm_metadata
from scripts.transform_ushmm_transcripts import run as create_ushmm_transcript_input
from scripts.create_fortunoff_metadata import parse as create_fortunoff_metadata
from scripts.transform_fortunoff_transcripts import run as create_fortunoff_transcript_input
from scripts.create_usc_metadata import run as create_usc_metadata
from scripts.transform_usc_transcripts import run as create_usc_transcripts
from scripts.create_folia_input import run as create_folia_input
from add_sample_transcript import add_sample_transcript
from scripts.identify_interviews_with_more_persons import run as identify_interviews_with_more_persons
from scripts.print_all_testimonies import run as print_all_testimonies
from scripts.identify_interviewees_sharing_same_surname import run as identify_interviewees_sharing_same_surname
from scripts.identify_interviewees_giving_more_interviews import run as identify_interviewees_giving_more_interviews
from scripts.order_interviewees_by_surnames import run as order_interviewees_by_surnames
from scripts.identify_interviews_without_year_of_recording import run as identify_interviews_without_year_of_recording
from scripts.identify_interviews_without_ghetto_and_camp import run as identify_interviews_without_ghetto_and_camp
from scripts.identify_interviews_without_gender_infos import run as identify_interviews_without_gender_infos
from scripts.identify_interviews_without_name_of_interviewees import run as identify_interviews_without_name_of_interviewees
from scripts.correct_ushmm_shelfmarks import run as correct_ushmm_shelfmarks
##Global Variables##

DB = constants.DB

output_collection_fortunoff=constants.OUTPUT_COLLECTION_FORTUNOFF
output_collection_usc=constants.OUTPUT_COLLECTION_USC
output_collection_ushmm=constants.OUTPUT_COLLECTION_USHMM
output_folder_db=constants.OUTPUT_FOLDER_DB
output_db=constants.OUTPUT_DB
output_folder_fragments=constants.OUTPUT_FOLDER_FRAGMENTS



def process_data():

 
 
 #create the output folders
 make_output_pathes()

 #delete lts database if already in the system
 os.system('mongo ' + output_db + ' --eval "db.dropDatabase()"')

 #delete the processing databases if already in the system
 os.system('mongo ' + DB + ' --eval "db.dropDatabase()"')


 

 #create the empty let_them_data_processing database
 os.system('mongo ' + DB + ' --eval "db.createCollection(\'test\')"')
 
 #transform USC catalogue data to app specific metadata
 print ("The processing of USC metadata has started")
 create_usc_metadata.main()
 print ("The processing of USC metadata finished")
 
 #process USC transcripts
 print ("The processing of USC transcripts has started")
 create_usc_transcripts.run(debug)
 print ("The processing of USC transcripts has finished")

 #transform USHMM catalogue data to app specific metadata
 print ("The processing of USHMM metadata has started")
 create_ushmm_metadata.main()

 print ("The processing of USHMM metadata finished")

 #process USHMM transcripts
 print ("The processing of USHMM transcripts has started")
 create_ushmm_transcript_input.main(debug)
 
 
 print ("The processing of USHMM transcripts finished")

 #transform Fortunoff catalogue data to app specific metadata
 print ("The processing of Fortunoff metadata has started")
 create_fortunoff_metadata.main()
 print ("The processing of Fortunoff metadata finished")

 #process Fortunoff transcripts
 print ("The processing of Fortunoff transcripts has started")
 create_fortunoff_transcript_input.run(debug=debug)
 print ("The processing of Fortunoff transcripts has finished")
 
 
 
 

 

 
 
 
 #test the output results
 print ("Testing of output has started; for a more detailed output run: python test_processing_outputs.py ")
 os.system('pytest test_processing_outputs.py')
 print ("Testing of output has finished")


 #copy the three collections into one
 

 
 os.system('mongo ' + DB + ' --eval "db.'+output_collection_fortunoff+'.copyTo(\'testimonies\')"')
 
 os.system('mongo ' + DB + ' --eval "db.'+output_collection_ushmm+'.copyTo(\'testimonies\')"')

 
 os.system('mongo ' + DB + ' --eval "db.'+output_collection_usc+'.copyTo(\'testimonies\')"')

 #create the folia input
 create_folia_input.main()

 

 #delete entries that could not be processed by folia

 h.delete(DB,'testimonies',{'html_transcript': { '$exists': False } })

 #delete entries where transformation to structured_transcript was not possible
 h.delete(DB,'testimonies',{'structured_transcript': { '$exists': False } })

#perhaps these entries are to be logged

 
 #upload sample text to the unprocessed entries if necessary and update their status to transcript_unprocessed

 add_sample_transcript()

 #add a status transcript_processed to processed entries 
 
 results=h.query(DB, 'testimonies', {'status': { '$exists': False } },{'_id':1})
 for result in results:
 		#update the status
 		status={'status':'transcript_processed'}
 		h.update_entry(DB,'testimonies',result['_id'],status)


 #create fragments from the CSV input file
 transform_fragments_in_csv_to_json_for_fragments_collection.main()



 #create a new DB and copy everything to there


 os.system('mongo ' + DB + ' --eval "db.copyDatabase(\''+DB+'\',\''+output_db+'\',\'localhost\')"')


#post-process the output DB

#correct USHMM shelfmarks
 correct_ushmm_shelfmarks.run()

#extract interviews with multiple persons and set empty of their gender
 identify_interviews_with_more_persons.run()

#print all interviews titles and shelfmarks to file
 print_all_testimonies.run()

 #print interviewees giving multiple interviews
 identify_interviewees_giving_more_interviews.run()

 #identify interviewers sharing the same surname
 identify_interviewees_sharing_same_surname.run()

 #print all interviewees arranged by surnames
 order_interviewees_by_surnames.run()


 #print all interviews without recording year
 identify_interviews_without_year_of_recording.run()

 #identify interviews without camps and ghettos
 identify_interviews_without_ghetto_and_camp.run()

 #identify interviews without gender
 identify_interviews_without_gender_infos.run()

 #identify interviews where no interviewee name was retrieved
 identify_interviews_without_name_of_interviewees.run()

#delete the unnecessary collections from the final result
 
 collections_to_delete=[constants.OUTPUT_COLLECTION_USHMM,constants.INPUT_COLLECTION_USHMM,constants.OUTPUT_COLLECTION_FORTUNOFF,constants.OUTPUT_COLLECTION_USC,constants.USHMM_TRACKER_COLLECTION,'test']
 for collection in collections_to_delete:
 	os.system('mongo ' + output_db + ' --eval "db.'+collection+'.drop()"')

#add the fragment collection to it

 os.system('mongoimport -d ' + output_db + ' -c fragments --file '+output_folder_fragments+'fragments.json --jsonArray')


 #archive the output db

 os.system('mongodump --db=' + output_db + ' --archive='+output_folder_db+'lts.archive')

 #delete it from the host system

#os.system('mongo ' + output_db + ' --eval "db.dropDatabase()"')

 #delete processing DB from the system

 #os.system('mongo ' + DB + ' --eval "db.dropDatabase()"')

 #zip the folia files
 os.system('zip -r -j data/outputs/folia_output/folia.zip data/outputs/folia_output/*')

 #upload the data to amazon server
 '''
 print 'upload data to amazon servers'

 os.system('aws s3 cp data/outputs/folia_output/folia.zip s3://lab-secrets/let-them-speak/folia.zip --profile lab-secrets')

 os.system('aws s3 cp data/outputs/db/lts.archive s3://lab-secrets/let-them-speak/lts.archive --profile lab-secrets')

'''


if __name__ == '__main__':
 dir = "data/outputs/"
 shutil.rmtree(dir,ignore_errors=True)
 process_data()