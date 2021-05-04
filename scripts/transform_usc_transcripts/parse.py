import xmltodict
import pdb
import sys
from collections import OrderedDict
from xml.dom import minidom
import datetime
def transform_transcript_to_structured_unit(transcript_file_name,part):
	
	with open(transcript_file_name) as fd:
		doc = xmltodict.parse(fd.read())
	
	result=[{'text':''}]
	i=0

	for posit,p in enumerate(doc['transcription']['p']):
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
			result.append({'text':paragraph,'posit':posit})
			
			'''
			if paragraph[1:2].isupper() and paragraph[0] !='[':
				result.append({'text':paragraph,'posit':posit})
			else:
				result[len(result)-1]= {'text':result[len(result)-1]['text'] +' '+paragraph,'posit':posit}
			
			'''
			i=i+1
	
	
	result=[{'unit':element['text'],'posit':element['posit']} for element in result if len(element['text'])>0]
	p1 = minidom.parse(transcript_file_name)
	p_elements = p1.getElementsByTagName('p')
	final_result = []
	for element in result:
		element['time'] = datetime.timedelta(milliseconds=int(p_elements[element['posit']].getElementsByTagName('span')[0].getAttribute('m'))).seconds
		element['part']= part
		final_result.append(element)

	return final_result
if __name__ == '__main__':
	name='9.1.xml'
	result = transform_transcript_to_structured_unit(name,1)
	pdb.set_trace()
	
