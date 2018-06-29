# USHMM Data

> A set of scripts to transform USHMM transcripts into a python list of dictionaries ( [{'unit':'some text'},{'unit':'some text'}]. Transcripts were provided by USHMM in different batches. The first batch contained all transcripts in PDF files (data/inputs/ushmm/pdf_transcripts), the second batch contained some but not all transcripts in DOCX and DOC format. To construct the input, first the DOCX and DOC files were used. The dataset was divided into different parts:
> 
> 1. Transcripts in DOCX that have one of these shelfmarks: RG-50.030, RG-50.106, and RG-50.549; these shelfmarks are part of the USHMM's core collection, and the transcription is supposed to follow a template (see transcription-templates/ushmm_transcription_template); this part of the data is named core_docx, all functions working with this data are named accordingly.
> 2. Transcripts in DOC that have one of these shelfmarks: RG-50.030, RG-50.106, and RG-50.549; these shelfmarks are part of the USHMM's core collection, and the transcription is supposed to follow a template (see transcription-templates/ushmm_transcription_template); this part of the data is named core_doc, all functions working with this data are named accordingly. When processing them, these transcripts are first transformed to DOCX.
> 3. Transcripts in DOCX that do not have one of these shelfmarks: RG-50.030, RG-50.106, and RG-50.549; these shelfmarks are part of the USHMM's core collection, hence any transcript without these shelfmarks are not part of USHMM's core collection. Transcripts do not follow any explicit template; this part of the data is named non_core_docx, all functions working with this data are named accordingly.
> 4. Transcripts in DOC that do not have one of these shelfmarks: RG-50.030, RG-50.106, and RG-50.549; these shelfmarks are part of the USHMM's core collection, hence any transcript without these shelfmarks are not part of USHMM's core collection. Transcripts do not follow any explicit template; this part of the data is named non_core_doc, all functions working with this data are named accordingly. When processing them, these transcripts are first transformed to DOCX.
> 5. Transcripts in PDF (without either DOC or DOCX file) that do not have one of these shelfmarks: RG-50.030, RG-50.106, and RG-50.549; these shelfmarks are part of the USHMM's core collection, hence any transcript without these shelfmarks are not part of USHMM's core collection. Transcripts do not follow any explicit template; this part of the data is named non_core_docx_made_from_pdf, all functions working with this data are named accordingly. When processing them, these transcripts were first transformed to DOCX by means of ADOBE ACROBAT (original pdf files in data/inputs/ushmm/pdf_transcript_not_available); the docx files (in data/inputs/ushmm/pdf_transcript_not_available_in_doc_transformed_to_docx) are the input of processing.
> 6. Transcripts in PDF (without either DOC or DOCX file) that have one of these shelfmarks: RG-50.030, RG-50.106, and RG-50.549; these shelfmarks are part of the USHMM's core collection, and the transcription is supposed to follow a template (see transcription-templates/ushmm_transcription_template); this part of the data is named core_docx_made_from_pdf, all functions working with this data are named accordingly. When processing them, these transcripts were first transformed to DOCX by means of ADOBE ACROBAT (original pdf files in data/inputs/ushmm/pdf_transcript_not_available); the docx files (in data/inputs/ushmm/pdf_transcript_not_available_in_doc_transformed_to_docx) are the input of processing.

## File Documentation


* **create_tracker.py**: creates a collection that tracks the processing of each shelfmark; processes below update the status field in the tracker with either "Processed" or "Unprocessed" values. This logs the entire process.
* **transcribe_core_doc.py**: transforms all files that are part of group 2 above. It uses textutil to create docx file which is used as input
* **transcribe_core_docx.py**: transforms all files that are part of group 1 above. 
* ***transcribe_non_core_doc.py**: transforms all files that are part of group 4 above. It uses textutil to create docx file which is used as input
* **transcribe_non_core_docx.py**: transforms all files that are part of group 4 above.
* ***transcribe_non_core_docx_made_from_pdf.py**: transforms all files that are part of group 5 above. As input it uses the docx version of the pdf files.
* ***transcribecore_docx_made_from_pdf.py**: transforms all files that are part of group 6 above. As input it uses the docx version of the pdf files.

## Input:
Transcripts in DOCX, DOC, or PDFs transformed to DOCX

## Output:

Python list of dictionaries ( [{'unit':'some text'},{'unit':'some text'}] uploaded to output_ushmm_metadata structured transcript field

## Quickstart


* git clone https://github.com/YaleDHLab/shoah-foundation-data.git
* cd scripts/transform\_ushmm\_transcripts_to_structured_units
* python run.py



