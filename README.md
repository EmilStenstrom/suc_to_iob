# SUC to IOB2 Converter

Convert the freely available Stockholm-Umeå-korpus 3.0 ([SUC 3.0](https://spraakbanken.gu.se/swe/resurs/suc3)) corpus from a custom format to [IOB2](https://en.wikipedia.org/wiki/Inside%E2%80%93outside%E2%80%93beginning_(tagging)) for use in training Swedish [NER](https://en.wikipedia.org/wiki/Named-entity_recognition) applications.

```
$ python suc_to_iob.py --help
usage: suc_to_iob.py [-h] [--skiptypes SKIPTYPES [SKIPTYPES ...]] infile

positional arguments:
  infile                Input for that contains the full SUC 3.0 XML. Can be the bz2-zipped
                        version or the xml version.

optional arguments:
  -h, --help            show this help message and exit
  --skiptypes SKIPTYPES [SKIPTYPES ...]
                        Entity types that should be skipped in output.
```

The SUC 3.0 Corpus can be downloaded from https://spraakbanken.gu.se/swe/resurs/suc3

## Clarification on the SUC 3.0 License

There are two versions of the SUC 3.0 corpus. One with the original texts mantained, and one with the sentences scrambled. The scrambled version has also been enhanced with automated tags using an automated tool (see below).

The license of the scrambled version is CC BY-SA, and trained models based on this corpus **does not need to be licensed the same way**.

Here's a translated excerpt from an e-mail from  clarifying this:

    From: peter.ljunglof@cse.gu.se
    Subject: Re: Licensing SUC 3.0
    Date: Tuesday, September 29, 2020 14:20

    Since the scrambled version is licensed under CC-BY, you do not need another license to use it for training.

    However, if you use the original SUC (ie, the non-scrambled version), you will need a SUC license.

    If we assume that it is not possible to recreate your training data based on the model, then our interpretation is that you do not need a license at all to distribute it further.

    However, for other reasons it is probably a good idea to describe the data you have trained the model with. This is so that the user of your model can know how good / bad the model can be thought to be in different contexts. (For example, I can imagine that a SUC-trained model is not the best for analyzing texts from social media).

    Peter Ljunglöf
    data- och informationsteknik, och språkbanken
    göteborgs universitet och chalmers tekniska högskola

## Algorithm

The SUC 3.0 Corpus has two ways to indicate named entities.

* Tags that are manually annotated as ´<name type=X>´
* Tags that are automatically annotated as as ´<ne type=X>´

This script parses both kinds of tags into one IOB file using the following heuristics:

1. If an entity is wrapped in both ´<name>´ and ´<ne>´, use ´<name>´
2. ... except when ´<name type="inst">´ and ´<ne type="LOC">´, use ´<ne>´.
3. ... except when ´<name type="person">´ and a part of it is a noun, use ´<ne>´.
4. ... except when ´<name type="other">´, use ´<ne>´.
5. If only ´<name>´, use ´<name>´
6. If only ´<ne>´, use ´<ne>´
7. If there are multiple types denoted by "/", as in "LOC/PRS", use the last type

### Explaination

1. ´<name>´ is manually annotated, so safer to use when possible
2. Many countries are annotated as institutions, but the automated tagging is correct, so use that one instead.
3. Some persons include their title, such as "morbror Ture" or "fänrik Brack". This rule removes the noun from the tag to just "Ture" and "Brack" are tagged.
4. Other tags are often better specified by the automated tagger
5. ´<name>´ this just means the tag was not found automatically
6. TME is not manually tagged, but exists as ´<ne>´, so this rule makes sure those are included too.
7. When the automated tagger is unsure it can output two tags denoted by a slash. Since we prioritize name tags, this rarely happens, and when manually inspecting the remaining tags the second tag was a better fit, so this rule uses that tag.

### Available tags

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

