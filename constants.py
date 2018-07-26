import sys, os


#set the pathes of the data specific input folders
INPUT_FOLDER_USHMM_METADATA = os.getcwd()+"/data/inputs/ushmm/metadata/"
INPUT_FOLDER_USHMM_TRANSCRIPTS_DOC = os.getcwd()+"/data/inputs/ushmm/transcripts/microsoft_doc_docx/"
INPUT_FOLDER_USHMM_TRANSCRIPTS_PDF_TRANSFORMED_TO_DOCS = os.getcwd()+"/data/inputs/ushmm/pdf_transcript_not_available_in_doc_transformed_to_docx/"
INPUT_FOLDER_FORTUNOFF_METADATA = os.getcwd()+"/data/inputs/fortunoff/metadata/"
INPUT_FOLDER_FORTUNOFF_TRANSCRIPTS = os.getcwd()+"/data/inputs/fortunoff/transcripts/"
INPUT_FOLDER_FORTUNOFF_NAME_CODES = os.getcwd()+"/data/inputs/fortunoff/"
INPUT_FOLDER_USC_METADATA = os.getcwd()+"/data/inputs/usc/metadata/"
INPUT_FOLDER_USC_TRANSCRIPTS=os.getcwd()+"/data/inputs/usc/transcripts/"
INPUT_FOLDER_FRAGMENTS=os.getcwd()+"/data/inputs/fragments/"

#set the parameter of the Mongo DB and data specific collections

OUTPUT_COLLECTION_USHMM = "output_ushmm_metadata"
INPUT_COLLECTION_USHMM = "input_ushmm_metadata"
OUTPUT_COLLECTION_FORTUNOFF = "output_fortunoff_metadata"
OUTPUT_COLLECTION_USC = "output_usc_metadata"
DB = "let_them_speak_data_processing"

#set the pathes of the data specific processing logs
OUTPUT_FOLDER_USHMM_PROCESSING_LOGS = os.getcwd()+"/data/outputs/ushmm/processing_logs/"
OUTPUT_FOLDER_FORTUNOFF_PROCESSING_LOGS = os.getcwd()+"/data/outputs/fortunoff/processing_logs/"
OUTPUT_FOLDER_USC_PROCESSING_LOGS = os.getcwd()+"/data/outputs/usc/processing_logs/"
OUTPUT_FOLDER_DB=os.getcwd()+"/data/outputs/db/"
OUTPUT_DB='lts'
OUTPUT_FOLDER_FRAGMENTS_PROCESSING_LOGS=os.getcwd()+"/data/outputs/fragment_processing_logs/"
OUTPUT_FOLDER_FRAGMENTS=os.getcwd()+"/data/outputs/fragments/"
OUTPUT_FOLDER_FOR_QUALITY_CONTROL=os.getcwd()+"/data/outputs/collections_for_quality_control/"


USHMM_TRACKER_COLLECTION = "USHMM_transcript_processing_progress_test"

STANFORD_CORE_NLP_JAR=os.getcwd()+"/lib/stanford-corenlp-full-2018-02-27"

FOLIA_OUTPUT_FOLDER=os.getcwd()+"/data/outputs/folia_output/"

FOLIA_PROCESSING_LOG_FOLDER=os.getcwd()+"/data/outputs/folia_processing_log/"

CORENLP_HOME=os.getcwd()+"/lib/stanford-corenlp/"

PATH_TO_FRAGMENTS_CSV=os.getcwd()+"/data/inputs/fragments/fragments.csv"
PATH_TO_FRAGMENTS_CSV_UPDATED=os.getcwd()+"/data/inputs/fragments/fragments_updated.csv"




