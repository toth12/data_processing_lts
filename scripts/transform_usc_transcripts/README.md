
> Scripts to transform USC transcripts into a python list of dictionaries ( [{'unit':'some text'},{'unit':'some text'}]. Transcripts, in xml format, were provided by USC. Transcripts are verbatim, and contain timestamp, which is not processed here. Transcripts consist of multiple files, and they are joined in the output (different parts are in /data/inputs/usc/transcripts/USC_Shoah_Foundation_Transcripts_list.csv". 
> 


## File Documentation


* **run.py**: Main function calling all sub functions
* **parse.py**:transform_transcript_to_structured_unit function that transforms the xml files into the output

## Input:
Transcripts in xml in the folder /data/inputs/usc/transcripts/
## Output:
Python list of dictionaries ( [{'unit':'some text'},{'unit':'some text'}] uploaded to output_usc_metadata structured_transcript field




