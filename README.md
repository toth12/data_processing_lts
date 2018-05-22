# Let Them Speak Data Processing

> Let Them Speak is a joint project by Gabor M. Toth and Yale Fortunoff Archive and DH Lab. It builds a data edition and text analysis tools to study testimonies of Holocaust survivors. Let Them Speak is empowered by a corpus engine (Blacklab) and a Mongo DB. (link to project rep) This repository is a collection of python scripts to transform two types of raw data (catalogue data and interview transcripts) into the input (link) of the engine and the DB. Raw data are provided by three institutions:

> * Fortunoff Archive Yale University
> * United States Holocaust Memorial Museums
> * USC Shoah Foundation

> Transformation of each data set is desribed in the README of the corresponding folder. (See /scripts/)


## Operating System Requirements

This project can be run on both Linux and Mac; but to process a few hundred raw transcripts in DOC, it uses Mac Os Textutil. This process is skipped if the library is not available (see scripts/transform_ushmm_transcripts/run.py). 

## Python version

This project is running with python2.

## Dependencies

First you'll need to install a Mongo DB. 

Linux:

```bash
sudo apt-get install mongo
```

Mac:

```bash
brew install mongo
```

Second you'll need to install the requirements:

```bash
pip install -r requirements
```

In case both python 2 and python 3 are installed:

```bash
pip2 install -r requirements
```

Then download Stanford Parser most recent version (https://nlp.stanford.edu/software/lex-parser.shtml#Download) and then unzip it and copy it to lib/stanford-corenlp (lib/stanford-corenlp is not part of the repo, you need to create it):

Unzip the data file and copy it to the main folder, this will create both input folders and the output folders.


## Running the transformations

Once the dependencies are settled, you can run all transformations in the main project folder by:

```bash
python run.py
```

Or if both python3 and python2 are installed:


```bash
python2 run.py
```

That will start a pipeline of 2x3 transformations:

> * transformation of catalogue data in various data formats (xls,marcXML,mongo collection dump) into the datamodel of the app 
> * transformation of transcripts (in XML, plain text, PDF, DOC, DOCX) into annotated FOLIA XML

The pipeline finishes with a test.

## Input

The input data is to be copied to data/input/{collection_siglum}. Each input data is described in the README of folders for different transformations. This repo comes with input data ready. Unzip the input data and copy to data/.

## Output

It is in data/output. The output of transformations is the input of the engine empowering Let Them Speak. First, it is two Mongo collections (see the model in DataModel.md) saved in /data/output/db/lts.archive:

> * testimonies
> * tokens

Second, it is a collection of annotated folia files in /data/output/folia/. 

Third, log of documents that could not be processed are in /data/outputs/.


