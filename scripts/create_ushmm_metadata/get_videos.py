import urllib
import time
import pprint
import sys, os
import constants
helper_path = os.path.join("..", "..", "utils")
sys.path.insert(0, helper_path)
import helper_mongo as h
pp = pprint.PrettyPrinter(indent=4)

# database info
DB = constants.DB
COLLECTION = constants.INPUT_COLLECTION

# URL for the USHM website
BASE_URL = 'https://collections.ushmm.org/search/catalog/'

def getHTML(url):
    """ 
    Returns the HTML page for the USHM page specified 
    by the given url with an interview id
    """
    html = urllib.urlopen(url).read().decode('utf8')
    return html

def getVideos(html):
    """
    Returns for all the .mp3 and .mp4 urls in
    the docs
    """
    vids = [w.replace(',', '').strip("'") for w in html.split() if '.mp4' in w or '.mp3' in w]
    return vids

def getImages(html):
    """
    Returns all thumbnails on the website
    """
    images = [w.replace(',', '').strip("'") for w in html.split() if ('.jpeg' in w or '.jpg' in w) and '=' not in w]
    return images

def getWebsite(_id):
    """
    Returns the website url for the given interview
    """
    return BASE_URL + _id


def getHTMLs():
    """
    Returns a dictionary with the interview_year of 1462 entries in
    the USHMM database
    """

   # query for interview years
    result = h.query(DB, COLLECTION,  {'website_html': {'$exists': 'true'}}, {'website_html': 1, 'id': 1})
    
    # initialize dictionary
    interviews_html = dict()

    # go through all the interviews
    for interview in result:
        key = interview.get('id')
        
        # access date object
        interviews_html[key] = interview.get('website_html')

    return interviews_html

if __name__ == "__main__":
    """
    url = getWebsite('irn516732')
    html = getHTML(url)
    pprint.pprint(html)
    getImages(html)
    """
