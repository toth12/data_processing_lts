import constants
import os


def make_output_pathes():
	os.makedirs(constants.OUTPUT_FOLDER_USHMM_PROCESSING_LOGS)
	os.makedirs(constants.OUTPUT_FOLDER_FORTUNOFF_PROCESSING_LOGS)
	os.makedirs(constants.OUTPUT_FOLDER_USC_PROCESSING_LOGS)
	os.makedirs(constants.OUTPUT_FOLDER_FRAGMENTS_PROCESSING_LOGS)
	os.makedirs(constants.OUTPUT_FOLDER_FRAGMENTS)
	os.makedirs(constants.OUTPUT_FOLDER_FOR_QUALITY_CONTROL)
	os.makedirs(constants.FOLIA_OUTPUT_FOLDER)
	os.makedirs(constants.FOLIA_PROCESSING_LOG_FOLDER)
	os.makedirs(constants.CORENLP_HOME)