from lxml import etree
import json
import argparse
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("file", help="file to process")
args = arg_parser.parse_args()

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

def generate_entries(doc):
	# dictionnaire contenant l'ensemble des tokens, l'entrée est le lemma
	d_entries = {}

	entries = doc.xpath('//tei:entry', namespaces=ns)

	for entry in entries:
		orth = entry.xpath('.//tei:orth/text()', namespaces=ns)[0]
		lemma = entry.xpath('./tei:form[@type="lemma"]', namespaces=ns)[0]
		identifiant = entry.xpath('./@xml:id', namespaces=ns)[0]
		# un dictionnaire par token (lemma + ses formes fléchies)
		d_entry = {}
		d_entry["id"] = identifiant
		# ce dictionnaire contient les informations du lemma
		d_lemma = create_dict(lemma)
		d_entry["lemma"] = d_lemma
		# Partie traitant des formes fléchies
		inflected = entry.xpath('./tei:form[@type="inflected"]', namespaces=ns)
		# Cette liste contient un dictionnaire pour chaque forme fléchie
		l_inflected = []
		for form in inflected:
			l_inflected.append(create_dict(form))
		d_entry["inflected"] = l_inflected 
		d_entries[orth] = d_entry
	return d_entries

def create_dict(form):
	d_infos = {}
	for child in form:
		# Permet de retirer les namespaces
		tag = etree.QName(child).localname
		# Si un élément a lui-même des enfants, on utilise une fonction récursive
		if len(list(child)) > 0:
			d_infos[tag] = create_dict(child)
		else:
			d_infos[tag] = child.text
	return d_infos

if __name__ == "__main__":
    parser = etree.XMLParser()
    doc = etree.parse(args.file, parser)
    dictionnaire = generate_entries(doc)
    with open("dictionnaire.json", "w", encoding="utf-8") as f:
    	json.dump(dictionnaire, f)