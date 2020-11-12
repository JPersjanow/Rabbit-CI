import xml.etree.cElementTree as ET
from xml.dom import minidom


def prettify(elem) -> str:
    """Method for prettyfying xml files"""
    rough_string = ET.tostring(elem, "utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def update_xml_attribute(xml_file: str, attribute_name: str, new_value: str) -> None:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    found = False

    for child in root:
        if child.tag == attribute_name:
            found = True
            child.text = new_value
    if not found:
        for child in root:
            for child_n in child:
                if child_n.tag == attribute_name:
                    child_n.text = new_value
    tree.write(xml_file)


def add_xml_attribute_to_root(
    xml_file: str, attribute_name: str, attribute_value: str = ""
) -> None:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ET.SubElement(root, attribute_name).text = attribute_value
    tree.write(xml_file)


def add_xml_attribute_to_child(
    xml_file: str,
    attribute_name: str,
    new_attribute_name: str,
    new_attribute_value: str,
) -> None:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for child in root.iter(attribute_name):
        ET.SubElement(child, new_attribute_name).text = new_attribute_value
    prettify(root)
    tree.write(xml_file)


def remove_xml_attribute_with_value(
    xml_file: str,
    attribute_name: str,
    attribute_name_delete: str,
    attribute_value_delete: str,
) -> None:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for child in root.iter(attribute_name):
        for child_in in child.iter(attribute_name_delete):
            if child_in.text == attribute_value_delete:
                child.remove(child_in)
    tree.write(xml_file)


def return_xml_attribute_value(xml_file: str, attribute_name: str) -> str:
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for child in root:
        if child.tag == attribute_name:
            return child.text