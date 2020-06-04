# SEG17

This script process segmentation, normalization and lemmatization of XML-TEI encoded files. Except the first, each step can be activated separately.

## Getting starded

#### To install SEG17, using command lines, you have to :
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
4. install lemmatisation models
```
PIE_EXTENDED_DOWNLOADS=~/MesModelsPieExtended pie-extended download fr
```

#### Now you can use SEG17

* if you want to **split** your text
```bash
python3 level2to3.py path/to/file
```
* if you want to **split and normalize** your text
```bash
python3 level2to3.py -n path/to/file
```
* if you want to **split and lemmatize**
```bash
PIE_EXTENDED_DOWNLOADS=~/MesModelsPieExtended python3 level2to3.py -l path/to/file
```
* if you want to **split, normalize and lemmatize** your text
```bash
PIE_EXTENDED_DOWNLOADS=~/MesModelsPieExtended python3 level2to3.py -l -n path/to/file
```

## How it works

### The segmentation

Using the `Level-2_to_level-3.xsl` XSL stylesheet, the script adds XML-TEI tags to split the text in segments (`<seg>`).
For each `<p>`(paragraph) and `<l>`(line), using some poncuation marks (.;:!?), the script `level2to3.py` split the text in segments captured in `<seg>` elements.

### The normalization via NMT

For the normalisation, we use [_PARALLEL17_](https://github.com/e-ditiones/PARALLEL17).


### The lemmazition

For lemmatisation, we use [_Pie-extended_](https://github.com/hipster-philology/nlp-pie-taggers) and the "[fr](https://github.com/hipster-philology/nlp-pie-taggers/tree/f3dd5197cd0a70381e008ab8239d47aff04c9737/pie_extended/models/fr)" model.

The original version, and not the normalised version, is lemmatised.

### The normalisation via lemmas

Using [Morphalou](https://www.ortolang.fr/market/lexicons/morphalou).
We offer an alternative normalisation, not seg-based but token-based. The script offer a normalised version for each token


## Examples

### Processing level2to3.Py on XML-TEI files 

Extract of the file to be processed (available [here](https://github.com/e-ditiones/SEG17/blob/master/Examples/EXP_0001_level-2_text.xml)) :

```xml
<p n="1" xml:id="EXP_0001-1-1">
    <persName>Monseignevr</persName>, Quand ie ne ſerois pas nay cõme ie ſuis, voſtre tres-humble
    ſeruiteur, il faudroit que ie fuſſe mauuais François pour ne me reſioüir pas des contẽtemens de
    voſtre <orgName>maiſon</orgName>, puis que ce ſont des felicités publiques.
</p>
```

Using `PIE_EXTENDED_DOWNLOADS=~/MesModelsPieExtended python3 level2to3.py -l -n path/to/EXP_0001_level-2_text.xml`, you get :

```xml
<p>
        <seg>
          <choice>
            <orig>
              <w lemma="monseigneur" pos="VERinf" msd="NOMB.=s">
                <orig>Monseignevr</orig>
                <reg>Monseignevr</reg>
              </w>
              <w lemma="," pos="PONfbl" msd="MORPH=empty">
                <orig>,</orig>
                <reg>,</reg>
              </w>
              <w lemma="quand" pos="CONsub" msd="MORPH=empty">
                <orig>Quand</orig>
                <reg>Quand</reg>
              </w>
              <w lemma="je" pos="PROper" msd="NOMB.=s">
                <orig>ie</orig>
                <reg>j'|je</reg>
              </w>
              <w lemma="ne" pos="ADVneg" msd="MORPH=empty">
                <orig>ne</orig>
                <reg>ne</reg>
              </w>
              <w lemma="être" pos="VERcjg" msd="MODE=con|PERS.=2|NOMB.=s">
                <orig>ſerois</orig>
                <reg>serais</reg>
              </w>
              ...
           </orig>
           <reg>Monseigneur , Quand je ne serais pas né comme je suis , votre très-humble
serviteur , il faudrait que je fusse mauvais Français pour ne me réjouir pas des ressentiments de
votre maison , puisque ce sont des ressentiments publiques .
</reg>
          </choice>
        </seg>
</p>
```
The output file can be found [here](https://github.com/e-ditiones/SEG17/blob/master/Examples/EXP_0001_level-3_text.xml).

### The dictionary

Based on the dictionary provided in TEI by Morphalou, we created a new dictionary, in JSON, using [this script](https://github.com/e-ditiones/SEG17/blob/master/Dictionary/dico.py).

For the entry "abbaye", you get :

* in TEI :
```xml
<entry xml:id="e69">
	<form type="lemma" corresp="morphalou2-tlf#ABBAYE{commonNoun} dela#abbaye{N+z1} dicollecte#abbaye{nom} lefff#abbaye{nc}">
		<orth>abbaye</orth>
		<pron>a b E i @</pron>
		<gramGrp>
			<pos>commonNoun</pos>
			<gen>feminine</gen>
		</gramGrp>
	</form>
	<form type="inflected" corresp="morphalou2-morphalou1#abbaye dela#abbaye dicollecte#abbaye lefff#abbaye">
		<orth>abbaye</orth>
		<pron>a b E i @</pron>
		<gramGrp>
			<number>singular</number>
		</gramGrp>
	</form>
	<form type="inflected" corresp="morphalou2-morphalou1#abbayes dela#abbayes dicollecte#abbayes lefff#abbayes">
		<orth>abbayes</orth>
		<pron>a b E i</pron>
		<gramGrp>
			<number>plural</number>
		</gramGrp>
	</form>
</entry>
```

* in JSON :

```json
{
   "abbaye":{
      "id":"e69",
      "lemma":{
         "orth":"abbaye",
         "pron":"a b E i @",
         "gramGrp":{
            "pos":"commonNoun",
            "gen":"feminine"
         }
      },
      "inflected":[
         {
            "orth":"abbaye",
            "pron":"a b E i @",
            "gramGrp":{
               "number":"singular"
            }
         },
         {
            "orth":"abbayes",
            "pron":"a b E i",
            "gramGrp":{
               "number":"plural"
            }
         }
      ]
   }
}
```



## Credits

This repository is developed by Alexandre Bartz with the help of Simon Gabay, as part of the project [e-ditiones](https://github.com/e-ditiones).


## Licences

<a rel="licence" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Licence Creative Commons" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />Our work is licenced under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International Licence</a>.

[_Pie-extended_](https://github.com/hipster-philology/nlp-pie-taggers) is under the [Mozilla Public License 2.0](https://www.mozilla.org/en-US/MPL/2.0/).

[_Morphalou_](https://www.ortolang.fr/market/lexicons/morphalou) is under the [LGPL-LR](https://spdx.org/licenses/LGPLLR.html).

## Cite this repository

Alexandre Bartz, Simon Gabay. 2019. _Lemmatization and normalization of French modern manuscripts and printed documents_. Retrieved from https://github.com/e-ditiones/SEG17.




