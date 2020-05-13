from lxml import etree
from pie_extended.cli.sub import get_tagger, get_model
from pie_extended.models.fr.imports import get_iterator_and_processor
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
        seg = etree.Element("{http://www.tei-c.org/ns/1.0}seg")
        seg.text = segment
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
    paragraphs = doc.xpath('//tei:text//tei:p', namespaces=ns)
    lines = doc.xpath('//tei:text//tei:l', namespaces=ns)
    segment_elements(paragraphs)
    segment_elements(lines)
    # Used to normalize the text.
    if args.normalize:
        segs = doc.xpath('//tei:seg', namespaces=ns)
        normalize(segs)
    # Used to lemmatize the text.
    if args.lemmatize:
        # Only the original text is lemmatized.
        orig = doc.xpath('//tei:orig', namespaces=ns)
        lemmatize(orig)
    # Indent() inserts tail whitespace for pretty-printing an XML tree.
    etree.indent(doc)
    return doc.write("Segmented_" + str(args.file), pretty_print=True, encoding="utf-8", method="xml")


def normalize(segs):
    """
    This function process a normalization of the text.

    :param doc: a list of tags
    """
    for seg in segs:
        # Creation of temporary file to use the normaliser.
        file = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, newline=None)
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
# !!!! gérer les problèmes de segments vides, fait bugger le programme

def lemmatize(segs):
    """
    This function process a lemmatization of the text.

    :param doc: a list of tags
    """
    model_name = "fr"
    tagger = get_tagger(model_name, batch_size=256, device="cpu", model_path=None)
    for seg in segs:
        iterator, processor = get_iterator_and_processor()
        lemmas = tagger.tag_str(seg.text, iterator=iterator, processor=processor)
        words = []
        for entry in lemmas:
            w = etree.Element("{http://www.tei-c.org/ns/1.0}w")
            w.text = entry['form']
            w.attrib['lemma']=entry['lemma']
            w.attrib['pos']=entry['POS']
            w.attrib['msd']=entry['morph']
            words.append(w)
        seg.clear()
        seg.extend(words)


if __name__ == "__main__":
    parser = etree.XMLParser(remove_blank_text=True)
    doc = etree.parse(args.file, parser)
    text_transformed = transform_text(doc)
    segment_document(text_transformed)