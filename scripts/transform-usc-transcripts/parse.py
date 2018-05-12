import xmltodict
import pdb
import sys
from collections import OrderedDict
def transform_transcript_to_structured_unit(transcript_file_name):
	
	with open(transcript_file_name) as fd:
		doc = xmltodict.parse(fd.read())
	
	result=[]
	i=0
	for p in doc['transcription']['p']:
		paragraph={'unit':[]}

		if p is not None:

			
			if type(p['span']) == list:
				for span in p['span']:
					if '#text' in span.keys():
						paragraph['unit'].append(span['#text'])
					elif 'i' in span.keys():
						paragraph['unit'].append(span['i'])


					
			elif type(p['span']) == OrderedDict:
				paragraph['unit'].append(p['span']['#text'])
				

			
				
			paragraph['unit']=' '.join(paragraph['unit'])
			result.append(paragraph)
			i=i+1
	if len(result) !=i:
		print 'problematic'
	return result
if __name__ == '__main__':
	name='/Users/gmt28/Documents/Workspace/Docker_Engine/varad/Yale_Projects/shoah-foundation-data/scripts/transform-usc-transcripts/inputs/93.2.xml'
	transform_transcript_to_structured_unit(name)