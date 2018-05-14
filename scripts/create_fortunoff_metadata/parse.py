'''
Transform the Marc XML from UC Riverside to JSON and save in Mongo
'''

from utils.text import read, get_stopwords
from utils.api import save, config
from utils.dir import make_dir, rm_dir
from utils.marc import get_marc_fields
from collections import defaultdict, Counter
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag
from multiprocessing import Pool
from glob import glob
from random import random, randint
import codecs
import os
import xmltodict
import sys
import json
import pdb

##
# Globals
##

# inputs and global config
marc_xml_path = 'inputs/metadata/fortunoff-marc.xml' # path to metadata xml
plaintext_glob = 'inputs/plaintext/*' # path to plaintext testimonies
output_dir = 'outputs' # directory in which outputs will be stored
folia_dir = 'outputs/folia' # path where folia outputs will be stored
db = config['db'] # the database name to use when saving results
drop_db = True # whether to drop db before processessing records
max_records = 182 # max records to process (int|None)

# tree processing config
window_len = 40
n_parents = 40 # n parent nodes to search for child nodes
n_children = 40 # n children nodes to search for each parent node
n_trees = 10 # number of trees to build
min_leaves = 4 # minimum number of leaves per child node
leaf_words = 10 # number of words to include on either side of a leaf node term
min_children_per_root = 3 # minimum number of children a root node must have

# marc fields to process
fields = [
  {
    'number': '245',
    'letter': 'a',
    'label': 'testimony_title',
  },
  
  {
    'number': '100',
    'letter': 'a',
    'label': 'interviewee_name',
  },
  {
    'number': '520',
    'letter': 'a',
    'label': 'interview_summary',
  },
  {
    'number': '610',
    'letter': 'a',
    'label': 'camp_names_1',
    'type': list
  },
  {
    'number': '690',
    'letter': 'a',
    'label': 'camp_names_2',
    'type': list
  },
  {
    'number': '691',
    'letter': 'a',
    'label': 'camp_names_3',
    'type': list
  },
  {
    'number': '691',
    'letter': 'a',
    'label': 'ghetto_names',
    'type': list
  },
  {
    'number': '090',
    'letter': 'b',
    'label': 'testimony_id',
  },
  {
    'number': '260',
    'letter': 'b',
    'label': 'provenance',
  },
  {
    'number': '260',
    'letter': 'c',
    'label': 'recording_year',
  },
  {
    'number': '650',
    'letter': '0',
    'label': 'gender',
  }
]

##
# Testimony Metadata Functions
##

def get_marc_json():
  '''
  Parse MarcXML from UC Riverside and return a list
  of JSON records from that XML file
  '''
  records = []
  # marcxml was delivered from UC Riverside
  f = read(marc_xml_path, 'utf8')
  for idx, i in enumerate(f.split('<marc:record>')[1:]):
    if max_records and idx > max_records:
      continue
    xml = '<record>' + i.split('</marc:record>')[0] + '</record>'
    records.append(xmltodict.parse(xml))
 
  return records


def get_field(d):
  '''
  Given a dict `d`, find the MARC code within that
  d and return that code and its value
  @args:
    {obj} d: an object with MARC XML
  @returns:
    {obj} an object with the code and value from d
  '''
  if '@code' in list(d.keys()) and '#text' in list(d.keys()):
    return {
      'code': d['@code'],
      'text': d['#text'],
    }
  return None


def nest_marc_json(arr):
  '''
  Format the JSON parsed from MarcXML
  @args:
    {arr} arr: a list of json records
  @returns:
    {arr} a formatted list of json records
  '''
  records = []
  for idx, i in enumerate(arr):
    record_json = defaultdict(lambda: defaultdict(list))
    record = i['record']

    # 001 = estc_id, 009 = estc internal id
    for j in record['marc:controlfield']:
      tag = j['@tag']
      if tag in ['001', '009']:
        record_json[tag] = j['#text']

    # get record metadata from datafields
    for c, j in enumerate(record['marc:datafield']):
      tag = record['marc:datafield'][c]['@tag']
      if 'marc:subfield' in list(record['marc:datafield'][c].keys()):
        subfield = record['marc:datafield'][c]['marc:subfield']

        # some subfields are arrays of objects, others are objects
        if not isinstance(subfield, list):
          subfield = [subfield]

        for subfield_dict in subfield:
          field = get_field(subfield_dict)
          if field:
            record_json[tag][field['code']].append(field['text'])
          else:
            pass

    parsed = to_dict(record_json)
    records.append(parsed)
    save(parsed, 'marc')
    print(' * parsed', idx+1, 'marc records')
  return records


def to_dict(d):
  '''
  Convert a nested defaultdict to a dictionary
  @args:
    {defaultdict} d: a nested defaultdict
  @returns:
    {dict} a plain nested dictionary
  '''
  if isinstance(d, defaultdict):
    d = {k: to_dict(v) for k, v in d.items()}
  return d


def flatten_marc_json(records):
  '''
  Convert a list of documents in nested Marc JSON to
  a list of documents in flat JSON with app-specific
  keys
  '''
  parsed_records = []
  for i, record in enumerate(records):
    
    parsed = get_marc_fields(record, fields)
    parsed['gender'] = clean_gender(parsed['gender'])
    parsed['collection'] = 'Fortunoff'
    parsed['shelfmark'] = parsed['testimony_id']
    parsed['recording_year'] = clean_year(parsed['recording_year'])
    parsed['media_url'] = []
    parsed['thumbnail_url'] = ''
    parsed['camp_names']=parsed['camp_names_1']+parsed['camp_names_2']+parsed['camp_names_2']
    parsed['camp_names'] = clean_camp_names(parsed['camp_names_1'])
    parsed['provenance'] = clean_provenance(parsed['provenance'])
    parsed['ghetto_names']=clean_ghetto_names(parsed['ghetto_names'])
    
    #delete unnecessary fields
    parsed.pop('camp_names_1',None)
    parsed.pop('camp_names_2',None)
    parsed.pop('camp_names_3',None)
    
    # add the parsed record to the list of parsed records
    parsed_records.append(parsed)
  return parsed_records


def clean_gender(gender):
  '''
  @args:
    {arr} gender: a list of urls, one them is the gender attribute of interviews
  @returns:
    {arr} 'M' or 'F' or 
  '''

  #check if multiple gender info is present, in this case this is a couple

  gender_urls={'F':'http://id.loc.gov/authorities/subjects/sh85147274','M':'http://id.loc.gov/authorities/subjects/sh85083510'}
  
  if (gender_urls['F'] in gender) and (gender_urls['M'] in gender):
    gender =float('nan')
  elif (gender_urls['F'] in gender):
    gender='F'
  elif (gender_urls['M'] in gender):
    gender = 'M'
  else:
    gender =float('nan')
   
  return gender

def clean_year(recording_year):
  '''
  @args:
    {arr} recording_year: a string representing the year when the interview was recorded
  @returns:
    {arr} string representation of the year without the dot at the end
  '''
  
  return recording_year[0:4]

def clean_camp_names(camp_names):
  '''
  @args:
    {arr} camp_names: a list of strings
  @returns:
    {arr} a list of strings
  '''

  if len(camp_names)>0:
    result=[]
    for element in camp_names:
      if '(Concentration camp)' in element:
        result.append(element.split('(Concentration camp)')[0].strip())
    return result
  else:
    return camp_names


def clean_provenance(provenance):
  '''
  @args:
    {str} provenance: a string reflecting the provenance of a record
  @returns:
    {str}: a string
  '''
  return provenance.strip().rstrip(',')


def clean_ghetto_names(ghetto_names):
  '''
  @args:
    {str} provenance: a string reflecting the provenance of a record
  @returns:
    {str}: a string
  '''
  
  if len(ghetto_names)>0:
    result=[]
    for element in ghetto_names:
      if 'ghetto' in element:
        
        result.append(element.split('ghetto.')[0].strip())
    return result
  else:
    return ghetto_names

def format_marc():
  '''
  Return a list of dictionaries, where each dict represents a
  testimony and possesses the required keys
  '''
  marc_json = get_marc_json()

  marc_json_nested = nest_marc_json(marc_json)
  #ez kell
  marc_json_flat = flatten_marc_json(marc_json_nested)
  pdb.set_trace()
  return marc_json_flat


##
# Text Processing
##

def process_texts(records):
  '''
  Use multiple cores to process each input document's text content.
  Save only those records that have text content to the db.
  '''
  pool = Pool(6)
  for idx, result in enumerate(pool.imap(parse_record_text, records)):
    if not result:
      continue

    record = result['record']
    testimony_id = record['testimony_id']

    # update record fields
    record['html_transcript'] = result['html']
    record['recording_year'] = int(record['recording_year'])
    save(record, 'testimonies')

    # save the tokens
    save({'testimony_id': testimony_id, 'tokens': result['tokens']}, 'tokens')

    # save the folia to disk
    out_path = os.path.join(folia_dir, testimony_id + '.xml')
    with codecs.open(out_path, 'w', 'utf8') as out:
      out.write(result['folia'].strip())


def parse_record_text(record):
  '''
  Given a dict `record` with flat, app-specific keys, try to process
  the text fields (folia, html, and tokens) for this record. Return
  a bool indicating whether the record's text fields were parseable
  '''
  text = get_testimony_text(record['testimony_id'])
  if not text:
    return False

  # parse the document text
  paragraphs = get_paragraphs_and_sentences(text)
  html, tokens = get_html_and_tokens(paragraphs)
  folia = get_folia(record, paragraphs)

  return {
    'html': html,
    'tokens': tokens,
    'folia': folia,
    'record': record
  }


def get_html_and_tokens(paragraphs):
  '''
  Given a list of lists, where each higher-order list represents content
  from a paragraph and each sublist item represents content from the given
  paragraph, return html for this document
  '''
  sentence_id = token_id = 0
  html = ''; tokens = []

  for paragraph_id, paragraph in enumerate(paragraphs):
    html += '<p>'
    for sentence in paragraph:
      html += '<span id="s' + str(sentence_id) + '">' + sentence + '</span>'
      for token in word_tokenize(sentence):
        tokens.append({
          'token_index': token_id,
          'sentence_index': sentence_id,
        })
        token_id += 1
      sentence_id += 1
    html += '</p>'
  return html, tokens


def get_paragraphs_and_sentences(str):
  '''
  Given a `str`, return a list of lists where each higher-order list
  contains content from a paragraph, and each sublist is a list of
  sentences in the given paragraph.
  '''
  paragraphs = []
  for i in str.split('\n\n'):
    paragraphs.append(sent_tokenize(i))
  return paragraphs


def get_testimony_text(testimony_id):
  '''
  Given a testimony id, return the text for that record, if available
  '''
  hvt = testimony_id.replace('HVT-', '')
  return hvt_to_transcript.get(hvt, False)


def get_testimony_tokens(testimony_id):
  '''
  Given a testimony id, return the tokens for that record, if available
  '''
  hvt = testimony_id.replace('HVT-', '')
  return hvt_to_tokens.get(hvt, False)

##
# Folia Parsing
##

def get_folia(record, paragraphs):
  '''
  Given a testimony record and a list of lists, where each higher-order
  list represents content from a paragraph and each sublist item represents
  content from the given paragraph, return folia XML for this document
  '''
  folia = get_folia_top(record['testimony_id'])
  folia += get_folia_metadata(record['testimony_id'], record['shelfmark'])
  folia += '<text><div>'

  # add text content
  sentence_id = 0
  for paragraph_id, paragraph in enumerate(paragraphs):
    for sentence in paragraph:
      folia += '<s id="s' + str(sentence_id) + '">' + '\n'
      folia += '<t>' + sentence + '</t>' + '\n'

      # tokenize each word in the sentence and add to the folia
      words = word_tokenize(sentence)
      parts_of_speech = [p[1] for p in pos_tag(words)]
      for idx, word in enumerate(words):
        folia += '<w>' + '\n'
        folia += '<t>' + word + '</t>' + '\n'
        folia += '<pos class="' + parts_of_speech[idx] + '"/>' + '\n'
        folia += '<lemma class="' + word + '"/>' + '\n'
        folia += '</w>' + '\n'

      folia += '</s>' + '\n'
      sentence_id += 1
  folia += '</div></text></FoLiA>'
  return folia


def get_folia_top(testimony_id):
  '''
  Get the top of a folia document given a testimony
  @args:
    {str} testimony_id: the unique identifier for a testimony
  '''
  return '''
  <?xml version='1.0' encoding='utf-8'?>
  <FoLiA xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns="http://ilk.uvt.nl/folia"
    xml:id="{0}"
    version="1.5.1"
    generator="seed_folia_util">
  '''.format(testimony_id)


def get_folia_metadata(testimony_id, shelfmark):
  '''
  Get the metadata tags for a folia document given a testimony
  @args:
    {str} testimony_id: the unique identifier for a testimony
    {str} title: the title of a testimony
  '''
  return '''
  <metadata type="native">
    <annotations>
      <pos-annotation set="brown-tagset"/>
      <lemma-annotation set="treetagger"/>
    </annotations>
    <meta id="testimony_id">{0}</meta>
    <meta id="shelfmark">{1}</meta>
  </metadata>
  '''.format(testimony_id, shelfmark)


##
# Generate tree data
##

def build_tree_data(records):
  '''
  Given a list of dictionaries, where each dict has app-specific
  keys, fetch the raw, unformatted, tree data for the client
  '''
  trees = []
  raw_tree = fetch_raw_tree_data(records)
  for parent_idx, parent_word in enumerate(list(raw_tree.keys())):
    tree = get_tree(parent_word)
    max_parent_nodes = randint(5, 6) # max number of parent nodes for this tree
    for child_idx, child_word in enumerate(list(raw_tree[parent_word].keys())):
      max_leaf_nodes = randint(4, 8) # max number of leaf nodes for this tree
      if child_idx >= max_parent_nodes: continue
      child = {'label': child_word, 'children': []}
      for leaf_idx, i in enumerate(raw_tree[parent_word][child_word]):
        if leaf_idx >= max_leaf_nodes: continue
        # take one value from each testimony with this parent/child word pair
        testimony_id = list(i.keys())[0] # id for a testimony where `child_word` occurs
        position = i[testimony_id][0] # testimony_id_tokens[position] is `child_word`
        child['children'].append(get_node(testimony_id, position))
      tree['tree']['children'].append(child)
    if len(trees) != n_trees:
      trees.append(tree)
  if trees: save(trees, 'fragments')
  else: print(' ! warning: no trees were found')


def get_tree(parent_word):
  '''
  Given the root word for a tree, return the initial tree object
  @args:
    {str} parent_word: the root word for a tree
  @returns:
    {obj} the basic tree object
  '''
  return {
    'label': parent_word,
    'tree': {'label': parent_word, 'children': []}
  }


def get_node(testimony_id, position):
  '''
  Get a leaf node give a text's testimony id and the position of the token
  on which the node's window should center
  @args:
    {str} testimony_id: a unique id for a testimony
    {int} position: the index position of the token in `testimony_id`'s tokens
      where the node's window should center
  @return:
    {obj} an object with keys required for a child (fragment) node
  '''
  start_s_idx, end_s_idx = get_sentence_indices(testimony_id, position)
  return {
    'label': get_leaf_text(testimony_id, position),
    'testimony_id': testimony_id,
    'start_sentence_index': start_s_idx,
    'end_sentence_index': end_s_idx,
    'media_index': 0,
    'media_offset': 0,
    'children': []
  }


def get_sentence_indices(testimony_id, position):
  '''
  Given a testimony id and the position of a term in that document,
  fetch the start and end sentence indices for the described window
  '''
  return 0, 0


def get_leaf_text(testimony_id, position):
  '''
  Given a testimony id and the position of a term in that testimony,
  return a string that includes the full leaf content
  @args:
    {str} testimony_id: the unique id for a testimony
    {int} position: the offset position of a term of interest in that testimony
  @returns:
    {str} a string with the leaf node content from `position` + some words
      to the left and right
  '''
  words = get_testimony_tokens(testimony_id)
  start = max(0, position-leaf_words)
  end = min(len(words), position+leaf_words)
  built = ' '.join(words[start:end])
  for i in ['--', ',', '.', '?', '!', "n't"]:
    built = built.replace(' ' + i + ' ', i + ' ')
    built = built.strip().strip(i)
  built = built.replace(" '", "'")
  return '...' + built + '...'


def fetch_raw_tree_data(records):
  '''
  Given a list of dictionaries, where each dict has app-specific
  keys, fetch the raw, unformatted, tree data for the client

  TODO
  tree structure:
    d = {
      'parent_nodes': {
        parent_word: {
          child_word: {

          }
        }
      }
      'non_parent_nodes':
    }
  '''
  tree = defaultdict(lambda: defaultdict(list))
  term_counts, term_positions = find_prominent_terms(records)
  used_terms = set(term_counts.keys()) # don't allow words to be reused
  # find terms correlated with `parent_word`
  for root_idx, i in enumerate(term_counts.most_common(n_parents)):
    parent_word, count = i
    child_word_counts = Counter()
    child_word_positions = defaultdict(lambda: defaultdict(list))
    testimony_ids = term_positions[parent_word]
    # tokens at indices `positions` in `testimony_id` == parent_word
    for testimony_id in testimony_ids:
      positions = term_positions[parent_word][testimony_id]
      # get a child word that frequently appear with `parent_word`
      result = find_child_words(parent_word, testimony_id, positions)
      if not result:
        continue
      # add the counts and positions to the accumulator variables
      c_word_counts, c_word_positions = result
      child_word_counts += c_word_counts
      for c_word in c_word_positions:
        # TODO: guard against word reuse
        if c_word not in used_terms:
          used_terms.add(c_word)
        child_word_positions[c_word][testimony_id] = c_word_positions[c_word]
    # add the most correlated terms to the tree
    for child_word, _ in child_word_counts.most_common(n_children):
      # ensure the parent + child combo occurs in at least `min_leaves` documents
      if len(list(child_word_positions[child_word].keys())) < min_leaves:
        continue
      # specify the list of positions in which the child word occurs
      child_positions = child_word_positions[child_word].values()
      tree[parent_word][child_word] = child_positions
    # provide feedback
    print(' * processed', root_idx+1, 'root terms')
  return tree


def find_child_words(parent_word, testimony_id, positions):
  '''
  Given a parent word, a testimony id, the index positions where that word
  occurs in `testimony_id`, find the counts and positions
  of child terms that frequently occur near `parent_word`
  @args:
    {str} parent_word: the word for which we seek child words
    {str} testimony_id: the testimony id in which `parent_word` occurs
    [int] positions: the index positions in which `parent_word` occurs
      in the tokenized `testimony_id`
  '''
  child_word_counts = Counter()
  child_word_positions = defaultdict(lambda: defaultdict(list))
  words = get_testimony_tokens(testimony_id)
  if not words:
    return False
  # find nouns that often occur within `window_len` words of `parent_word`
  for idx in positions:
    start = max(0, idx-window_len)
    end = min(len(words) - 1, idx+window_len)
    child_words = words[start:end]
    parts_of_speech = pos_tag(child_words)
    for child_idx, child_word in enumerate(child_words):
      # only allow nouns
      if parts_of_speech[child_idx][1][0] != 'N':
        continue
      # apply other filtering criteria
      if not is_valid_child_term(parent_word, child_word):
        continue
      child_word_counts[child_word] += 1
      child_word_positions[child_word][testimony_id].append(start + child_idx)
  return child_word_counts, child_word_positions


def is_valid_child_term(parent_word, child_word):
  '''
  Return a bool indicating whether a given term can be used as a child term
  in the tree
  '''
  # don't allow child word to == parent term
  if child_word == parent_word:
    return False
  # don't use short words
  if len(child_word) < 4:
    return False
  # don't allow all uppercase words
  if all([char.isupper() for char in child_word]):
    return False
  # don't use stopwords
  if child_word.lower() in stopwords:
    return False
  return True


def find_prominent_terms(records):
  '''
  Given a list of dictionaries, where each dict has app-specific keys
  representing a testimony, return a counter of the nouns in each testimony
  and a mapping from noun to testimony_id to occurrences of that noun
  in the testimony (by 0-based index offset)

  return {
    word_a: {
      testimony_id_a: [idx_a, idx_b]
    },
    word_b: {
      testimony_id_b: [idx_b, idx_b]
    }
  }
  '''
  pool = Pool()
  all_counts = Counter()
  all_positions = defaultdict(lambda: defaultdict(list))
  for idx, result in enumerate(pool.imap(get_noun_positions, records)):
    print(' * processed term data in', idx+1, 'records')
    if not result:
      continue
    record, positions, counts = result
    all_counts += counts
    # update the master positions dict
    for term in positions:
      all_positions[term][record['testimony_id']] = positions[term]
  return all_counts, all_positions


def get_noun_positions(record):
  '''
  Given a record, return a counter of all the nouns in that record's
  text, and a mapping from each noun to its occurrences in the text
  '''
  positions = defaultdict(list)
  counts = Counter()
  text = get_testimony_text(record['testimony_id'])
  if not text:
    return None
  parts_of_speech = pos_tag(word_tokenize(text))
  for idx, i in enumerate(parts_of_speech):
    word, pos = i
    # only process nouns
    if pos[0] != 'N':
      continue
    # skip entirely uppercase terms (e.g. INTERVIEWER, SUBJECT...)
    if all([char.isupper() for char in word]):
      continue
    # skip small words
    if len(word) < 3:
      continue
    positions[word].append(idx)
    counts[word] += 1
  return record, positions, counts


##
# Output Helpers
##

def clear_outputs():
  '''
  Drop and repopulate output dirs and table
  '''
  for i in [output_dir, folia_dir]:
    rm_dir(i)
    make_dir(i)
  if drop_db:
    os.system('mongo ' + db + ' --eval "db.dropDatabase()"')


def save_mongo_archive():
  '''
  Save records in mongo to an archive for ingestion into app
  '''
  cmd = 'mongodump '
  cmd += '--archive=' + output_dir + '/lts.archive '
  cmd += '--db ' + db
  os.system(cmd)


##
# Fetch text documents
##

def get_hvt_to_transcript():
  '''
  Return a dictionary mapping each HVT number in the Fortunoff
  MARC to the testimony for that HVT number, if the testimony
  is available. Else map the HVT number to False
  '''
  d = {}
  for i in glob(plaintext_glob):
    hvt = i.split('_hvt_')[1].split('_')[0]
    if hvt in d:
      d[hvt] += read(i, 'utf-8') + '\n\n'
    else:
      d[hvt] = read(i, 'utf-8') + '\n\n'
  return d


def get_hvt_to_tokens():
  '''
  Create a mapping from HVT id to the case-sensitive tokens in that work
  '''
  d = {}
  for idx, i in enumerate(list(hvt_to_transcript.keys())):
    if max_records and idx >= max_records:
      continue
    d[i] = word_tokenize(hvt_to_transcript[i])
    print(' * tokenized', idx + 1, 'transcripts')
  return d


##
# Main
##

if __name__ == '__main__':

  #clear_outputs()

  # global data stores
  #hvt_to_transcript = get_hvt_to_transcript()
  #hvt_to_tokens = get_hvt_to_tokens()
  #stopwords = get_stopwords()

  # process records
  records = format_marc()
  #save it to the DB
  save(records, 'output_fortunoff_metadata')
  pdb.set_trace()
  #process_texts(records)
  #build_tree_data(records)
  #save_mongo_archive()