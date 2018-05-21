# USC Metadata Transformation

> A script to extract information from data provided by USC SHOAH FOUNDATION. It is an xls file (archived as ), then saved to CSV (archived as). This CSV is to be copied to /data/inputs/usc/metadata/). Input data is transformed into a python dictionary, and then to app conformant mongo collection (output_usc_metadata), which is finally copied into the testimonies collection, the final output of all transformations. 
> 



## Quickstart to run only this transformation

* git clone https://github.com/YaleDHLab/shoah-foundation-data.git
* cd scripts/create\_usc\_metadata
* python run.py


## Issues

Report any issues to @toth12