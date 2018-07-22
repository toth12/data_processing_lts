import os,sys
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import text
import folia_utils
import pdb
import helper_mongo as h
root_path = os.path.join("..", "..")
sys.path.insert(0, root_path)
import constants
from string import Template
import commands





input_csv='sample_data/quality_control.csv'
path_to_old_folia=os.path.join("..", "..", "data/outputs/folia_output_old/")
path_to_new_folia=os.path.join("..", "..", "data/outputs/folia_output/")
DB=constants.DB
method_collection='USHMM_transcript_processing_progress_test'

def add_additional_data(data,pool='old'):
	new_data=[]
	for record in data[105:110]:
		entry=record.copy()
		
		#Get the number of tokens in the previous folia output
		counts_previous_folia=get_previous_folia_out(record['testimony_id'])
		entry['token_in_prev_folia']=counts_previous_folia['tokens']
		entry['divs_in_prev_folia']=counts_previous_folia['divisions']

		
		#Get the number of tokens in the current folia
		counts_current_folia=get_current_folia_out(record['testimony_id'])
		entry['token_in_current_folia']=counts_current_folia['tokens']
		entry['divs_in_current_folia']=counts_current_folia['divisions']
		

		#Get the method used for building this file
		try:
			entry['method']=h.query(DB,method_collection,{'id':record['testimony_id']},{'method':1})[0]['method']
		except:
			entry['method']=''

		#Get the number of tokens in the undress experiment
		entry['token_in_undress_experiment']=get_undress_exp_token_count(record['testimony_id'])
		if pool=='old':
			if len(entry['pass or fail'])>0:
				entry['status']='first_qc'
			else:
				entry['status']=''

		else:
			entry['status']=''
		#Get the lenght of videos
		entry['video_lenght']=get_video_length(entry['testimony_id'])
		new_data.append(entry)
	
	pdb.set_trace()


def get_previous_folia_out(testimony_id):
	counts={}

	counts=folia_utils.get_counts(path_to_old_folia+testimony_id+'.xml')

	return counts


def get_current_folia_out(testimony_id):
	counts=folia_utils.get_counts(path_to_new_folia+testimony_id+'.xml')
	return counts

def get_undress_exp_token_count(testimony_id):
	#connect to mongo
	all_ids=h.query(DB,'undress',{},{'id':1,'_id':0})

	for element in all_ids[0:1]:
		result=h.query(DB,'undress',{'id':element['id']},{'sentence_segmented_tokenized_only_lemmas':1})[0]
		data=result['sentence_segmented_tokenized_only_lemmas']
		count=sum(len(sentence) for sentence in data)
		return count
def get_video_length(testimony_id):
	#get videos
	videos=h.query('lts','testimonies',{'testimony_id':testimony_id},{'media_url':1})[0]['media_url']
	if len(videos)>0:
		complete_duration=[]
		for video in videos:
			command_to_get_duration= "ffmpeg -i '"+video+"' 2>&1 | grep Duration | awk '{print $2}' | tr -d ,"
			
			## run it ##
			duration=commands.getoutput(command_to_get_duration)
			complete_duration.append(get_sec(duration))
		complete_duration=sum(element for element in complete_duration)
	else:
		complete_duration=None
	return complete_duration
	

def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(float(s))
if __name__ == '__main__':
	#read the csv file in
	input_data=text.ReadCSVasDict(input_csv)
	add_additional_data(input_data)
	pdb.set_trace()





