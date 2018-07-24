import os,sys
#set the project folder path
constants_path = os.getcwd()
sys.path.insert(0, constants_path)
import constants
import Levenshtein
import json

#set utils path
helper_path = os.getcwd()+"/utils"
sys.path.insert(0, helper_path)
from text import ReadCSVasDict,write_to_csv
import pdb
from pynlpl.formats import folia

###Globals###
path_to_CSV=constants.PATH_TO_FRAGMENTS_CSV
path_to_folia_xml=os.getcwd()+"/data/outputs/folia_output/"
path_log_file=constants.OUTPUT_FOLDER_FRAGMENTS_PROCESSING_LOGS
path_to_CSV_updated=constants.PATH_TO_FRAGMENTS_CSV_UPDATED

def main(fragments):
	not_retrieved=[]
	for index,record in enumerate(fragments):
		
		print str(index)+" fragments out of " + str(len(fragments)) + " have been processed."

		#open the original xml file
		folia_doc = folia.Document(file=path_to_folia_xml+record['testimony_id']+'.xml',encoding='utf-8')
		original_sentences=json.loads(record['original_sentences'])

		new_start_sentence_index=None
		new_end_sentence_index=None


		for i in range(int(record['start_sentence_index'])-100, int(record['end_sentence_index'])+100):
			sentence=folia_doc.sentences(i)
			if new_end_sentence_index is None:
				if Levenshtein.ratio(original_sentences[-1],sentence.text()) > 0.9:
					new_end_sentence_index=int(sentence.id.split('s')[1])-1
			if new_start_sentence_index is None:
				if Levenshtein.ratio(original_sentences[0],sentence.text()) > 0.9:
					new_start_sentence_index=int(sentence.id.split('s')[1])-1
			if (new_end_sentence_index is not None) and (new_start_sentence_index is not None):
				break

		#if the previous did not produce results
		sentences=folia_doc.sentences()
		for sentence in sentences:
			if new_end_sentence_index is None:
				if Levenshtein.ratio(original_sentences[-1],sentence.text()) > 0.9:
					new_end_sentence_index=int(sentence.id.split('s')[1])-1
			if new_start_sentence_index is None:
				if Levenshtein.ratio(original_sentences[0],sentence.text()) > 0.9:
					new_start_sentence_index=int(sentence.id.split('s')[1])-1
			if (new_end_sentence_index is not None) and (new_start_sentence_index is not None):
				break
		#if none produced results
		if (new_start_sentence_index is None) or (new_end_sentence_index is None):
			print record['testimony_id']
			record['start_sentence_index']=new_start_sentence_index
			record['end_sentence_index']= new_end_sentence_index
			#log it
			not_retrieved.append({'testimony_id':record['testimony_id'],'original_sentences':record['original_sentences']})


		else:
			record['start_sentence_index']=new_start_sentence_index
			record['end_sentence_index']= new_end_sentence_index
	if len(not_retrieved)==0:
		not_retrieved.append({'testimony_id':'','original_sentences':''})
	try:
		write_to_csv(not_retrieved,path_log_file+'fragments_not_retrieved.csv')
		write_to_csv(fragments,path_to_CSV_updated)
	except:
		print 'an error happened throughout the processing'
		pdb.set_trace()

if __name__ == '__main__':
	#run from the main project folder
	fragments=ReadCSVasDict(path_to_CSV)
	main(fragments)