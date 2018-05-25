import corenlp
import os, sys
constants_path = os.getcwd()
sys.path.insert(0, constants_path)
import constants
import pdb

os.environ["CORENLP_HOME"] = constants.CORENLP_HOME

def find_sentence_id(fragment,folia_xml):
	#start a parser

	try:
		folia_sentences=[element.text() for element in folia_xml.sentences()]
		
		with corenlp.CoreNLPClient(annotators="tokenize ssplit pos lemma".split(),properties={'timeout': '50000'}) as client:
			fragment_sentences = client.annotate(fragment)

		result_index=[]
		
		for sentence in fragment_sentences.sentence:


			fragment_sentence= corenlp.to_text(sentence)

			#find out if the sentence has been truncated
			
			if '...' in fragment_sentence:
				#find the longest text part
				parts=fragment_sentence.split('...')
				le = max(len(x) for x in parts)
				max_length=[x for x in parts if len(x) == le][0]
				#iterate through all sentences and try to identify the one where this is part

				matches=[match for match in folia_sentences if max_length in match]

				for part in parts:
					if len(part)>0:

						matches=[match for match in folia_sentences if part.strip() in match]
						
						position=folia_sentences.index(matches[0])+1
						result_index.append(position)

			else:
				

				result_index.append(folia_sentences.index(fragment_sentence)+1)
	except:
		return None

		

	return {'start_index':'s'+str(result_index[0]),'end_index':'s'+str(result_index[-1])}