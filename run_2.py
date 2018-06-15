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
from shutil import copyfile




#import project specific scripts
from scripts.create_ushmm_metadata import run as create_ushmm_metadata
from scripts.transform_ushmm_transcripts import run as create_ushmm_transcript_input
from scripts.create_fortunoff_metadata import parse as create_fortunoff_metadata
from scripts.transform_fortunoff_transcripts import run as create_fortunoff_transcript_input
from scripts.create_usc_metadata import run as create_usc_metadata
from scripts.transform_usc_transcripts import run as create_usc_transcripts
from scripts.create_folia_input import run as create_folia_input
from add_sample_transcript import add_sample_transcript
from scripts.create_fragments_collection import run as create_fragments_collection

from scripts.transform_ushmm_transcripts import create_tracker

#added
from scripts.transform_ushmm_transcripts import transcribe_core_docx_made_from_pdf
from scripts.transform_ushmm_transcripts import transcribe_non_core_docx_made_from_pdf
from scripts.transform_ushmm_transcripts import transcribe_core_docx    
##Global Variables##

DB = constants.DB

output_collection_fortunoff=constants.OUTPUT_COLLECTION_FORTUNOFF
output_collection_usc=constants.OUTPUT_COLLECTION_USC
output_collection_ushmm=constants.OUTPUT_COLLECTION_USHMM
output_folder_db=constants.OUTPUT_FOLDER_DB
output_db=constants.OUTPUT_DB
TRACKER = constants.USHMM_TRACKER_COLLECTION



def process_data():
 
	transcribe_core_docx_made_from_pdf.createStructuredTranscriptDoc() 
	#transcribe_non_core_docx_made_from_pdf.createStructuredTranscriptDoc()
	#transcribe_core_docx.createStructuredTranscriptDocx()



if __name__ == '__main__':
	
	process_data()