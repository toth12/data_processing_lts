# Fortunoff Metadata Transformation

> A script to extract information from data provided by Fortunoff Archive Yale University. It is a Marc XML file (archived as fortunoff.marcxml, and to be copied to /data/inputs/fortunoff/metadata/) transformed into a python dictionary, and then to app conformant mongo collection (output_fortunoff_metadata), which is finally copied into the testimonies collection, the final output of all transformations. 
> 



## Quickstart to run only this transformation

* git clone https://github.com/YaleDHLab/shoah-foundation-data.git
* cd scripts/create\_fortunoff\_metadata
* python parse.py


## Issues

Report any issues to @toth12