# SUC to IOB2 Converter

Convert the [SUC 3.0](https://spraakbanken.gu.se/swe/resurs/suc3) corpus from a custom format to [IOB2](https://en.wikipedia.org/wiki/Inside%E2%80%93outside%E2%80%93beginning_(tagging)) for use in training [NER](https://en.wikipedia.org/wiki/Named-entity_recognition) applications.

```
$ python suc_to_iob.py --help
usage: suc_to_iob.py [-h] [--detail {UNNAMED,NAMED,NAMED_DETAILED}]
                     [--skiptypes SKIPTYPES [SKIPTYPES ...]]
                     infile

positional arguments:
  infile                Input for that contains the full SUC 3.0 XML. Can be
                        the bz2-zipped version or the xml version.

optional arguments:
  -h, --help            show this help message and exit
  --detail {UNNAMED,NAMED,NAMED_DETAILED}
                        Detail level that the file should be output in.
  --skiptypes SKIPTYPES [SKIPTYPES ...]
                        Entity types that should be skipped in output.
```

The SUC 3.0 Corpus can be downloaded from https://spraakbanken.gu.se/swe/resurs/suc3

## Example usage:

Normal usage (No need to unzip the corpus):
```
$ python suc_to_iob.py suc3.xml.bz2 > suc_3.0_iob.txt
```

Include the more specific labels from SUC in the output:
```
$ python suc_to_iob.py suc3.xml.bz2 --detail NAMED_DETAILED > suc_3.0_iob.txt
```

Skip some labels from the output:
```
$ python suc_to_iob.py suc3.xml.bz2 --skiptypes MSR TME > suc_3.0_iob.txt
```

