import pdb
import constants
import json
import re
import pandas as pd


def segment_transcript(path_to_transcript_file,shelfmark,surname):
 '''Processes raw plain text transcripts (created by 3playmedia) that are 
	sequences of questions and answers. Beginning of each question or answer 
	is signed with an upper case word (such as for instance INTERVIEWER or DORI LAUB)
	The script is returning a list consisting of dictionaries with the key 'unit'. 
	Each unit corresponds to either a question or answer in the original interview
 '''
 #open the file and read in the text line by line
 input_data=open(path_to_transcript_file).readlines()


 
 output=[]
 
 #eliminate empty lines
 input_data=[element.strip().decode('utf-8') for element in input_data if element !='\n']
 input_data=correct_names(shelfmark,input_data)
 input_data=remove_surnames(shelfmark,input_data,surname)
 
 #process the transcript line by line
 for line in input_data:
	#check if a line is the beginning of segment by checking whether the second character of the line is uppercase
	
	
	if ((not line[1:2].islower()) and line[1:2]!=' '):
		output.append({'unit':line})
	#if it is not the beginning of a new segment, add it to thew last segment
	elif(len(output)>0):
		output[len(output)-1]['unit']=output[len(output)-1]['unit']+' '+line
	else:
		output.append({'unit':line})
	


			

 return output


def correct_names(shelfmark,data):
	'''A function to correct interviewer and subject names based on a data file provided by Fortunoff Staff'''

	#Read the data file line by line
	
	name_codes=open(constants.INPUT_FOLDER_FORTUNOFF_NAME_CODES+'name_codes.txt' ).readlines()
	codes=[json.loads(element.strip()) for element in name_codes]
	patterns=[pattern for pattern in codes if 'mssa_'+shelfmark ==pattern.keys()[0]][0]
		 
	#Create a python dic from each line, find the line with the corresponding shelfmark
	for i,line in enumerate(data):
		for pattern in patterns['mssa_'+shelfmark][0]:
			
			if len(re.split(pattern,line)) > 1:
				line_splitted=re.split(pattern,line)
				line_splitted[0]=patterns['mssa_'+shelfmark][0][pattern]
				
				data[i]=''.join(line_splitted)
				break
			
	
	return data

def remove_surnames(shelfmark,data,surname):
	 '''A function to remove the surnames of survivors from transcripts'''

	 # Load the list of surnames

	 
	 new_surname = '[surname removed]' 
	 for i,element in enumerate(data):
	 	data[i]=element.replace(surname,new_surname)
	 return data

