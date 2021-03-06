import xml.etree.cElementTree as ET
import os
import shutil
from typing import Tuple
from glob import glob
import xmltodict

from tools.xml_tools import prettify


class KanbanFinder:
    """ Class consisting of methods for finding and returning specific kanban info """

    @staticmethod
    def find_kanban_dir_with_id(
        kanban_id: int, kanbans_directory: str
    ) -> Tuple[str, bool]:
        """Returns directory as string, if direcotry not found return empty string"""
        all_kanbans = glob(os.path.join(kanbans_directory, "*"), recursive=True)
        for kanban_directory in all_kanbans:
            info = os.path.split(kanban_directory)
            if str(kanban_id) in info:
                found = kanban_directory
                break

        if "found" in locals():
            return found, True
        else:
            return "", False

    @staticmethod
    def return_all_kanabans_info(kanbans_directory: str) -> list:
        """ Return list with dictionaries consiting of kanbans info from config xml files """
        all_kanbans = glob(os.path.join(kanbans_directory, "*"), recursive=True)
        print(all_kanbans)
        all_kanbans_info = []
        for single_kanban_directory in all_kanbans:
            if os.path.isdir(single_kanban_directory):
                single_kanban_config = os.path.join(
                    single_kanban_directory, "config.xml"
                )
                with open(single_kanban_config, "r") as xml_file:
                    all_kanbans_info.append(xmltodict.parse(xml_file.read()))

        return all_kanbans_info

    @staticmethod
    def return_kanban_info(kanban_directory: str) -> list:
        kanban_config_file = os.path.join(kanban_directory, "config.xml")
        with open(kanban_config_file) as xml_file:
            kanban_info = xmltodict.parse(xml_file.read())

        return kanban_info

    @staticmethod
    def define_next_kanban_id(kanbans_directory: str) -> int:
        with open(
            os.path.join(kanbans_directory, "next_kanban_id"), "r"
        ) as kanban_id_file:
            kanban_issue_id = kanban_id_file.readline()
        next_kanban_id = int(kanban_issue_id)
        return next_kanban_id


class KanbanCreator:
    """ Class consisting of methods for creating kanban boards objects """

    @staticmethod
    def create_new_kanban_folder(kanbans_directory: str) -> Tuple[str, int]:
        """ Creates new kanban folder and returns new directory with new kanban id """
        all_kanbans = glob(os.path.join(kanbans_directory, "*"), recursive=True)
        try:
            new_kanban_id = KanbanFinder.define_next_kanban_id(
                kanbans_directory=kanbans_directory
            )
        except FileNotFoundError:
            new_kanban_id = 1
        new_kanban_directory = os.path.join(kanbans_directory, str(new_kanban_id))
        os.mkdir(new_kanban_directory)

        return new_kanban_directory, new_kanban_id

    @staticmethod
    def create_new_kanban_config(
        kanbans_directory: str,
        kanban_id: int,
        new_kanban_directory: str,
        config_xml_tree,
    ) -> None:
        with open(
            os.path.join(new_kanban_directory, "config.xml"), "w+"
        ) as config_file:
            config_file.write(config_xml_tree)

        with open(
            os.path.join(kanbans_directory, "next_kanban_id"), "w+"
        ) as kanban_id_file:
            kanban_id_file.write(str(kanban_id + 1))

    @staticmethod
    def create_xml_tree_for_kanban_config(
        kanban_name: str, kanban_id: int, description: str = ""
    ):
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
            return None


class KanbanDeleter:
    @staticmethod
    def delete_kanban(kanbans_directory: str, kanban_id: str):
        kanban_directory = os.path.join(kanbans_directory, str(kanban_id))
        shutil.rmtree(kanban_directory)
