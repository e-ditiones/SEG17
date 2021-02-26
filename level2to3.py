from lxml import etree
import json
from pie_extended.cli.sub import get_tagger, get_model
# Change fr to freem for early modern french.
from pie_extended.models.fr.imports import get_iterator_and_processor
import os
import re
import tempfile
import subprocess
import argparse
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("file", help="file to process")
arg_parser.add_argument("-l", "--lemmatize",
                        help="used to lemmatize a text", action="store_true")
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
    xslt = etree.parse('XSLT/Level-2_to_level-3.xsl')
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
    n = 1
    for segment in segments:
        # This makes sure no <seg> is empty
        text = segment.strip()
        if text:
            seg = etree.Element("{http://www.tei-c.org/ns/1.0}seg")
            seg.text = text
            seg.attrib["n"] = str(n)
            # The xml:id attribute is generated with the value of the n attribute.
            seg.attrib["{http://www.w3.org/XML/1998/namespace}id"] = "s" + seg.get("n")
            n += 1
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


def to_level_3(doc):
    """
    For each lines and paragraphs, this function segments, lemmatizes and normalizes the text.

    :param doc: a XML document
    :return: a level 3 XML document
    :rtype: a new XLM document
    """
    # Only the text enclosed between <p> and <l> is segmented.
    paragraphs = doc.xpath('//tei:text//tei:p', namespaces=ns)
    lines = doc.xpath('//tei:text//tei:l', namespaces=ns)
    segment_elements(paragraphs)
    segment_elements(lines)
    # Used to lemmatize the text.
    if args.lemmatize:
        # If the text is only to be lemmatized, segs are lemmatized.
        tags = doc.xpath('//tei:seg', namespaces=ns)
        lemmatize(tags)
    # Indent() inserts tail whitespace for pretty-printing an XML tree.
    etree.indent(doc)
    # This output file is specific to the project e-ditiones, you can easily change the output with e.g. doc.write("New" + args.file, ...)
    return doc.write(args.file.replace("-2", "-3"), pretty_print=True, encoding="utf-8", method="xml")


# LEMMATIZATION ###############################################################

def lemmatize(segs):
    """
    This function process a lemmatization of the text.

    :param doc: a list of tags
    """
    # Change fr to freem for early modern french.
    model_name = "fr"
    tagger = get_tagger(model_name, batch_size=256, device="cpu", model_path=None)
    # Used for the new of the seg element (removed by .clear())
    n = 1
    for seg in segs:
        iterator, processor = get_iterator_and_processor()
        # There are two lemmatizations, one with the text with 'ſ' (named orig_lemmas), the other with 's' (nammed lemmas)
        seg_s = seg.text.replace('ſ', 's')
        orig_lemmas = tagger.tag_str(seg.text, iterator=iterator, processor=processor)
        lemmas = tagger.tag_str(seg_s, iterator=iterator, processor=processor)

        spanGrp = etree.Element("{http://www.tei-c.org/ns/1.0}spanGrp")
        # Lists containing the TEI elements to be added.
        # tei:span
        span_list = []
        # tei:w
        w_list = []
        # tei:fs
        fs_list = []

        # We check that both lists are still sames.        
        assert len(orig_lemmas) == len(lemmas)
        seg_id = seg.attrib["{http://www.w3.org/XML/1998/namespace}id"]
        id = 1
        for index in range(len(lemmas)):
            ### W
            w = etree.Element("{http://www.tei-c.org/ns/1.0}w")
            w.text = orig_lemmas[index]['form']
            w.attrib["{http://www.w3.org/XML/1998/namespace}id"] = seg_id + "w" + str(id)
            w_list.append(w)
            
            ### FS
            fs = etree.Element("{http://www.tei-c.org/ns/1.0}fs")
            fs.attrib["{http://www.w3.org/XML/1998/namespace}id"] = seg_id + "fs" + str(id)
            # This list contains the f element to be expanded in the fs element.
            f_list = []
            if lemmas[index]['lemma'] != None:
                f = etree.Element("{http://www.tei-c.org/ns/1.0}f")
                string = etree.Element("{http://www.tei-c.org/ns/1.0}string")
                f.attrib["name"] = "lemma"
                string.text = lemmas[index]['lemma']
                f.append(string)
                f_list.append(f)
            if lemmas[index]['POS'] != None:
                f = etree.Element("{http://www.tei-c.org/ns/1.0}f")
                symbol = etree.Element("{http://www.tei-c.org/ns/1.0}symbol")
                f.attrib["name"] = "pos"
                symbol.attrib["value"] = lemmas[index]['POS']
                f.append(symbol)
                f_list.append(f)
            if lemmas[index]['morph'] != None:
                f = etree.Element("{http://www.tei-c.org/ns/1.0}f")
                symbol = etree.Element("{http://www.tei-c.org/ns/1.0}symbol")
                f.attrib["name"] = "msd"
                symbol.attrib["value"] = lemmas[index]['morph']
                f.append(symbol)
                f_list.append(f)
            fs.extend(f_list)
            fs_list.append(fs)

            ### SPAN
            span = etree.Element("{http://www.tei-c.org/ns/1.0}span")
            span.attrib["target"] = "#" + w.attrib["{http://www.w3.org/XML/1998/namespace}id"]
            span.attrib["ana"] = "#" + fs.attrib["{http://www.w3.org/XML/1998/namespace}id"]
            span_list.append(span)

            id += 1

        seg.clear()
        # Attributes are deleted with .clear() we have to add it again.
        seg.attrib["{http://www.w3.org/XML/1998/namespace}id"] = "s" + str(n)
        n += 1
        seg.extend(w_list)
        # .extend() is used for a list of elements.
        spanGrp.extend(span_list)
        spanGrp.attrib["type"] = "wordForm"
        # .append() is used for a single element.
        seg.append(spanGrp)
        seg.extend(fs_list)


def rebuild_words(doc):
    """
    Used to rebuild a word separated by a lb element.
    For example :
    <lb/>I hope this script is use
    <lb break='no' rend='-'/>ful
    will give :
    <lb/>I hope this script is useful
    --> then all words can be tokenized correctly.

    :param doc: a XML document
    :return: the same document with rebuilt word.
    :rtype: a new XLM document
    """
    # For each line break wich splits a word in two, we want to remove it and reform the word.
    for lb in doc.xpath("//tei:lb[@break='no']", namespaces=ns):
        # We get the text where the first part of the word belongs.
        previous = lb.getprevious()
        # We get the second part.
        tail = lb.tail if lb.tail is not None else ""
        # We want to be sure that the element contains a string and we want to be sure that there is some text.
        # This prevents encoding errors.
        if previous != None and previous.tail != None:
            previous.tail = previous.tail.rstrip() + tail
        # Otherwise, we get the text of the parent element and we want to be sure that there is some text.
        elif lb.getparent().tail != None :
            lb.getparent().text = lb.getparent().text.rstrip() + tail
        lb.getparent().remove(lb)


if __name__ == "__main__":
    parser = etree.XMLParser(remove_blank_text=True)
    doc = etree.parse(args.file, parser)
    rebuild_words(doc)
    text_transformed = transform_text(doc)
    to_level_3(text_transformed)
