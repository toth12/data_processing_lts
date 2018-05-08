import pdb

def segment_transcript(transcript_file):
 input_data=open(transcript_file).readlines()
 output=[]
 input_data=[element.strip() for element in input_data if element !='\n']
 for line in input_data:
 	if not line[1:2].islower():
 		output.append({'unit':line})
 	else:
 		output[len(output)-1]['unit']=output[len(output)-1]['unit']+' '+line


 
 return output