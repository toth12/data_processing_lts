# Shoah Foundation Data

> A script to extract information from the USHM databse

## File Documentation

* **run.py:** imports all the helper scripts and returns a Mongo collection specified in https://github.com/YaleDHLab/shoah-foundation-data/milestone/2 
* **get\_camp\_names.py**: queries undress\_experiment for subject_topical. Look for the camp names under the pattern 
"camp\_name (Concentration camp), returns a dictionary with 529 entries, the keys being the 'id' of the interview and the value being an array with the names of the camps
* **get\_ghetto\_names.py**: queries undress\_experiment for subject\_topical. Within the subject\_topical array, any element that contained the substring "ghetto" was considered a ghetto. Returns a dictionary with 341 entries, the keys being the 'id' of the interview and the value being an array with the ghettos associated with the interview
* **get\_interview\_year.py**: queries undress\_experiment for the interview\_year field, returns a dictionary with 1462 entries, the keys being the 'id' of the interview and the value being the date it was recorded
* **get\_interview\_summary.py**: queries undress\_experiment for the interview\_year field,returns a dictionary with 1065 entries, the keys being the 'id' of the interview and the value being an array with the summary of the interviews
* **get\_gender.py:**: queries undress\_experiment for the interview\_summary field. Uses common pronouns as a proxy to define the gender of the interviewee given the interview's interview summary. Returns a dictionary with 1065 entries, the keys being the 'id' of the interview and the value being the gender of the interviewee, if any

* **sample**: a folder with sample documents of the undress_experiment collection

## Quickstart

* git clone https://github.com/YaleDHLab/shoah-foundation-data.git
* cd scripts/create\_ushmm\_metadata
* python run.py


## Issues

Report any issues to @gabrielsaruhashi