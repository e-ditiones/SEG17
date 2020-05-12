# SEG17

In order to process the lemmatization of encoded XML-TEI files, we use this script to split the text in segments.

## Getting starded

To use it, you just have to :
* install all the python librairies needed with `pip install -r requirements.txt`
* download the `fr` model with `PIE_EXTENDED_DOWNLOADS=~/MesModelsPieExtended pie-extended download fr`
* then, if you want to **split** your text, use `python3 seg.py path/to/file`
* if you want to **split and lemmatize** your text, use `PIE_EXTENDED_DOWNLOADS=~/MesModelsPieExtended python3 seg.py -l path/to/file`


The output file will be : `Segmented_YourFile.xml`


## How it works

Using a XSL stylesheet, the script add XML-TEI tags to split the text in segments.
For each `<p>`(paragraph) and `<l>`(line), using some poncuation marks (.;:!?), the script `seg.py` split the text in segments captured in `<seg>`elements.

The text is then lemmatized using [_Pie-extended_](https://github.com/hipster-philology/nlp-pie-taggers) and the modef "[fr](https://github.com/hipster-philology/nlp-pie-taggers/tree/f3dd5197cd0a70381e008ab8239d47aff04c9737/pie_extended/models/fr)".

You will find some examples [here](https://github.com/e-ditiones/SEG17/tree/master/Examples).

## Credits

This repository is developed by Alexandre Bartz with the help of Simon Gabay, as part of the project [e-ditiones](https://github.com/e-ditiones).

## Licences

<a rel="licence" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Licence Creative Commons" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />Our work is licenced under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International Licence</a>.

[_Pie-extended_](https://github.com/hipster-philology/nlp-pie-taggers) is under the [Mozilla Public License 2.0](https://www.mozilla.org/en-US/MPL/2.0/).

## Cite this repository

Alexandre Bartz, Simon Gabay. 2019. _Lemmatization and normalization for French modern manuscripts and printed documents_. Retrieved from https://github.com/e-ditiones/SEG17.




