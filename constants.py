import sys, os


#set the pathes of the data specific input folders
INPUT_FOLDER_USHMM_METADATA = os.getcwd()+"/data/inputs/ushmm/metadata/"
INPUT_FOLDER_USHMM_TRANSCRIPTS_DOC = os.getcwd()+"/data/inputs/ushmm/transcripts/microsoft_doc_docx/"
#set the parameter of the Mongo DB and data specific collections

OUTPUT_COLLECTION_USHMM = "output_ushmm_metadata"
INPUT_COLLECTION_USHMM = "input_ushmm_metadata"
DB = "let_them_speak_data_processing"

#set the pathes of the data specific processing logs
OUTPUT_FOLDER_USHMM_PROCESSING_LOGS = os.getcwd()+"/data/outputs/USHMM/processing_logs/"


USHMM_TRACKER_COLLECTION = "USHMM_transcript_processing_progress"
