CHUNK_SIZE = 8192  # chunk size for streaming xml to file
EFETCH_URL = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db={db}&id={id}&rettype=fasta&retmode=xml'
ENCODING = 'utf8'
SEQUENCE_TAG = 'TSeq_sequence'
XML_FILE = 'sequence.fasta.xml'
