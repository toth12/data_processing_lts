import pdb
import constants
import json
import re
import pandas as pd
import re

def segment_transcript(path_to_transcript_file,shelfmark,surnames):
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
 input_data=remove_surnames(shelfmark,input_data,surnames,path_to_transcript_file)
 
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

def remove_surnames(shelfmark,data,surnames,path_to_transcript_file):
	 '''A function to remove the surnames of survivors from transcripts'''
	 
	 new_surname = '[surname removed]'
	 total_count = 0
	 for i,element in enumerate(data):

	 	for surname in surnames:

		 	data[i],count=re.subn(surname, repl=new_surname, string=element)
		 	total_count = total_count+count
		
	 	#data[i]=element.replace(surname,new_surname)
	 if total_count == 0:
	 	
	 	part=int(path_to_transcript_file.split('_p')[1].split('.')[0].split('of')[0])
	 	if part ==1:

		 	print path_to_transcript_file.split('/')[-1]
		 	print shelfmark
		 	import regex
		 	res = regex.findall("("+surname+"){e<=2}", ' '.join(data))

		 	result =  [char for char in res if char.strip()[0].isupper()] 
		 	print ('In the transcripts:')
		 	print (set(result))
		 	print ('In the catalogue results:')
		 	print (surname)
		 	
	 return data

