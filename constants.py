import sys, os


#set the pathes of the data specific input folders
INPUT_FOLDER_USHMM_METADATA = os.getcwd()+"/data/inputs/ushmm/metadata/"

#set the parameter of the Mongo DB and data specific collections

OUTPUT_COLLECTION_USHMM = "output_ushmm_metadata"
INPUT_COLLECTION_USHMM = "input_ushmm_metadata"
DB = "let_them_speak_data_processing"

#set the pathes of the data specific processing logs
OUTPUT_FOLDER_USHMM_PROCESSING_LOGS = os.getcwd()+"/data/outputs/USHMM/processing_logs/"

