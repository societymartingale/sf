# SF Project

## Installation
```
pyvenv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Running
```
(env) ~/project/sf$ python analyze_sequence.py -h
usage: analyze_sequence.py [-h] --db DB --id ID --outfile OUTFILE --regex REGEX

optional arguments:
  -h, --help         show this help message and exit
  --db DB            database name such as nucleotide
  --id ID            database id such as 224589800
  --outfile OUTFILE  name of output file
  --regex REGEX      regex pattern such as "(A|C|G|T)"
```

## Sample output
```
(env) ~/project/sf$ python analyze_sequence.py --db nucleotide --id 224589800 --outfile out.txt --regex "(A|C|G|T)"
T	65668756
A	65570891
C	47024412
G	47016562
```

## Sample of csv file
```
(env) ~/project/sf$ head out.txt
T,10001,10001
A,10002,10002
A,10003,10003
C,10004,10004
C,10005,10005
C,10006,10006
T,10007,10007
A,10008,10008
A,10009,10009
C,10010,10010
```

## Commentary
One of the challenges of this project was dealing with an XML file containing a very large element,
such as the human chromosome 1 sequence. I employed the following strategies to avoid pulling the
entire element into memory:
- When retrieving the XML from NCBI, streamed the data to a file.
- When extracting the sequence from XML, used the expat parser, which doesn't read
  each element into memory as other Python XML parsers do.
- Wrote the sequence to a temp file and created a memory map to that file to allow
  for searching directly on the file.

For the human chromosome 1 (id=224589800), the process is a bit slow when searching
the regex "(A|C|G|T)". The bottleneck here is the regular expression search, which
is looking at each character and checking whether it matches one of four characters.

Design wise, the main components are:
 1. analyze_sequence.py: script run from command line
 2. efetch.py: contains a function that retrieves XML from NCBI and streams it to a file
 3. sequence_extractor.py: class that extracts the sequence from the XML and writes it
    to a temp file.

Obviously for production code, I would add things such as error handling, logging,
and unit tests, but this gives you some idea of my coding style.
