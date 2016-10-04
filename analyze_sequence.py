import argparse
import mmap
import re
import tempfile

from collections import Counter
from xml.parsers import expat

import constant
import efetch
from sequence_extractor import SequenceExtractor


def _get_xml_parser(temp_file):
    """get xml parser that extracts sequence to temp file
    Args:
        temp_file (file object)
    Returns:
        expat parser
    """
    s = SequenceExtractor(temp_file)
    xml_parser = expat.ParserCreate()
    xml_parser.StartElementHandler = s.start_element
    xml_parser.CharacterDataHandler = s.char_data
    return xml_parser


def _generate_report(mm, regex, outfile):
    """Write reports to STDOUT and outfile
    Args:
        mm (mmap): memory map containing sequence
        regex (string): regex to search for in mm
        outfile (string): name of csv file to write
    """
    counter = Counter()
    with open(outfile, mode='w') as f:
        for match in re.finditer(bytes(regex, encoding=constant.ENCODING), mm):
            hit_sequence = match.group().decode(constant.ENCODING)
            # convention to start at 1 rather than 0
            start = match.start() + 1
            end = match.end()
            f.write('{},{},{}\n'.format(hit_sequence, start, end))
            counter.update([hit_sequence])
    for val, count in counter.most_common():
        print('{}\t{}'.format(val, count))


def _parse_cl_args():
    """Parse command-line arguments and return them
    Returns:
        args (argparse.Namespace): namespace containing command-line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--db',
                        type=str,
                        help='database name such as nucleotide',
                        required=True)
    parser.add_argument('--id',
                        type=int,
                        help='database id such as 224589800',
                        required=True)
    parser.add_argument('--outfile',
                        type=str,
                        help='name of output file',
                        required=True)
    parser.add_argument('--regex',
                        type=str,
                        help='regex pattern such as "(A|C|G|T)"',
                        required=True)
    return parser.parse_args()


def main():
    """Main entry point into this script
    Gets command-line args, fetches xml from ncbi,
    parses xml, and generates reports
    """
    args = _parse_cl_args()
    efetch.get_ncbi_data(args.db, args.id)

    with tempfile.TemporaryFile() as temp_file:
        xml_parser = _get_xml_parser(temp_file)
        with open(constant.XML_FILE, 'rb') as f:
            xml_parser.ParseFile(f)

        temp_file.seek(0)
        mm = mmap.mmap(temp_file.fileno(), 0)

        _generate_report(mm, args.regex, args.outfile)


if __name__ == '__main__':
    main()
