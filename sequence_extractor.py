import constant


class SequenceExtractor():
    """Extract sequence data from XML file to temp file
    """

    def __init__(self, temp_file):
        self.current_tag = None
        self.temp_file = temp_file

    def start_element(self, name, attrs):
        self.current_tag = name

    def end_element(self, name):
        self.current_tag = None

    def char_data(self, data):
        if self.current_tag == constant.SEQUENCE_TAG:
            self.temp_file.write(bytes(
                data, encoding=constant.ENCODING))
