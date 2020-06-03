from lxml import etree
import json
from pie_extended.cli.sub import get_tagger, get_model
from pie_extended.models.fr.imports import get_iterator_and_processor
import os
import re
import tempfile
import subprocess
import argparse
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("file", help="file to process")
arg_parser.add_argument("-l", "--lemmatize", help="used to lemmatize a text", action="store_true")
arg_parser.add_argument("-n", "--normalize", help="used to normalize a text", action="store_true")
args = arg_parser.parse_args()

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

# SEGMENTATION ################################################################

def transform_text(doc):
    """
    This function removes unsupported tags from a given doc.

    :param doc: XML document
    :return: XML doc after transformation
    :rtype: XLM doc
    """
    xslt = etree.parse('Level-2_to_level-3.xsl')
    transform = etree.XSLT(xslt)
    doc_transf = transform(doc)
    return doc_transf


def segment_text(text):
    """
    This function is used to segment the text and wrap these segments with <seg> elements.

    :param doc: text
    :return: a list of segments
    :rtype: list
    """
    segments = re.findall(r"[^\.\?:\;!]+[\.\?:\;!]?", text)
    list = []
    for segment in segments:
        # This makes sure no <seg> is empty
        text = segment.strip()
        if text:
            seg = etree.Element("{http://www.tei-c.org/ns/1.0}seg")
            seg.text = text
            list.append(seg)
    return list


def segment_elements(list_elements):
    """
    For each element, this function adds the text in the new <seg> elements.

    :param doc: a list of XML elements
    """
    for element in list_elements:
        text = element.text
        segs = segment_text(text)
        # This removes the text before we add it in the new <seg> element.
        element.clear()
        element.extend(segs)


def segment_document(doc):
    """
    For each lines and paragraphs, this function segments the text and add new <seg> elements.

    :param doc: a XML document
    :return: XML doc with segmented text
    :rtype: a new XLM doc
    """
    # Only the text enclosed between <p> and <l> is segmented.
    with open('Dictionary/dictionnaire.json', 'r') as f:
        dico = json.loads(f.read()) 
    paragraphs = doc.xpath('//tei:text//tei:p', namespaces=ns)
    lines = doc.xpath('//tei:text//tei:l', namespaces=ns)
    segment_elements(paragraphs)
    segment_elements(lines)
    # Used to normalize the text.
    if args.normalize:
        segs = doc.xpath('//tei:seg', namespaces=ns)
        normalize_segs(segs)
    # Used to lemmatize the text.
    if args.lemmatize:
        if args.normalize:
            # Only the original text is lemmatized.
            tags = doc.xpath('//tei:orig', namespaces=ns)
        else:
            # If the text is only to be lemmatized, segs are lemmatized.
            tags = doc.xpath('//tei:seg', namespaces=ns)
        lemmatize(tags)
        for tag in tags:
            words = tag.xpath('./tei:w', namespaces=ns)
            normalize_w(words, dico)
    # Indent() inserts tail whitespace for pretty-printing an XML tree.
    etree.indent(doc)
    # This output file is specific to the project e-ditiones, you can easily change the output with e.g. doc.write("New" + args.file, ...)
    return doc.write(args.file.replace("level-2", "level-3"), pretty_print=True, encoding="utf-8", method="xml")


# NORMALIZATION - W ###########################################################

def create_gram(pos, msd):
    gram = {}
    infos = msd.split("|")
    for info in infos:
        [key, val] = info.split("=")
        if key == "NOMB.":
            if val == "s":
                gram["number"] = "singular"
            elif val == "p":
                gram["number"] = "plural"
        elif key == "GENRE":
            if val == "f":
                gram["gen"] = "feminine"
            elif val == "m":
                gram ["gen"] = "masculine"
        elif key == "PERS." :
            if val == "1":
                gram["per"] = "firstPerson"
            elif val == "2":
                gram["per"] = "secondPerson"
            elif val == "3":
                gram["per"] = "thirdPerson"
        elif key == "TEMPS":
            if val == "pst":
                gram["tns"] = "present"
            elif val == "fut":
                gram["tns"] = "future"
            elif val == "ipf":
                gram["tns"] = "imperfect"
            elif val == "psp":
                gram["tns"] = "simplePast"
        elif key == "MODE":
            if val == "ind":
                gram["mood"] = "indicative"
            elif val == "con":
                gram["mood"] = "conditional"
            elif val == "imp":
                gram["mood"] = "imperative"
            elif val == "sub":
                gram["mood"] = "subjonctive"
    if pos == "VERppe":
        gram["mood"] = "participle"
        gram["tns"] = "past"
    elif pos == "VERppa":
        gram["mood"] = "participle"
        gram["tns"] = "present"
    elif pos == "VERinf":
        gram["mood"] = "infinitive"
    return gram

def match_gram(gram, dict_gram):
    for key in gram:
        if key not in dict_gram:
            return False
        if gram[key] != dict_gram[key] and dict_gram[key] != "invariable":
            return False
    return True


def normalize_word(word, dico):
    result = []
    lemma = word.get("lemma")
    pos = word.get("pos")
    msd = word.get("msd")
    entry = dico.get(lemma)
    if not entry:
        return word.text
    gram = create_gram(pos, msd)
    for inflected in entry["inflected"]:
        if "gramGrp" in inflected and match_gram(gram, inflected["gramGrp"]):
            result.append(inflected["orth"])
    if len(result) > 0:
        return "|".join(result)
    return word.text


def normalize_w(words, dico):
    """
    This function normalize each word using the dictionnary. 

    :param doc: a list of words 
    :param doc: the dictionnay
    """
    for word in words:
        orig = etree.Element("{http://www.tei-c.org/ns/1.0}orig")
        reg = etree.Element("{http://www.tei-c.org/ns/1.0}reg")
        orig.text = word.text
        reg.text = normalize_word(word, dico)
        word.text = ""
        word.extend([orig, reg])

# NORMALIZATION - SEG #########################################################

def normalize_segs(segs):
    """
    This function process a normalization of the text.

    :param doc: a list of tags
    """
    for seg in segs:
        # Creation of temporary file to use the normaliser.
        file = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", newline=None)
        # This removes blank line, otherwise the script doesn't work.
        text = seg.text.strip('\n')
        file.write(text)
        # Insure file is written.
        file.flush()
        # This first script prepare the file.
        subprocess.run(["NORM17/prepare_data.bash", file.name])
        # This second script is used to normalize the text.
        subprocess.run(["NORM17/translate_file.bash", file.name + ".tok"])
        # Addition of new XML-TEI elements.
        orig = etree.Element("{http://www.tei-c.org/ns/1.0}orig")
        reg = etree.Element("{http://www.tei-c.org/ns/1.0}reg")
        choice = etree.Element("{http://www.tei-c.org/ns/1.0}choice")
        orig.text = text
        with open(file.name + ".tok_into_fr.test.beam10", "r") as f:
            reg.text = f.read()
        choice.extend([orig, reg])
        seg.clear()
        seg.append(choice)
        os.remove(file.name + ".tok")
        os.remove(file.name + ".tok_into_fr.test.beam10")
        file.close()


# LEMMATIZATION ###############################################################

def lemmatize(segs):
    """
    This function process a lemmatization of the text.

    :param doc: a list of tags
    """
    model_name = "fr"
    tagger = get_tagger(model_name, batch_size=256, device="cpu", model_path=None)
    for seg in segs:
    	seg_s = seg.text.replace('ſ', 's')
    	iterator, processor = get_iterator_and_processor()
    	# On procède à deux lemmatisations, l'une avec l'ancien texte et l'autre avec le nouveau
    	orig_lemmas = tagger.tag_str(seg.text, iterator=iterator, processor=processor)
    	lemmas = tagger.tag_str(seg_s, iterator=iterator, processor=processor)
    	words = []
    	assert len(orig_lemmas) == len(lemmas)
    	for index in range(len(lemmas)):
    		w = etree.Element("{http://www.tei-c.org/ns/1.0}w")
    		# On conserve ainsi la forme "ſ" 
    		w.text = orig_lemmas[index]['form']
    		w.attrib['lemma']=lemmas[index]['lemma']
    		w.attrib['pos']=lemmas[index]['POS']
    		w.attrib['msd']=lemmas[index]['morph']
    		words.append(w)
    	seg.clear()
    	seg.extend(words)


if __name__ == "__main__":
    parser = etree.XMLParser(remove_blank_text=True)
    doc = etree.parse(args.file, parser)
    text_transformed = transform_text(doc)
    segment_document(text_transformed)