# Let Them Speak Data Processing

> Let Them Speak is a joint project by Gabor M. Toth and Yale Fortunoff Archive and DH Lab. It builds a data edition and text analysis tools to study testimonies of Holocaust survivors. Let Them Speak is empowered by a corpus engine (Blacklab) and a Mongo DB. This repository is a collection of python scripts to transform two types of raw data (catalogue data and interview transcripts provided by data providers) into the input of the engine (annotated FOLIA xml files) and into collections of the Mongo DB running the edition. Raw data are provided by three institutions:

> * Fortunoff Archive Yale University - siglum: fortunoff
> * United States Holocaust Memorial Museums - siglum: ushmm
> * USC Shoah Foundation - siglum: usc

> Transformation of each data set is desribed in the README of the corresponding folder. (See scripts/)
> 
> The main process (see below) also takes testimonial fragments in CSV file (by using utils/transform_fragments_in_csv_to_json_for_fragments_collection.py), and transforms them to the required input of the Mongo fragments collection


## Operating System Requirements

This project can be run on both Linux and Mac; but to process a few hundred raw transcripts in DOC, it uses Mac Os Textutil. This process is skipped if the library is not available (see scripts/transform_ushmm_transcripts/run.py). 

## Python version

This project is running with python 2.7

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
pip install -r requirements.txt
```

In case both python 2 and python 3 are installed:

```bash
pip2 install -r requirements.txt
```

Then download Stanford Parser most recent version (https://stanfordnlp.github.io/CoreNLP/download.html), copy it it to project folder. First create the folder for it:
```bash
mkdir -p lib/stanford-corenlp
```

Second, unzip it (the actual zip filename may change!):

```bash
unzip -j stanford-corenlp-full-2018-02-27.zip -d lib/stanford-corenlp/
```

Copy the data.zip provided by the repo owner to the main folder, and unzip it. This will create both input folders and the output folders (this will be empty with folders used to hold output data).


## Running the transformations

Once the dependencies are settled, you can run all transformations in the main project folder by:

First open a new tab in the terminal with the project root folder and start the Stanford core nlp server as a daemon:

```bash
python start_stanford_parser.py
```

Or if both python3 and python2 are installed:

```bash
python2 start_stanford_parser.py
```
Then you can start the entire transformation process, which takes several hours to accomplish.

```bash
python run.py
```

Or if both python3 and python2 are installed:


```bash
python2 run.py
```

Or it is also possible to run the transformations in debug mode. This will process only a few transcripts, hence it will be significantly faster than the full process.

```bash
python run.py -debug
```

Or if both python3 and python2 are installed:


```bash
python2 run.py -debug
```

That will start a pipeline of 2x3 (i.e. two transformations per each institution) transformations:

> * transformation of catalogue data in various data formats (xls,marcXML,mongo collection dump) into the datamodel of the app 
> * transformation of transcripts (in XML, plain text, PDF, DOC, DOCX) into annotated FOLIA XML.

The pipeline finishes with a test, optionally it uploads the output to an amazon server (this is by default commented out). To hold data during transformations, the pipeline constructs a temporary mongo DB (let_them_speak_data_processing); at the end of the process, this DB is dropped. To create the final output,the pipeline constructs a temporary mongo DB (lts); at the end of the process, this DB is dropped. All relative pathes, collection and DB names are stored in constants.py.

## Input

The input data is copied to data/input/{collection_siglum}, once the data.zip is copied to the project folder, and unzipped. Each input data is described in the README of folders for different transformations. 

## Output

It is in data/output. The output of transformations is the input of the engine empowering Let Them Speak. First, it is three Mongo collections (see the model in DataModel.md) saved in /data/output/db/lts.archive:

> * testimonies
> * tokens
> * fragments

Second, it is a collection of annotated folia files in /data/output/folia/ in zip file. 

Third, log of documents that could not be processed are in /data/outputs/{collection_siglum}


