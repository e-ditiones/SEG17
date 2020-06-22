from lxml import etree
import json
import argparse
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("file", help="file to process")
args = arg_parser.parse_args()

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

def generate_entries(doc):
	"""
	Cette fonction permet de générer un dictionnaire ayant pour entrées le lemma 
	et pour valeurs une liste contenant toutes les formes de ce lemma.

	:param doc: document XML
	:rtype: dict
	"""
	# dictionnaire contenant l'ensemble des tokens, l'entrée est le lemma
	d_entries = {}

	entries = doc.xpath('//tei:entry', namespaces=ns)

	for entry in entries:
		orth = entry.xpath('.//tei:orth/text()', namespaces=ns)[0]
		lemma = entry.xpath('./tei:form[@type="lemma"]', namespaces=ns)[0]
		# ce dictionnaire contient les informations du lemma
		d_lemma = create_dict(lemma)
		# Partie traitant des formes fléchies
		inflected = entry.xpath('./tei:form[@type="inflected"]', namespaces=ns)
		# Cette liste contient un dictionnaire pour chaque forme 
		forms = [d_lemma]
		for form in inflected:
			d_form = create_dict(form)
			# On ne conserve que les formes qui ont déjà un "gramGrp" pour éviter les doublons.
			if "gramGrp" not in d_form:
				continue
			# On fusionne les deux dictionnaires pour ne pas perdre d'informations (notamment pour les noms).
			d_form["gramGrp"] = {**d_lemma.get("gramGrp", {}), **d_form.get("gramGrp", {})}
			forms.append(d_form)
		d_entries[orth] = d_entries.get(orth, []) + forms
	return d_entries

def create_dict(form):
	"""
	Cette fonction permet de créer un dictionnaire pour chaque forme (lemma et formes fléchies).

	:param form: XML
	:rtype: dict
	"""
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
    with open(args.file + ".json", "w", encoding="utf-8") as f:
    	json.dump(dictionnaire, f)