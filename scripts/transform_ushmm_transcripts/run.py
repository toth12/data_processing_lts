from create_tracker import createTracker
from transcribe_core_doc import createStructuredTranscriptDoc
from transcribe_core_docx import createStructuredTranscriptDocx
from transcribe_non_core_doc import createStructuredTranscript_Non_Core_Doc
from transcribe_non_core_docx import createStructuredTranscript_Non_Core_Docx
import constants
import helper_mongo as h
import commands
import pdb

from transcribe_core_docx_made_from_pdf import createStructuredTranscriptDoc as transcribe_core_docx_made_from_pdf
from transcribe_non_core_docx_made_from_pdf import createStructuredTranscriptDoc as transcribe_non_core_docx_made_from_pdf

db = constants.DB
collection=constants.OUTPUT_COLLECTION_USHMM

def main():
	#Transcription of doc files involves a first step: transformation of them to docx
	#This is using Mac OS textutil if this is not available, processing of doc files is skipped

	#Check if textutil is available
	status, result = commands.getstatusoutput("textutil")

	
	#Create a collection that tracks the progress of processing
	createTracker()
	print ("A temporary collection tracking the transformation of USHMM transcript was set up")

	
	
	#Transcribe files belonging to the core data asset and has the DOCX format
	print ("The processing of USHMM transcripts in DOC format belonging to the core asset has started")
	createStructuredTranscriptDocx()
	
	#Transcribe files belonging to the core data asset and has the DOC format
	print ("The processing of USHMM transcripts in DOC format belonging to the core asset has started")
	
	if status ==0:

		createStructuredTranscriptDoc()
	else:
		print ('Textutil is not available on this system, this is skipped')
	
	
	
	#Transcribe files not belonging to the core data asset and has the DOC format -> this is where the problem is
	print ("The processing of USHMM transcripts in DOC format not belonging to the core asset has started")

	if status ==0:

		createStructuredTranscript_Non_Core_Doc()
	else:
		print ('Textutil is not available on this system, this is skipped')
	

	
	#Transcribe files not belonging to the core data asset and has the DOCX format
	print ("The processing of USHMM transcripts in DOCX format not belonging to the core asset has started")
	createStructuredTranscript_Non_Core_Docx()

	
	

	#Transcribe files belonging to the core data asset and originally in pdf
	print ("The processing of USHMM transcripts, which were originally in PDF, and belonging to the core asset has started")
	transcribe_core_docx_made_from_pdf()
	
	#Transcribe files not belonging to the core data asset and originally in pdf
	print ("The processing of USHMM transcripts, which were originally in PDF, and not belonging to the core asset has started")
	transcribe_non_core_docx_made_from_pdf()

	#delete those entries that were not yet processed
	#h.delete(db,collection,{'structured_transcript': { '$exists': False } })


	
	


if __name__ == '__main__':
	main()