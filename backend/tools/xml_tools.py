from xml.dom import minidom
import xml.etree.cElementTree as ET


def prettify(elem):
    """Method for prettyfying xml files"""
    rough_string = ET.tostring(elem, "utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def update_xml_attribute(xml_file: str, attribute_name: str, new_value: str):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for child in root:
        if child.find(attribute_name) is not None:
            child.find(attribute_name).text = new_value

    tree.write(xml_file)


def add_xml_attribute_to_root(
    xml_file: str, attribute_name: str, attribute_value: str = ""
):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ET.SubElement(root, attribute_name).text = attribute_value
    tree.write(xml_file)
