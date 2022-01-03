from bz2 import BZ2File
from xml.etree.ElementTree import iterparse
import argparse
from collections import Counter

def parse(fp, skiptypes=[]):
    types = Counter()

    root = None
    ne_prefix = ""
    ne_type = "O"
    name_prefix = ""
    name_type = "O"

    for event, elem in iterparse(fp, events=("start", "end")):
        if root is None:
            root = elem

        if event == "start":
            if elem.tag == "name":
                _type = name_type_to_ne_type(elem.attrib["type"])
                if (
                    _type not in skiptypes and
                    not (_type == "ORG" and ne_type == "LOC")
                ):
                    name_type = _type
                    name_prefix = "B-"

            elif elem.tag == "ne":
                _type = elem.attrib["type"]
                if "/" in _type:
                    _type = _type[_type.index("/") + 1:]

                if _type not in skiptypes:
                    ne_type = _type
                    ne_prefix = "B-"

            elif elem.tag == "w":
                if name_type == "PRS" and elem.attrib["pos"] == "NN":
                    name_type = "O"
                    name_prefix = ""

        elif event == "end":
            if elem.tag == "sentence":
                yield

            elif elem.tag == "name":
                name_type = "O"
                name_prefix = ""

            elif elem.tag == "ne":
                ne_type = "O"
                ne_prefix = ""

            elif elem.tag == "w":
                if name_type != "O" and name_type != "OTH":
                    types[name_type] += 1
                    yield elem.text, name_prefix, name_type
                elif ne_type != "O":
                    types[ne_type] += 1
                    yield elem.text, ne_prefix, ne_type
                else:
                    yield elem.text, "", "O"

                if ne_type != "O":
                    ne_prefix = "I-"

                if name_type != "O":
                    name_prefix = "I-"

        root.clear()

    print(types)

def name_type_to_ne_type(name_type):
    mapping = {
        "inst": "ORG",
        "product": "OBJ",
        "other": "OTH",
        "place": "LOC",
        "myth": "MYT",
        "person": "PRS",
        "event": "EVN",
        "work": "WRK",
        "animal": "ANI",
    }
    return mapping.get(name_type)

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

    for token in parse(fp, skiptypes=args.skiptypes):
        if not token:
            print()
        else:
            word, prefix, label = token
            print(word + "\t" + prefix + label)

    fp.close()


if __name__ == '__main__':
    main()
