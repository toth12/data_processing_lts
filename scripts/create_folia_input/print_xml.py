import xml.dom.minidom

def pretty_print(xml_string):
    x=xml.dom.minidom.parseString(xml_string)
    pretty_xml_as_string = x.toprettyxml()
    print pretty_xml_as_string
