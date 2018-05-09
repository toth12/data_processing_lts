import pdb

def segment_transcript(path_to_transcript_file):
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
 input_data=[element.strip() for element in input_data if element !='\n']
 
 #process the transcript line by line
 for line in input_data:
 	#check if a line is the beginning of segment by checking whether the second character of the line is uppercase
 	if not line[1:2].islower():
 		output.append({'unit':line})
 	#if it is not the beginning of a new segment, add it to thew last segment
 	else:
 		output[len(output)-1]['unit']=output[len(output)-1]['unit']+' '+line


 
 return output