import xml.etree.cElementTree as ET
from typing import Tuple
from glob import glob
import os
import xmltodict

from tools.xml_tools import prettify

class KanbanFinder:
    """ Class consisting of methods for finding and returning specific kanban info """
    @staticmethod
    def find_kanban_dir_with_id(kanban_id: int, kanbans_directory: str) -> Tuple[str, bool]:
        """Returns directory as string, if direcotry not found return empty string"""
        all_kanbans = glob(os.path.join(kanbans_directory, '*'), recursive=True)
        for kanban_directory in all_kanbans:
            info = os.path.split(kanban_directory)
            if str(kanban_id) in info:
                found = kanban_directory
                break
        
        if 'found' in locals():
            return found, True
        else:
            return '', False

    @staticmethod
    def return_all_kanabans_info(kanbans_directory: str) -> list:
        """ Return list with dictionaries consiting of kanbans info from config xml files """
        all_kanbans = glob(os.path.join(kanbans_directory, '*'), recursive=True)
        print(all_kanbans)
        all_kanbans_info = []
        for single_kanban_directory in all_kanbans:
            single_kanban_config = os.path.join(single_kanban_directory, 'config.xml')
            with open(single_kanban_config, 'r') as xml_file:
                all_kanbans_info.append(xmltodict.parse(xml_file.read()))

        return all_kanbans_info

    @staticmethod
    def return_kanban_info(kanban_directory: str) -> list:
        kanban_config_file = os.path.join(kanban_directory, 'config.xml')
        with open(kanban_config_file) as xml_file:
                kanban_info = xmltodict.parse(xml_file.read())

        return kanban_info

class KanbanCreator:
    @staticmethod
    def create_new_kanban_folder(kanbans_directory: str) -> Tuple[str, int]:
        """ Creates new kanban folder and returns new directory with new kanban id """
        all_kanbans = glob(os.path.join(kanbans_directory, '*'), recursive=True)
        new_kanban_id = len(all_kanbans) + 1
        new_kanban_directory = os.path.join(kanbans_directory, str(new_kanban_id))
        os.mkdir(new_kanban_directory)

        return new_kanban_directory, new_kanban_id

    @staticmethod
    def create_new_kanban_config(new_kanban_directory: str, config_xml_tree) -> None:
        with open(os.path.join(new_kanban_directory, 'config.xml'), 'w+') as config_file:
            config_file.write(config_xml_tree)

    @staticmethod
    def create_xml_tree_for_kanban_config(kanban_name: str, kanban_id: int, description: str = ""):
        """Method for creating xml tree for kanban config"""
        try:
            root = ET.Element("kanban")
            info = ET.SubElement(root, "info")
            ET.SubElement(info, "name").text = kanban_name
            ET.SubElement(info, "id").text = str(kanban_id)
            ET.SubElement(info, "description").text = description
            ET.SubElement(root, "todo")
            ET.SubElement(root, "doing")
            ET.SubElement(root, "done")
            tree = prettify(root)
            return tree
        except Exception as e:
            print(e)
            return None