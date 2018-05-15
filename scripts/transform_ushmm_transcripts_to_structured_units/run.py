from create_tracker import createTracker
from transcribe_core_doc import createStructuredTranscriptDoc

def main():
	#Create a collection that tracks the progress of processing
	#createTracker()
	print ("A temporary collection tracking the transformation of USHMM transcript was set up")

	#Transcribe files belonging to the cora data asset and has the DOC format
	print ("The processing of USHMM transcripts in DOC format belonging to the core asset has started")
	createStructuredTranscriptDoc()

if __name__ == '__main__':
	main()