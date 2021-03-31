import xmltodict
import pdb
import sys
from collections import OrderedDict
def transform_transcript_to_structured_unit(transcript_file_name):
	
	with open(transcript_file_name) as fd:
		doc = xmltodict.parse(fd.read())
	
	result=['']
	i=0

	for p in doc['transcription']['p']:
		paragraph=[]

		if p is not None:

			
			if type(p['span']) == list:
				for span in p['span']:
					if '#text' in span.keys():
						if span['#text'] is not None:
							paragraph.append(span['#text'])
					elif 'i' in span.keys():
						if span['i'] is not None:
							paragraph.append(span['i'])


					
			elif type(p['span']) == OrderedDict:
				if p['span']['#text'] is not None:
					paragraph.append(p['span']['#text'])
				

			
			
			paragraph=' '.join(paragraph)
			if paragraph[1:2].isupper() and paragraph[0] !='[':
				result.append(paragraph)
			else:
				result[len(result)-1]= result[len(result)-1] +' '+paragraph
			i=i+1
	
	
	result=[{'unit':element}for element in result if len(element)>0]

	return result
if __name__ == '__main__':
	name='9.1.xml'
	result = transform_transcript_to_structured_unit(name)
	pdb.set_trace()
	
