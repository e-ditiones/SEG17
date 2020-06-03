# SEG17

This script process segmentation, normalization and lemmatization of XML-TEI encoded files. Except the first, each step can be activated separately. 

## Getting starded

To use it, you just have to :
* download this repository
* create a virtual environment
* in this virtual env, install all the python librairies needed with `pip install -r requirements.txt`
* if you want to **split** your text, use `python3 level2to3.py path/to/file`
* if you want to **split and normalize** your text, use `python3 level2to3.py -n path/to/file`
* if you want to **split and lemmatize** your text, start to download the `fr` model with `PIE_EXTENDED_DOWNLOADS=~/MesModelsPieExtended pie-extended download fr` and then use `PIE_EXTENDED_DOWNLOADS=~/MesModelsPieExtended python3 level2to3.py -l path/to/file`
* if you want to **split, normalize and lemmatize** your text, use `PIE_EXTENDED_DOWNLOADS=~/MesModelsPieExtended python3 level2to3.py -l -n path/to/file`


You will find some examples [here](https://github.com/e-ditiones/SEG17/tree/master/Examples).

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


## Credits

This repository is developed by Alexandre Bartz with the help of Simon Gabay, as part of the project [e-ditiones](https://github.com/e-ditiones).

For the dictionnary : Analyse et traitement informatique de la langue française - UMR 7118 (ATILF) (2019). Morphalou [Lexique]. ORTOLANG (Open Resources and TOols for LANGuage) - www.ortolang.fr, https://hdl.handle.net/11403/morphalou/v3.1.

## Licences

<a rel="licence" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Licence Creative Commons" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />Our work is licenced under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International Licence</a>.

[_Pie-extended_](https://github.com/hipster-philology/nlp-pie-taggers) is under the [Mozilla Public License 2.0](https://www.mozilla.org/en-US/MPL/2.0/).

## Cite this repository

Alexandre Bartz, Simon Gabay. 2019. _Lemmatization and normalization of French modern manuscripts and printed documents_. Retrieved from https://github.com/e-ditiones/SEG17.




