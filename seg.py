from lxml import etree
from pie_extended.cli.sub import get_tagger, get_model
from pie_extended.models.fr.imports import get_iterator_and_processor
import re
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
        # This removes the text before we add it in the new <seg> element
        element.clear()
        element.extend(segs)


def segment_document(doc):
    """
    For each lines and paragraphs, this function segments the text and add new <seg> elements.

    :param doc: a XML document
    :return: XML doc with segmented text
    :rtype: a new XLM doc
    """
    paragraphs = doc.xpath('//tei:text//tei:p', namespaces=ns)
    lines = doc.xpath('//tei:text//tei:l', namespaces=ns)
    segment_elements(paragraphs)
    segment_elements(lines)
    segs = doc.xpath('//tei:seg', namespaces=ns)
    if args.lemmatize:
        lemmatize(segs)
    # indent() inserts tail whitespace for pretty-printing an XML tree.
    etree.indent(doc)
    return doc.write("Segmented_" + str(args.file), pretty_print=True, encoding="utf-8", method="xml")


def lemmatize(segs):
    """
    This function process a lemmatization and adds <w> elements.

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