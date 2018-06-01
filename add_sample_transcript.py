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
output_folder_db=constants.OUTPUT_FOLDER_DB
output_db=constants.OUTPUT_DB


def add_sample_transcript():
 
 input_collections=[output_collection_ushmm,output_collection_fortunoff,output_collection_usc]
 for collection in input_collections:
 	#get all entries
 	results=h.query(DB, collection, {},{'_id':0,'structured_transcript':0})
 	for result in results:
 		#check if already in the testimonies collection
 		testimonies=h.query(DB,'testimonies',{'testimony_id':result['testimony_id']},{})
 		if len(testimonies)==0:
 			result['html_transcript']='<html><body><p>This transcript is not yet available</p></body></html>'
 			result['status']='transcript_unprocessed'
 			h.insert(DB,'testimonies',result)

 


 


if __name__ == '__main__':
	
	add_sample_transcript()