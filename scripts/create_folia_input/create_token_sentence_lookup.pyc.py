�
̚�Zc           @   s�   d  d l  Z  d  d l Z d  d l m Z d  d l Z d  d l m Z d  d l j j	 Z
 d  d l Z d  d l m Z d  d l Z e j j d d d � Z e j j d e � d  d l Z d �  Z e d	 k r� e j d
 e j �  d � Z e e d � Z n  d S(   i����N(   t   folia(   t   word_tokenize(   t   BeautifulSoups   ..t   utilsi    c         C   sm   |  j  t j � } g  t | � D]0 \ } } i | d 6t | j j d � d 6^ q } i | d 6| d 6} | S(   s�  Takes a folia xml, which is divided into div, sentence and token units, and creates a token sentence id look up dictionary. The position of token in the entire document is the dictionary key, the assigned value is the
    is the unique id of the sentence in which it occur.

    :param folia_doc_string: folia xml containing division, sentence and token level segmentation
    :return: look up dictionaryt   token_indexi   t   sentence_indext   testimony_idt   tokens(   t   selectR    t   Wordt	   enumeratet   intt   parentt   id(   t	   folia_docR   R   t   indext   tokent   look_up_indext   look_up_table(    (    sr   /home/varad/project/Yale_Projects/shoah-foundation-data/scripts/create_folia_input/create_token_sentence_lookup.pyt   process   s    Ct   __main__t   files(   /data/output/sample_folia_pos_tagged.xmlt   some_id(   t   jsont   ost   pynlpl.formatsR    t   pdbt   nltk.tokenizeR   t   xml.dom.minidomt   domt   minidomt   xmlprintt   uctot   bs4R   t   syst   patht   joint   helper_patht   insertt   helper_mongot   hR   t   __name__t   Documentt   getcwdt   doct   result(    (    (    sr   /home/varad/project/Yale_Projects/shoah-foundation-data/scripts/create_folia_input/create_token_sentence_lookup.pyt   <module>   s   	