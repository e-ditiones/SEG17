# SEG17

This script process segmentation, normalization and lemmatization of XML-TEI encoded files. Except the first, each step can be activated separately. 

## Getting starded

To use it, you just have to :
* clone ord download this repository  
* create a virtual environment with `virtual env`and activate it with `source env/bin/activate`
* in this virtual env, install all the python librairies required with `pip install -r requirements.txt`
* if you want to **split** your text, use `python3 level2to3.py path/to/file`
* if you want to **split and normalize** your text, use `python3 level2to3.py -n path/to/file`
* if you want to **split and lemmatize** your text, start to download the `fr` model with `PIE_EXTENDED_DOWNLOADS=~/MesModelsPieExtended pie-extended download fr` and then use `PIE_EXTENDED_DOWNLOADS=~/MesModelsPieExtended python3 level2to3.py -l path/to/file`
* if you want to **split, normalize and lemmatize** your text, use `PIE_EXTENDED_DOWNLOADS=~/MesModelsPieExtended python3 level2to3.py -l -n path/to/file`

## How it works

### The segmentation

Using a XSL stylesheet, the script add XML-TEI tags to split the text in segments.
For each `<p>`(paragraph) and `<l>`(line), using some poncuation marks (.;:!?), the script `seg.py` split the text in segments captured in `<seg>` elements.

### The normalization

The text can be normalized using [_PARALLEL17_](https://github.com/e-ditiones/PARALLEL17).


### The lemmazition

The text can also be lemmatized using [_Pie-extended_](https://github.com/hipster-philology/nlp-pie-taggers) and the modef "[fr](https://github.com/hipster-philology/nlp-pie-taggers/tree/f3dd5197cd0a70381e008ab8239d47aff04c9737/pie_extended/models/fr)".

For now, lemmatization is only processed on the original transcription (`<orig>` or `<seg>` if the text isn't normalized).

The dictionnary used for the normalization of each token is based on [Morphalou](https://www.ortolang.fr/market/lexicons/morphalou).

## Examples

Extract of the file to be processed (available [here](https://github.com/e-ditiones/SEG17/blob/master/Examples/EXP_0001_level-2_text.xml)) :

```xml
<p n="1" xml:id="EXP_0001-1-1">
    <persName>Monseignevr</persName>, Quand ie ne ſerois pas nay cõme ie ſuis, voſtre tres-humble
    ſeruiteur, il faudroit que ie fuſſe mauuais François pour ne me reſioüir pas des contẽtemens de
    voſtre <orgName>maiſon</orgName>, puis que ce ſont des felicités publiques.
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
The output file can be found [here](https://github.com/e-ditiones/SEG17/blob/master/Examples/EXP_0001_level-3_text.xml))

## Credits

This repository is developed by Alexandre Bartz with the help of Simon Gabay, as part of the project [e-ditiones](https://github.com/e-ditiones).

The dictionary is generated using Morphalou. 
Analyse et traitement informatique de la langue française - UMR 7118 (ATILF) (2019). Morphalou [Lexique]. ORTOLANG (Open Resources and TOols for LANGuage) - www.ortolang.fr, https://hdl.handle.net/11403/morphalou/v3.1.

## Licences

<a rel="licence" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Licence Creative Commons" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />Our work is licenced under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International Licence</a>.

[_Pie-extended_](https://github.com/hipster-philology/nlp-pie-taggers) is under the [Mozilla Public License 2.0](https://www.mozilla.org/en-US/MPL/2.0/).

[_Morphalou_](https://www.ortolang.fr/market/lexicons/morphalou) is under the [LGPL-LR](https://spdx.org/licenses/LGPLLR.html).

## Cite this repository

Alexandre Bartz, Simon Gabay. 2019. _Lemmatization and normalization of French modern manuscripts and printed documents_. Retrieved from https://github.com/e-ditiones/SEG17.




