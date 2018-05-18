import json
import os
from pynlpl.formats import folia
import pdb
from nltk.tokenize import word_tokenize
import xml.dom.minidom as xmlprint
import ucto


def process(folia_doc):
    """Takes a folia doc string, which is divided into div and sentence units, and tokenizes each sentence. For tokenization, it uses the 
	ucto tokenizer. It returns the tokenized folia doc string. Each token get a unique id, which is the combination of the sentence id, and toke         position in the sentence.

        :param folia_doc: folia xml containing division level segmentation
        :return: folia xml with division and sentence segmentation, and tokens"""
    #initialize ucto
    configurationfile = "tokconfig-eng"
    tokenizer = ucto.Tokenizer(configurationfile)



    #get each sentence
    sentences=folia_doc.sentences()
    for sentence in sentences:
        #tokenize
        
        token_id=1
        tokenizer.process(sentence.text())
            
        for token in tokenizer:
            
            #create a new token

     #set the nospace attribute of each token           
            if token.nospace()==1:

                token_element=folia.Word(folia_doc,id=sentence.id+'_'+str(token_id),space=False)
            else:
                token_element=folia.Word(folia_doc,id=sentence.id+'_'+str(token_id))

            token_element.settext(unicode(token))

            sentence.add(token_element)

            token_id=token_id+1


    #Return the result in string
    return folia_doc


    #print xml.toprettyxml()

if __name__ == "__main__":
    #read sample input
    doc = folia.Document(file=os.getcwd()+'/data/output/sample_folia_sentences.xml')
    result=process(doc)
    #save it

    result.save(os.getcwd()+'/data/output/sample_folia_tokens.xml')






