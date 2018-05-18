import json
import os
from pynlpl.formats import folia
import pdb
from nltk.tokenize import word_tokenize
import xml.dom.minidom as xmlprint
import ucto
from components import postagger_component as pt

def process(folia_doc,pos_tagger):
    """Takes a folia doc string, which is divided into div, sentence and token units, and lemmatize and pos tag each. 
        For POS tagging it uses tree tagger.
        :param folia_doc: folia xml containing division, sentence and token level segmentation
        :return: folia xml with pos tagging and lemmatization"""

 
    #declare annotation
    folia_doc.declare(folia.PosAnnotation,set='brown-tagset')
    folia_doc.declare(folia.LemmaAnnotation,set='treetagger')

    #get each sentence
    sentences=folia_doc.sentences()
    
    for sentence in sentences:

        #todo: decide whether you want to annotate in lowercase
        words=[words.text() for words in list(sentence.words())]
        annotated=pos_tagger.process_input([words])
        for i,element in enumerate(annotated[0]):

            #todo: prepare for scenarios when for instance pos tag is missing
            #add pos annotation

            sentence.words(i).add(folia.PosAnnotation, set='brown-tagset',cls=element[1])
            sentence.words(i).add(folia.LemmaAnnotation, set='treetagger',cls=element[2])

    #return the result in string
    return folia_doc

if __name__ == "__main__":
    #read sample input
    doc = folia.Document(file=os.getcwd()+'/data/output/sample_folia_tokens.xml')
    #todo: decide what the input should be for this function
    result=process(doc)

    #save it

    result.save(os.getcwd()+'/data/output/sample_folia_pos_tagged.xml')

#java -cp core/target/blacklab-1.6.0.jar nl.inl.blacklab.tools.IndexTool create test_folia_data_2 test_folia_data_2/sample_folia_pos_tagged.xml folia





