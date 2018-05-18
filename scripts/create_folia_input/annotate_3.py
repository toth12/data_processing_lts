import os
import corenlp
import pdb

os.environ["CORENLP_HOME"] = r'/Users/gmt28/Documents/Workspace/Docker_Engine/varad/Yale_Projects/shoah-foundation-data-restored/shoah-foundation-data/lib/stanford-corenlp-full-2018-02-27'
text = "Gábor was born."

# We assume that you've downloaded Stanford CoreNLP and defined an environment
# variable $CORENLP_HOME that points to the unzipped directory.
# The code below will launch StanfordCoreNLPServer in the background
# and communicate with the server to annotate the sentence.
client=corenlp.CoreNLPClient(annotators="tokenize ssplit lemma".split())
result = client.annotate(text)
pdb.set_trace()
print (corenlp.to_text(result.sentence[0].token[0]))