from xml.dom import minidom
import xml.etree.cElementTree as ET

def prettify(elem):
    """Method for prettyfying xml files"""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def create_xml_tree_for_kanban_config(kanban_name: str, kanban_id: int, description: str = ""):
    """Method for creating xml tree for kanban config"""
    try:
        root = ET.Element("kanban")
        info = ET.SubElement(root, "info")
        ET.SubElement(info, "name").text = kanban_name
        ET.SubElement(info, "id").text = str(kanban_id)
        ET.SubElement(info, "description").text = description
        tree = prettify(root)
        return tree
    except Exception as e:
        print(e)
        return None

def update_xml_attribute(xml_file: str, attribute_name: str, new_value: str):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for child in root:
        child.find(attribute_name).text = new_value
    tree.write(xml_file)

