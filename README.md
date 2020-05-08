# SEG17

In order to process the lemmatization of encoded XML-TEI files, we use this script to split the text in segments.

## Getting starded

To use it, you just have to :
* install all the python librairies needed with `pip install -r requirements.txt`
* run the scrit with `python3 seg.py path/to/file.xml`


The output file will be : `Segmented_YourFile.xml`

Then this file can be lemmatized, using `Pie`.

## How it works

Using a XSL stylesheet, the script add XML-TEI tags to split the text in segments.
For each `<p>`(paragraph) and `<l>`(line), using some poncuation marks (.;:!?), the script `seg.py` split the text in segments captured in `<seg>`elements.

## Credits

This repository is developed by Alexandre Bartz with the help of Simon Gabay, as part of the project [e-ditiones](https://github.com/e-ditiones).

## Licence

This repository is CC-BY.
<br/>
<a rel="license" href="https://creativecommons.org/licenses/by/2.0"><img alt="Creative Commons License" src="https://i.creativecommons.org/l/by/2.0/88x31.png" /></a>

