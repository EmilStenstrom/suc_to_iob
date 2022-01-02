from bz2 import BZ2File
from xml.etree.ElementTree import iterparse
import argparse

def parse(fp, skiptypes=[]):
    root = None
    ne_type = "O"
    ne_prefix = ""
    for event, elem in iterparse(fp, events=("start", "end")):
        if root is None:
            root = elem

        if event == "end" and elem.tag == "sentence":
            yield "\n"

        if event == "start" and elem.tag == "ne" and elem.attrib["type"] not in skiptypes:
            ne_type = elem.attrib["type"]
            ne_prefix = "B-"

        if event == "end" and elem.tag == "ne":
            ne_type = "O"
            ne_prefix = ""

        if event == "end" and elem.tag == "w":
            yield elem.text + "\t" + ne_prefix + ne_type + "\n"

            if ne_type != "O":
                ne_prefix = "I-"

        root.clear()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "infile",
        help="""
            Input for that contains the full SUC 3.0 XML.
            Can be the bz2-zipped version or the xml version.
        """
    )
    parser.add_argument(
        "--skiptypes",
        help="Entity types that should be skipped in output.",
        nargs="+",
        default=[]
    )
    args = parser.parse_args()

    MAGIC_BZ2_FILE_START = b"\x42\x5a\x68"
    fp = open(args.infile, "rb")
    is_bz2 = (fp.read(len(MAGIC_BZ2_FILE_START)) == MAGIC_BZ2_FILE_START)

    if is_bz2:
        fp = BZ2File(args.infile, "rb")
    else:
        fp = open(args.infile, "rb")

    for line in parse(fp, skiptypes=args.skiptypes):
        print(line, end="")

    fp.close()


if __name__ == '__main__':
    main()
