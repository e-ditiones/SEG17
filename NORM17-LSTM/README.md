# Normalisation of Modern French with an LSTM 'NMT' model

## Basic Usage

From untokenised text, input directly from standard input

```
>> echo "D'autres loin de ſe taire en ce meſme moment," | bash run_normalisation.sh

D'	D'
autres	autres
loin	loin
de	de
ſe	se
taire	taire
en	en
ce	ce
meſme	même
moment	moment
,	,

```

N.B. The tokenisation used (scripts found in align/) is from [pie-taggers, v0.0.13](https://github.com/hipster-philology/nlp-pie-taggers/blob/80a1b7477abb4abaaac943c793cf1fb2c106749a/pie_extended/models/fr/tokenizer.py). The necessary files for tokenised have been copied here to avoid having to import heavy dependencies.

From tokenised text, input tab-separated text (1st field = original text, 2nd field = tokenised) from standard input

```
>> echo -e "D'autres loin de ſe taire en ce meſme moment,\tD' autres loin de ſe taire en ce meſme moment ," | bash run_normalisation-double-input.sh

D	D▁
'	▁'
autres	autres
loin	loin
de	de
ſe	se
taire	taire
en	en
ce	ce
meſme	même
moment	moment
,	,

```

## TEI format

TODO


