
import urllib
import json
import pdb
def words(context):
    """ Convert word array to string. """
    return " ".join(context['word'])

def print_utf8(s):
    print(''.join(i for i in s if ord(i) < 128))

def search(cqlQuery):
    """ Search and show hits. """
    url = "http://172.28.148.181:8082/blacklab-server-1.6.0/test_folia_data_2/hits?&patt=" + urllib.quote_plus(cqlQuery)+"&outputformat=json"
    

    print url
    f=urllib.urlopen(url)
    import pdb
    
    response = json.loads(f.read().decode('utf-8'))
   
    hits = response['hits']
    
   
    for hit in hits:
       # Show the document title and hit information
      
        print_utf8( words(hit['left']) + " [" + words(hit['match']) + "] " +  words(hit['right']) )
        print '\n\n\n'


if __name__ == "__main__":
    search('[lemma="which"]')
