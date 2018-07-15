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
from subprocess import call


#added
from scripts.transform_ushmm_transcripts import transcribe_core_docx_made_from_pdf
from scripts.transform_ushmm_transcripts import transcribe_non_core_docx_made_from_pdf
from scripts.transform_ushmm_transcripts import transcribe_core_docx
from scripts.transform_ushmm_transcripts import transcribe_core_doc
from scripts.transform_ushmm_transcripts import transcribe_non_core_doc 
from scripts.transform_ushmm_transcripts import transcribe_non_core_docx as tcd 
from scripts.transform_ushmm_transcripts import run
#import project specific scripts
from scripts.create_ushmm_metadata import run as create_ushmm_metadata
from scripts.transform_ushmm_transcripts import run as create_ushmm_transcript_input
from scripts.create_fortunoff_metadata import parse as create_fortunoff_metadata
from scripts.transform_fortunoff_transcripts import parse 
from scripts.create_usc_metadata import run as create_usc_metadata
from scripts.transform_usc_transcripts import run as create_usc_transcripts
from scripts.create_folia_input import run as create_folia_input
from add_sample_transcript import add_sample_transcript
from scripts.create_fragments_collection import run as create_fragments_collection


##Global Variables##

DB = constants.DB

output_collection_fortunoff=constants.OUTPUT_COLLECTION_FORTUNOFF
output_collection_usc=constants.OUTPUT_COLLECTION_USC
output_collection_ushmm=constants.OUTPUT_COLLECTION_USHMM
output_folder_db=constants.OUTPUT_FOLDER_DB
output_db=constants.OUTPUT_DB


def process_data():
	methods={}
	lines=open('fragment_not_in_xml').readlines()
	for line in lines:
		print line
		result=h.query(DB,constants.USHMM_TRACKER_COLLECTION,{'id':line.strip().strip('\n')},{'method':1,'microsoft_doc_file':1})
		if len(result)>0:
			if result[0]['method'] in methods.keys():
				methods[result[0]['method']].append(result[0]['microsoft_doc_file'])
			else:
				methods[result[0]['method']]=[result[0]['microsoft_doc_file']]

	for element in methods['transcribe_core_doc']:
		pdb.set_trace()
		command = 'textutil -convert docx ' + constants.INPUT_FOLDER_USHMM_TRANSCRIPTS_DOC+element[0] + ' -output ' + element[0]+'x' 
            
		call(command, shell=True)
		units=transcribe_core_doc.getTextUnits(element[0]+'x')

		
		pdb.set_trace()
	#transcribe_non_core_docx_made_from_pdf.createStructuredTranscriptDoc()

	'''url='/Users/gmt28/Documents/Workspace/Docker_Engine/varad/Yale_Projects/shoah-foundation-data-restored/shoah-foundation-data/data/inputs/fortunoff/transcripts/'
	files=[url+'mssa_hvt_93_p1of2.plain_text.txt',url+'mssa_hvt_93_p2of2.plain_text.txt']
	print files[0]
	result=parse.segment_transcript(files[0])
	pdb.set_trace()'''
	
if __name__ == '__main__':
	process_data()
	