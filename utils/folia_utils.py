from pynlpl.formats import folia
import pdb


def read_folia_xml(filename):
	doc = folia.Document(file=filename,encoding='utf-8')
	return doc

def get_tokens(filename):
	folia_xml=read_folia_xml(filename)
	tokens=folia_xml.words()
	result=[token.text() for token in tokens]
	return result

def count_tokens(filename):
	folia_xml=read_folia_xml(filename)
	tokens=folia_xml.words()
	result=[token.text() for token in tokens]
	return len(result)

def get_counts(filename):
	result={}
	folia_xml=read_folia_xml(filename)
	tokens=folia_xml.words()
	result['tokens']=len([token.text() for token in tokens])
	result['divisions']= len([ div for  div in folia_xml.select(folia.Division)])
	return result

