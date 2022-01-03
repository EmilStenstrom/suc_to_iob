# SUC to IOB2 Converter

Convert the [SUC 3.0](https://spraakbanken.gu.se/swe/resurs/suc3) corpus from a custom format to [IOB2](https://en.wikipedia.org/wiki/Inside%E2%80%93outside%E2%80%93beginning_(tagging)) for use in training [NER](https://en.wikipedia.org/wiki/Named-entity_recognition) applications.

```
$ python suc_to_iob.py --help
usage: suc_to_iob.py [-h] [--skiptypes SKIPTYPES [SKIPTYPES ...]]
                     infile

positional arguments:
  infile                Input for that contains the full SUC 3.0 XML. Can be
                        the bz2-zipped version or the xml version.

optional arguments:
  -h, --help            show this help message and exit
  --skiptypes SKIPTYPES [SKIPTYPES ...]
                        Entity types that should be skipped in output.
```

The SUC 3.0 Corpus can be downloaded from https://spraakbanken.gu.se/swe/resurs/suc3

## Algorithm

The SUC 3.0 Corpus has two ways to indicate named entities.

* Tags that are manually annotated as ´<name type=X>´
* Tags that are automatically annotated as as ´<ne type=X>´

This script parses both kinds of tags into one IOB file using the following heuristics:

1. If an entity is wrapped in both ´<name>´ and ´<ne>´, use ´<name>´
2. ... except when ´<name type="inst">´ and ´<ne type="LOC">´, use ´<ne>´.
3. ... except when ´<name type="person">´ and a part of it is a noun, use ´<ne>´.
4. ... except when ´<name type="other">´ and ´<ne type="ORG">´, use ´<ne>´.
5. If only ´<name>´, use ´<name>´
6. If only ´<ne>´, use ´<ne>´
7. If there are multiple types denoted by "/", as in "LOC/PRS", use the last type

The second rule handles locations commonly annotated as institutions.
The third rule handles person blocks marked as "morbror Ture" instead of just the name.
The fourth rule handles other blocks incorrectly markeas as other instead of org.
The sixth rule handles more TME tags which are otherwise missed.

All name types are mapped to ne types, to produce the following set of existing tags (number of occurances within parentisis):

* TME (25967) - Time unit
* PRS (22874) - Person
* LOC (12076) - Location
* ORG (8224) - Organization
* MSR (6061) - Meassurement
* WRK (5055) - Work of art
* OBJ (1085) - Object
* EVN (642) - Event
* ANI (464) - Animal
* MYT (301) - Mythological

## Example usage:

Normal usage (No need to unzip the corpus):
```
$ python suc_to_iob.py suc3.xml.bz2 > suc_3.0_iob.txt
```

Skip some labels from the output:
```
$ python suc_to_iob.py suc3.xml.bz2 --skiptypes MSR TME > suc_3.0_iob.txt
```

