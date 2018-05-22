# USHMM Metadata Transformation

> A script to extract information from data provided by USHMM. It is a Mongo Collection gathered by downloading all testimonies that are transcribed and publicly available and then filtering them to find only the English ones. (archived as input_ushmm.json to be copied to data/inputs/ushmm/metadata).Some of the data set has been preprocessed manually (gender of interviwee, missing pieces of information in catalogue records, (interview year, video url, etc)), they are archived as (genderize_info.json,USHM_missing_records_Eliot.csv). The processing is done by including data from these two data files. The process is logged.
> 


## File Documentation

* **run.py:** imports all the helper scripts and returns a Mongo collection specified in https://github.com/YaleDHLab/shoah-foundation-data/milestone/2. It uses a manually written spreadsheet as a backup method in case no information is found
* **download_htmls.py**: downloads the html pages of each of the 1514 databases in order to make the media extraction easier later
* **get\_camp\_names.py**: queries undress\_experiment for subject_topical. Look for the camp names under the pattern "camp\_name (Concentration camp), returns a dictionary with 529 entries, the keys being the 'id' of the interview and the value being an array with the names of the camps
* **get\_ghetto\_names.py**: queries undress\_experiment for subject\_topical. Within the subject\_topical array, any element that contained the substring "ghetto" was considered a ghetto. Returns a dictionary with 341 entries, the keys being the 'id' of the interview and the value being an array with the ghettos associated with the interview
* **get\_interview\_year.py**: queries undress\_experiment for the interview\_year field, returns a dictionary with 1462 entries, the keys being the 'id' of the interview and the value being the date it was recorded
* **get\_interview\_summary.py**: queries undress\_experiment for the interview\_year field. Strips the date string to get only the year. Returns a dictionary with 1065 entries, txzhe keys being the 'id' of the interview and the value being an array with the summary of the interviews
* **get\_gender.py:**: queries undress\_experiment for the interview\_summary field. Uses common pronouns as a proxy to define the gender of the interviewee given the interview's interview summary. Returns a dictionary with 1065 entries, the keys being the 'id' of the interview and the value being the gender of the interviewee, if any. It uses the Genderize API as a backup in case no gender could be determined
* **get\_interview\_title.py:**: queries undress\_experiment for the title field.Returns a dictionary with 1514 entries, the keys being the 'id' of the interview and the value being the interview title
* **get\_interviewee_name.py:**: queries undress\_experiment for the interviewee field (1301 fields have it). If not found, check if there is a summary (summary begins with the name of the interviewee) and use it as a backup method (201 names found through this backup method). Returns a dictionary with 1503 entries, the keys being the 'id' of the interview and the value being the interviewee name. 
* **get\_provenance.py**: queries undress\_experiment for the historical provenance field, returns a dictionary with 1514 entries, the keys being the 'id' of the interview and the value being the provenance
* **get\_shelfmark.py**: queries undress\_experiment for the rgn field, returns a dictionary with 1514 entries, the keys being the 'id' of the interview and the value being the shelfmark
* **get\_videos.py**: helper functions related to the video extraction task, including generating the url for the given interview, retrieving thumbnails and scraping the HTML for any video or audio interviews (.mp3 or .mp4)
* **sample**: a folder with sample documents of the undress_experiment collection and a result.txt that shows the resulting collection



## Issues

Report any issues to @toth12