import urllib
import time
import pprint
import sys, os
import constants
import helper_mongo as h
pp = pprint.PrettyPrinter(indent=4)

# database info
DB = constants.DB
COLLECTION = constants.INPUT_COLLECTION_USHMM

# URL for the USHM website
BASE_URL = 'https://collections.ushmm.org/search/catalog/'

# types of video
MP3 = ".mp3"
MP4 = ".mp4"
NO_MEDIA = "no media"

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
    vids = [w.replace(',', '').strip("'") for w in html.split() if w.endswith('.mp4\',')]

    # if there are .mp4 videos in the page
    if vids:
        return vids, MP4

    # use .mp3 as backup method
    audios = [w.replace(',', '').strip("'") for w in html.split() if w.endswith('.mp3\',')]
    
    if audios:
        return audios, MP3
    
    else:
        return [], NO_MEDIA

def getImages(html):
    """
    Returns one thumbnail from the website
    """
    # look for thumbnails
    images = [w.replace(',', '').strip("'") for w in html.split() if ('.jpeg' in w or '.jpg' in w) and '=' not in w]
    
    # return one image to be used
    if images:
        return images[0]
    else:
        return None

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
    url = getWebsite('irn511346')
    html = getHTML(url)
    vid = getVideos(html)
    pprint.pprint(vid)
    #htmls = getHTMLs()
    #pprint.pprint(htmls)
