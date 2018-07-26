
> Scripts to transform Fortunoff transcripts into a python list of dictionaries ( [{'unit':'some text'},{'unit':'some text'}]. Transcripts, in txt format with each speech unit divided by empty space, were provided by Fortunoff Archive, and made by the private company named 3playmedia. Transcripts are verbatim, and contain timestamp, which is not processed here. Transcripts consist of multiple files, and they are joined in the output. Each unit in the original transcript file begins with either INTERVIEWER: or SUBJECT:. If multiple interviewers or multiple subjects are present, they are differentiated with numbers: "INTERVIEWER 1:" or "SUBJECT 2:". Some files were not created by following this standard; instead of INTERVIEWER 1:" or "SUBJECT 2:", the first name of the persons was used. This is corrected in parse.py with the help of a txt file containing a set of json string (/data/inputs/fortunoff/names_codes.txt). 
> 


## File Documentation


* **run.py**: Main function calling all sub functions
* **parse.py**:segment_transcript function that transforms the txt files into the output

## Input:
Transcripts in txt in the folder /data/inputs/fortunoff/transcripts/
## Output:
Python list of dictionaries ( [{'unit':'some text'},{'unit':'some text'}] uploaded to output_fortunoff_metadata structured_transcript field




