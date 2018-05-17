from create_tracker import createTracker
from transcribe_core_doc import createStructuredTranscriptDoc
from transcribe_core_docx import createStructuredTranscriptDocx
from transcribe_non_core_doc import createStructuredTranscript_Non_Core_Doc
from transcribe_non_core_docx import createStructuredTranscript_Non_Core_Docx
import constants
import helper_mongo as h

db = constants.DB
collection=constants.OUTPUT_COLLECTION_USHMM

def main():
	#Create a collection that tracks the progress of processing
	createTracker()
	print ("A temporary collection tracking the transformation of USHMM transcript was set up")

	#Transcribe files belonging to the core data asset and has the DOC format
	print ("The processing of USHMM transcripts in DOC format belonging to the core asset has started")
	createStructuredTranscriptDoc()

	#Transcribe files belonging to the core data asset and has the DOCX format
	print ("The processing of USHMM transcripts in DOC format belonging to the core asset has started")
	createStructuredTranscriptDocx()

	#Transcribe files not belonging to the core data asset and has the DOC format
	print ("The processing of USHMM transcripts in DOC format not belonging to the core asset has started")
	createStructuredTranscript_Non_Core_Doc()

	#Transcribe files not belonging to the core data asset and has the DOCX format
	print ("The processing of USHMM transcripts in DOCX format not belonging to the core asset has started")
	createStructuredTranscript_Non_Core_Docx()

	#delete those entries that were not yet processed
	h.delete(db,collection,{'structured_transcript': { '$exists': False } })






if __name__ == '__main__':
	main()