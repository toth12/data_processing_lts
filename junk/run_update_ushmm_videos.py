#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
import pdb
import shutil
#set utils path
helper_path = os.getcwd()+"/utils"
sys.path.insert(0, helper_path)
import helper_mongo as h
import transform_fragments_in_csv_to_json_for_fragments_collection
import encodings
from encodings import idna
from encodings import ascii


#parse argument for debugging
import argparse
parser = argparse.ArgumentParser(description="Only the first ten interviews are processed from every collection")
parser.add_argument('-debug', action='store_true')
args = parser.parse_args()
debug = args.debug


#set constants path
constants_path = os.getcwd()
sys.path.insert(0, constants_path)
import constants
from make_output_pathes import make_output_pathes



#import project specific scripts
from scripts.create_ushmm_metadata import run as create_ushmm_metadata
from scripts.transform_ushmm_transcripts import run as create_ushmm_transcript_input
from scripts.create_fortunoff_metadata import parse as create_fortunoff_metadata
from scripts.transform_fortunoff_transcripts import run as create_fortunoff_transcript_input
from scripts.create_usc_metadata import run as create_usc_metadata
from scripts.transform_usc_transcripts import run as create_usc_transcripts
from scripts.create_folia_input import run as create_folia_input
from add_sample_transcript import add_sample_transcript
from scripts.identify_interviews_with_more_persons import run as identify_interviews_with_more_persons
from scripts.print_all_testimonies import run as print_all_testimonies
from scripts.identify_interviewees_sharing_same_surname import run as identify_interviewees_sharing_same_surname
from scripts.identify_interviewees_giving_more_interviews import run as identify_interviewees_giving_more_interviews
from scripts.order_interviewees_by_surnames import run as order_interviewees_by_surnames
from scripts.identify_interviews_without_year_of_recording import run as identify_interviews_without_year_of_recording
from scripts.identify_interviews_without_ghetto_and_camp import run as identify_interviews_without_ghetto_and_camp
from scripts.identify_interviews_without_gender_infos import run as identify_interviews_without_gender_infos
from scripts.identify_interviews_without_name_of_interviewees import run as identify_interviews_without_name_of_interviewees
from scripts.correct_shelfmarks import run as correct_shelfmarks
from scripts.update_ushmm_videos import run as update_videos
##Global Variables##

DB = constants.DB

output_collection_fortunoff=constants.OUTPUT_COLLECTION_FORTUNOFF
output_collection_usc=constants.OUTPUT_COLLECTION_USC
output_collection_ushmm=constants.OUTPUT_COLLECTION_USHMM
output_folder_db=constants.OUTPUT_FOLDER_DB
output_db=constants.OUTPUT_DB
output_folder_fragments=constants.OUTPUT_FOLDER_FRAGMENTS



def process_data():
    update_videos.run()

 






if __name__ == '__main__':
 process_data()