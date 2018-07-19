'''
Transforms a mongo fragment collection to a CSV file, and inserts the original sentence from folia xml files
Each entry in the CSV file has the following fields:
mid_leaf, media_index, media_offset, testimony_id, end_sentence_index, label, original_sentences, start_sentence_index,main_leaf

if a leaf is prototypical, its mid_leaf left empty

'''


import pdb
import os, sys
constants_path = os.getcwd()
sys.path.insert(0, constants_path)
import constants
from pynlpl.formats import folia
#set utils path
helper_path = os.getcwd()+"/utils"
sys.path.insert(0, helper_path)
import helper_mongo as h
import csv
import json

DB = 'lts'
collection='fragments'
path_to_folia_xml=os.getcwd()+"/data/outputs/folia_output/"
output_path='some path to here'


def get_leaves():
	'''Get all branches of a tree and transforms them to entries in a CSV file'''
	#get all fragments with testimony id and position in the db

	all_fragments=[]
	leaves=h.query(DB,collection,{},{'tree.children':1,'label':1})
	for leaf in leaves:
		result=get_prototypical_fragments(leaf)
		all_fragments.extend(result)

		result=get_fragments_of_sub_experiences(leaf)
		all_fragments.extend(result)


	write_to_csv(all_fragments,output_path)

	

	
def get_prototypical_fragments(leaf):
	'''Get leafes expressing prototypical experiences of a main leaf'''
	prototypical_fragments=[]
	#iterate through all leafes and find the ones that have no children, they are the prototypical ones
	for element in leaf['tree']['children']:
		if len(element['children'])==0:
			
			#get rid of children as this is not necessary
			entry=element.copy()
			entry.pop('children',None)
			
			#set the main label
			entry['main_leaf']=leaf['label']

			#set the mid leaf to empty
			entry['mid_leaf']=''

			#get the original sentence
			original_sentences=get_fragments_original_sentence(entry['testimony_id'],entry['start_sentence_index'],entry['end_sentence_index'])
			entry['original_sentences']=json.dumps(original_sentences)

			prototypical_fragments.append(entry)
			
			
			

	return prototypical_fragments

def get_fragments_of_sub_experiences(leaf):
	'''Get leafes expressing sub-experiences of a main leaf'''
	fragments_of_sub_experiences=[]
	#iterate through all sub leafes and find the ones that have children, they are the sub experiences
	for element in leaf['tree']['children']:
		if len(element['children'])>0:

			mid_leaf=element['label']

			#find the sub leaves
			for sub_leaf in element['children']:
					
					entry=sub_leaf.copy()
					entry.pop('children',None)
				#set the main label
					entry['main_leaf']=leaf['label']

					#set the mid leaf to empty
					entry['mid_leaf']=mid_leaf

					#get the original sentence
					original_sentences=get_fragments_original_sentence(entry['testimony_id'],entry['start_sentence_index'],entry['end_sentence_index'])
					entry['original_sentences']=json.dumps(original_sentences)

					fragments_of_sub_experiences.append(entry)
			
					
		

	
	return fragments_of_sub_experiences




def get_fragments_original_sentence(folia_xml_id,start_sentence_index,end_sentence_index):
	'''Finds the original sentence of a fragment'''
	folia_doc = folia.Document(file=path_to_folia_xml+folia_xml_id+'.xml',encoding='utf-8')
	sentences=[]
	
	if (start_sentence_index==end_sentence_index):
	 	sentence=folia_doc.sentences(start_sentence_index-1).text()
	 	sentences.append(sentence)
	else:
		for i in range(start_sentence_index,end_sentence_index):
			sentence=folia_doc.sentences(i-1).text()
		 	sentences.append(sentence)
	return sentences

def write_to_csv(data,file):
	keys = data[0].keys()
	f=open(file, 'wb')
	writer = csv.DictWriter(f, fieldnames=keys)
	writer.writeheader()
	writer.writerows(data)


	
if __name__ == '__main__':
	get_leaves()

