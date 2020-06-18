# Dictionaries

Using the lemmatization and dictionaries, we offer an alternative normalization, not seg-based but token-based.

There are two dictionaries :
* [an intermediary dictionary](https://github.com/e-ditiones/SEG17/blob/master/Dictionaries/intermediary_dict.xml.json)
* [a dictionary based on Morphalou](https://github.com/e-ditiones/SEG17/blob/master/Dictionaries/morphalou_dict.json)

These two dictionaries are automaticaly generated with [*dict_TEI_to_JSON.py*](https://github.com/e-ditiones/SEG17/blob/master/Dictionaries/dict_TEI_to_JSON.py). The input file is a XML-TEI file and the output file in JSON. 

We generated the dictionary based on Morphalou using the XML-TEI file provided by Morphalou and available [here](https://www.ortolang.fr/market/lexicons/morphalou).

In order to get better results, we decided to create an intermediary dictionary in XML-TEI format, which is converted in JSON with [*dict_TEI_to_JSON.py*](https://github.com/e-ditiones/SEG17/blob/master/Dictionaries/dict_TEI_to_JSON.py) too.
You can easily add new entries in this dictionary and then process the script to get a new dictionary in JSON. 

## Getting started

### Add new entries

This part explains how you can add some new entries in the intermediary dictionary and presents the XML-TEI structure of each type of entries. A part of the structure is always the same and is required (`entry` with `@xml:id`, `form`with `@type`for example) but there are some special characteristics.

#### A common noun

```xml
<entry xml:id="EXP1">
	<form type="lemma">
		<orth>abadis</orth>
		<gramGrp>
			<pos>commonNoun</pos>
			<gen>masculine</gen>
		</gramGrp>
	</form>
	<form type="inflected">
		<orth>abadis</orth>
		<gramGrp>
			<number>invariable</number>
		</gramGrp>
	</form>
</entry>
```

#### An invariable common noun

```xml
<entry xml:id="EXP2">
	<form type="lemma">
		<orth>abandonnataire</orth>
		<gramGrp>
			<pos>commonNoun</pos>
			<gen>invariable</gen>
		</gramGrp>
	</form>
	<form type="inflected">
		<orth>abandonnataire</orth>
		<gramGrp>
			<number>singular</number>
		</gramGrp>
	</form>
	<form type="inflected">
		<orth>abandonnataires</orth>
		<gramGrp>
			<number>plural</number>
		</gramGrp>
	</form>
</entry>
```

#### An adjective

```xml
<entry xml:id="EXP3">
	<form type="lemma">
		<orth>abaissable</orth>
		<gramGrp>
			<pos>adjective</pos>
		</gramGrp>
	</form>
	<form type="inflected">
		<orth>abaissable</orth>
		<gramGrp>
			<number>singular</number>
			<gen>invariable</gen>
		</gramGrp>
	</form>
	<form type="inflected">
		<orth>abaissables</orth>
		<gramGrp>
			<number>plural</number>
			<gen>invariable</gen>
		</gramGrp>
	</form>
</entry>
```

#### A verb

```xml
<entry xml:id="EXP4">
	<form type="lemma">
		<orth>abaisser</orth>
		<gramGrp>
			<pos>verb</pos>
		</gramGrp>
	</form>
	<form type="inflected">
		<orth>abaissa</orth>
		<gramGrp>
			<number>singular</number>
			<mood>indicative</mood>
			<per>thirdPerson</per>
			<tns>simplePast</tns>
		</gramGrp>
	</form>
</entry>
```

#### An adverb

```xml
<entry xml:id="EXP5">
	<form type="lemma">
		<orth>amiteusement</orth>
		<gramGrp>
			<pos>adverb</pos>
		</gramGrp>
	</form>
	<form type="inflected">
		<orth>amiteusement</orth>
	</form>
</entry>
```

#### A personal pronoun

```xml
<entry xml:id="EXP6">
	<form type="lemma">
		<orth>je</orth>
		<gramGrp>
			<pos>pronoun</pos>
			<subc>personal</subc>
		</gramGrp>
	</form>
	<form type="inflected">
		<orth>j'</orth>
		<gramGrp>
			<number>singular</number>
			<per>firstPerson</per>
		</gramGrp>
	</form>
	<form type="inflected">
		<orth>je</orth>
		<gramGrp>
			<number>singular</number>
			<per>firstPerson</per>
		</gramGrp>
	</form>
</entry>
```

#### A preposition

```xml
<entry xml:id="EXP7">
	<form type="lemma">
		<orth>jouxte</orth>
		<gramGrp>
			<pos>preposition</pos>
		</gramGrp>
	</form>
	<form type="inflected">
		<orth>jouxte</orth>
	</form>
</entry>
```

#### A determiner

```xml
<entry xml:id="EXP8">
	<form type="lemma">
		<orth>un</orth>
		<gramGrp>
			<pos>determiner</pos>
			<subc>indefinite</subc>
		</gramGrp>
	</form>
	<form type="inflected">
		<orth>un</orth>
		<gramGrp>
			<number>singular</number>
			<gen>masculine</gen>
		</gramGrp>
	</form>
	<form type="inflected">
		<orth>des</orth>
		<gramGrp>
			<number>plural</number>
			<gen>invariable</gen>
		</gramGrp>
	</form>
</entry>
```

#### A conjunction

```xml
<entry xml:id="EXP9">
	<form type="lemma">
		<orth>c'est pourquoi</orth>
		<gramGrp>
			<pos>conjunction</pos>
			<subc>coordination</subc>
		</gramGrp>
	</form>
	<form type="inflected">
		<orth>c'est pourquoi</orth>
	</form>
</entry>
```

### Get your dictionary in JSON

If you havn't downloaded the repository yet, start to :
1. clone or download this repository
```bash
git clone git@github.com:e-ditiones/SEG17.git
cd SEG17
```
2. create a virtual environment and activate it
```bash
python3 -m venv env
source env/bin/activate
```
3. install dependencies
```bash
pip install -r requirements.txt
```
Once it's done, you can create your dictionary :

1. start with
```bash
cd Dictionaries
```

2. and create your dictionary
```bash
python3 dict_TEI_to_JSON.py your_file.xml
```