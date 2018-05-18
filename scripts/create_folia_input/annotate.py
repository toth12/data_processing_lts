from stanfordcorenlp import StanfordCoreNLP
import json
import pdb
text ="Hi, my name is Gabor. How are you?"
props={'annotators': 'tokenize,ssplit,pos,lemma,ner','pipelineLanguage':'en','outputFormat':'json'}
nlp = StanfordCoreNLP('http://localhost', port=8090)

result= json.loads(nlp.annotate(text, properties=props))



result['sentences'][0]['tokens'][0]


pdb.set_trace()