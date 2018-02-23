# Shoah Foundation Data

> A script to extract information from the USHM databse

## File Documentation

* **run.py:** imports all the helper scripts and returns a Mongo collection specified in https://github.com/YaleDHLab/shoah-foundation-data/milestone/2. Takes > 7m15s to run
* **get\_camp\_names.py**: queries undress\_experiment for subject_topical. Look for the camp names under the pattern 
"camp\_name (Concentration camp), returns a dictionary with 529 entries, the keys being the 'id' of the interview and the value being an array with the names of the camps
* **get\_ghetto\_names.py**: queries undress\_experiment for subject\_topical. Within the subject\_topical array, any element that contained the substring "ghetto" was considered a ghetto. Returns a dictionary with 341 entries, the keys being the 'id' of the interview and the value being an array with the ghettos associated with the interview
* **get\_interview\_year.py**: queries undress\_experiment for the interview\_year field, returns a dictionary with 1462 entries, the keys being the 'id' of the interview and the value being the date it was recorded
* **get\_interview\_summary.py**: queries undress\_experiment for the interview\_year field. Strips the date string to get only the year. Returns a dictionary with 1065 entries, txzhe keys being the 'id' of the interview and the value being an array with the summary of the interviews
* **get\_gender.py:**: queries undress\_experiment for the interview\_summary field. Uses common pronouns as a proxy to define the gender of the interviewee given the interview's interview summary. Returns a dictionary with 1065 entries, the keys being the 'id' of the interview and the value being the gender of the interviewee, if any
* **get\_interview\_title.py:**: queries undress\_experiment for the title field.Returns a dictionary with 1514 entries, the keys being the 'id' of the interview and the value being the interview title
* **get\_interviewee_name.py:**: queries undress\_experiment for the interviewee field (1301 fields have it). If not found, check if there is a summary (summary begins with the name of the interviewee) and use it as a backup method (201 names found through this backup method). Returns a dictionary with 1503 entries, the keys being the 'id' of the interview and the value being the interviewee name. 
* **get\_provenance.py**: queries undress\_experiment for the historical provenance field, returns a dictionary with 1514 entries, the keys being the 'id' of the interview and the value being the provenance

* **sample**: a folder with sample documents of the undress_experiment collection and a result.txt that shows the resulting collection

## Quickstart

* git clone https://github.com/YaleDHLab/shoah-foundation-data.git
* cd scripts/create\_ushmm\_metadata
* python run.py


## Issues

Report any issues to @gabrielsaruhashi