import constant
import requests


def get_ncbi_data(db, id):
    """Get data from ncbi and stream to xml file
    Args:
        db (str): database name such as nucleotide
        id (int): database id such as 224589800
    """
    url = constant.EFETCH_URL.format(db=db, id=id)
    response = requests.get(url, stream=True)
    with open(constant.XML_FILE, 'wb') as f:
        for chunk in response.iter_content(chunk_size=constant.CHUNK_SIZE):
            if chunk:
                f.write(chunk)
