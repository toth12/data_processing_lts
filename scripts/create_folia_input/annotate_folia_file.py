import json
import os
from pynlpl.formats import folia
import pdb
import xml.dom.minidom as xmlprint
from stanfordcorenlp import StanfordCoreNLP
from unidecode import unidecode
from slugify import slugify
import constants



stanford_nlp=constants.STANFORD_CORE_NLP_JAR





def annotate(folia_doc):
    """Takes a folia doc string, which is divided into div units, and splits the text of each unit into sentences, adds a unique id to each sentence 
	with a prefix. Returns a new folia doc string which contains also sentence level division. For sentence tokenization it uses NLTK.
    :param folia_doc: folia xml containing division level segmentation
    :param prefix: prefix to be used when adding a unique id to each sentence
    :return: folia xml with division and sentence segmentation
    """


    #declare annotation
    folia_doc.declare(folia.PosAnnotation,set='brown-tagset')
    folia_doc.declare(folia.LemmaAnnotation,set='treetagger')
    #get the first level text
    text=folia_doc.select(folia.Text)
    sentence_id=1
    nlp = StanfordCoreNLP('http://localhost', port=8090)
    props={'annotators': 'tokenize, pos, lemma','pipelineLanguage':'en','outputFormat':'json'}

    #get each sentence
    sentences=folia_doc.sentences()
    for sentence in sentences:
        #tokenize
        
        token_id=1
        try:
            result= json.loads(nlp.annotate(slugify(sentence.text()), properties=props))
        except:
            pdb.set_trace()
        for token in result['sentences'][0]['tokens']:
            
            
            #create a new token

     #set the nospace attribute of each token           
            if not token['after']==' ':

                token_element=folia.Word(folia_doc,id=sentence.id+'_'+str(token_id),space=False)
            else:
                token_element=folia.Word(folia_doc,id=sentence.id+'_'+str(token_id))

            token_element.settext(unicode(token['word']))

            #annotate it

            token_element.add(folia.PosAnnotation, set='brown-tagset',cls=token['pos'])
            token_element.add(folia.LemmaAnnotation, set='treetagger',cls=token['lemma'])

            sentence.add(token_element)

            token_id=token_id+1


    #Return the result in string
        
    return folia_doc


if __name__ == "__main__":
    #read sample input
    doc = folia.Document(file=os.getcwd()+'/data/output/sample_folia_divisions.xml')
    result=annotate(doc)

    #save it

    result.save(os.getcwd()+'/data/output/sample_folia_sentences.xml')








