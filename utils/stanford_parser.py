import os
import requests
import json


def annotate(text):
	'''Utility function that sentence split, tokenize and pos tag an English text'''
	
	#set up the properties of the annotator
	props={'annotators':'tokenize,ssplit,pos,lemma'}

	#set the encoding of the annotator
	requests.encoding = 'utf-8'
	#make a request
	r = requests.post('http://localhost:9000/', params={'properties':json.dumps(props)}, data=text.encode('utf-8'))
    
    #transform the result to python dict
	result=json.loads(r.text,encoding='utf-8')
	
	return result


def sentence_to_text(sentence):
    """
    Helper routine that converts a sentence dictionary returned by Stanford Parser into the original input text.
    """
    text = ""
    for i, tok in enumerate(sentence['tokens']):
        if i != 0:
            text += tok['before']
        text += tok['originalText']
    return text

def start_stanfordcornlp_server(path_to_stanford_corenlp):
	"""
    Helper routine that starts Stanford Parser in the background as daemon
    """
	start_command='java -mx12g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -thread 4 -port 9000 -timeout 15000'
	complete_start_command='cd '+ path_to_stanford_corenlp +' && '+start_command+' &'
	os.system(complete_start_command)



if __name__ == '__main__':
	path='/Users/gmt28/Documents/Workspace/Docker_Engine/varad/Yale_Projects/shoah-foundation-data-restored/shoah-foundation-data/lib/stanford-corenlp'
	start_stanfordcornlp_server(path)