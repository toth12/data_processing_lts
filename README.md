# Shoah Foundation Data

> A script to extract information from the USHM databse

## File Documentation

* **run.py:** imports all the helper scripts and returns a Mongo collection specified in https://github.com/YaleDHLab/shoah-foundation-data/milestone/2 
* **get\_camp\_names.py**: queries undress\_experiment for the camp names under the pattern 
"camp\_name (Concentration camp), returns a dictionary with 529 entries, the keys being the 'id' of the interview and the value being an array with the names of the camps
* **get\_interview\_year.py**: queries undress\_experiment for the interview\_year field, returns a dictionary with 1462 entries
* **get\_interview\_summary.py**: queries undress\_experiment for the interview\_year field,returns a dictionary with 1065 entries, the keys being the 'id' of the interview and the value being an array with the summary of the interviews

## Quickstart

* git clone https://github.com/YaleDHLab/shoah-foundation-data.git
* cd scripts/create\_ushmm\_metadata
* python run.py


## Issues

Report any issues to @gabrielsaruhashi