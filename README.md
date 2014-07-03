# identify_wiki

**identify_wiki** identifies the subjects most likely to represent the content of a wiki.

## Installation

```
python setup.py install
```

## Usage

To run as module:

```
python -m identify_wiki --input wiki_ids.txt --output subjects.txt
```

From another Python script:

``` python
>>> from identify_wiki import get_subject_list
>>> get_subject_list('831')
[u'Muppet']
```
