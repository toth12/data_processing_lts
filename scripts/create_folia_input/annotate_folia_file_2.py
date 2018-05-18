import simplejson as json
import os
from pynlpl.formats import folia
import pdb
import xml.dom.minidom as xmlprint
from stanfordcorenlp import StanfordCoreNLP
from unidecode import unidecode
from slugify import slugify
import unidecode
import corenlp

os.environ["CORENLP_HOME"] = r'/Users/gmt28/Documents/Workspace/Docker_Engine/varad/Yale_Projects/shoah-foundation-data-restored/shoah-foundation-data/lib/stanford-corenlp-full-2018-02-27'






def annotate(text,client):
    """Takes a folia doc string, which is divided into div units, and splits the text of each unit into sentences, adds a unique id to each sentence 
	with a prefix. Returns a new folia doc string which contains also sentence level division. For sentence tokenization it uses NLTK.
    :param folia_doc: folia xml containing division level segmentation
    :param prefix: prefix to be used when adding a unique id to each sentence
    :return: folia xml with division and sentence segmentation
    """


    
    '''nlp = StanfordCoreNLP('http://localhost', port=8090)
    props={'annotators': 'tokenize,ssplit, pos, lemma','pipelineLanguage':'en','outputFormat':'json'}
    result=nlp.annotate(unidecode.unidecode(text), properties=props)'''

    #with corenlp.CoreNLPClient(annotators="tokenize ssplit pos lemma".split(),properties={'timeout': '50000'}) as client:
    result = client.annotate(text)
    '''
    pdb.set_trace()
    result= json.loads(result)

    '''
    
    
    
    #get each sentence
    return result

if __name__ == "__main__":
    #read sample input
    doc = folia.Document(file=os.getcwd()+'/data/output/sample_folia_divisions.xml')
    result=annotate(doc)

    #save it

    result.save(os.getcwd()+'/data/output/sample_folia_sentences.xml')


