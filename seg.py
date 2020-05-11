from lxml import etree
import re
import sys

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
        seg = etree.Element("seg")
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
    lines = doc.xpath('TEI//tei:text//tei:l', namespaces=ns)
    segment_elements(paragraphs)
    segment_elements(lines)
    return doc.write("Segmented_" + str(sys.argv[1]), pretty_print=True, encoding="utf-8")


if __name__ == "__main__":
    parser = etree.XMLParser(remove_blank_text=True)
    doc = etree.parse(sys.argv[1], parser)
    text_transformed = transform_text(doc)
    segment_document(text_transformed)
