import sys, os


#set the pathes of the data specific input folders
INPUT_FOLDER_USHMM_METADATA = os.getcwd()+"/data/inputs/ushmm/metadata/"
INPUT_FOLDER_USHMM_TRANSCRIPTS_DOC = os.getcwd()+"/data/inputs/ushmm/transcripts/microsoft_doc_docx/"
INPUT_FOLDER_FORTUNOFF_METADATA = os.getcwd()+"/data/inputs/fortunoff/metadata/"
INPUT_FOLDER_FORTUNOFF_TRANSCRIPTS = os.getcwd()+"/data/inputs/fortunoff/transcripts/"

#set the parameter of the Mongo DB and data specific collections

OUTPUT_COLLECTION_USHMM = "output_ushmm_metadata"
INPUT_COLLECTION_USHMM = "input_ushmm_metadata"
OUTPUT_COLLECTION_FORTUNOFF = "output_fortunoff_metadata"
DB = "let_them_speak_data_processing_test"

#set the pathes of the data specific processing logs
OUTPUT_FOLDER_USHMM_PROCESSING_LOGS = os.getcwd()+"/data/outputs/ushmm/processing_logs/"
OUTPUT_FOLDER_FORTUNOFF_PROCESSING_LOGS = os.getcwd()+"/data/outputs/fortunoff/processing_logs/"


USHMM_TRACKER_COLLECTION = "USHMM_transcript_processing_progress_test"
