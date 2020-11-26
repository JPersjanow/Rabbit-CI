import xml.etree.cElementTree as ET
import os
from glob import glob
from typing import Tuple
from datetime import datetime
from enum import Enum
import xmltodict

from flask import jsonify

try:
    from tools.xml_tools import (
        prettify,
        return_xml_attribute_value,
        update_xml_attribute,
        add_xml_attribute_to_child,
        remove_xml_attribute_with_value,
    )
except ModuleNotFoundError:
    from xml_tools import (
        prettify,
        return_xml_attribute_value,
        update_xml_attribute,
        add_xml_attribute_to_child,
        remove_xml_attribute_with_value,
    )


class Stages(Enum):
    """ Stages enum class for keeping them in a proper structure rather than string """

    ToDo = "todo"
    Doing = "doing"
    Done = "done"


class IssueCreator:
    """ Class consiting of methods for creating issues """

    @staticmethod
    def create_issue_folder(kanbans_directory: str, kanban_id: int) -> str:
        kanbans_directory = os.path.join(kanbans_directory, str(kanban_id))
        issues_directory = os.path.join(kanbans_directory, "issues")

        if not os.path.isdir(issues_directory):
            os.mkdir(issues_directory)

        return issues_directory

    @staticmethod
    def create_xml_tree_for_issue_config(
        issue_name: str,
        kanban_id: id,
        issue_id: id,
        issue_description: str = "",
        creator: str = "unknown",
    ) -> ET.ElementTree:
        """ Method for creating xml tree for issue config """
        date = datetime.date(datetime.now())
        try:
            root = ET.Element("issue")
            ET.SubElement(root, "name").text = issue_name
            ET.SubElement(root, "issue_id").text = str(issue_id)
            ET.SubElement(root, "kanban_id").text = str(kanban_id)
            ET.SubElement(root, "description").text = issue_description
            ET.SubElement(root, "stage").text = Stages.ToDo.value
            ET.SubElement(root, "creator").text = creator
            ET.SubElement(root, "creation_date").text = str(date)
            tree = prettify(root)
            return tree
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def create_new_issue_config(
        kanbans_directory: str,
        kanban_id: int,
        issue_name: str,
        issue_description: str = "",
        creator: str = "unknown",
    ):
        issues_directory = os.path.join(kanbans_directory, str(kanban_id), "issues")
        all_issues_id = IssueFinder.get_all_issues_ids(issues_directory)
        if not all_issues_id:
            issue_id = 1
        else:
            issue_id = IssueFinder.define_next_issue_id(issues_directory)

        issue_xml_tree = IssueCreator.create_xml_tree_for_issue_config(
            issue_name=issue_name,
            issue_id=issue_id,
            kanban_id=kanban_id,
            issue_description=issue_description,
            creator=creator,
        )
        issue_config = os.path.join(issues_directory, f"{issue_id}.xml")
        if issue_xml_tree is not None:
            with open(issue_config, "w+") as issue_config_file:
                issue_config_file.write(issue_xml_tree)

        with open(
            os.path.join(issues_directory, "next_issue_id"), "w+"
        ) as issue_id_file:
            issue_id_file.write(str(issue_id + 1))


class IssueFinder:
    """ Class consisting of methods for finding issues and issues related objects """

    @staticmethod
    def define_next_issue_id(issues_directory: str) -> int:
        with open(
            os.path.join(issues_directory, "next_issue_id"), "r"
        ) as issue_id_file:
            next_issue_id = issue_id_file.read(1)
        next_issue_id = int(next_issue_id)
        return next_issue_id

    @staticmethod
    def get_all_issues_ids(issues_directory: str) -> list:
        all_issues = glob(os.path.join(issues_directory, "*.xml"))
        all_issues_id = [
            int(os.path.split(issue)[1].replace(".xml", "")) for issue in all_issues
        ]
        return all_issues_id

    @staticmethod
    def get_all_issues_files_with_dir(issues_directory: str) -> list:
        all_issues = glob(os.path.join(issues_directory, "*.xml"))
        return all_issues

    @staticmethod
    def get_all_issues_files(issues_directory: str) -> list:
        all_issues = glob(os.path.join(issues_directory, "*.xml"))
        all_issues_files = [os.path.split(issue)[1] for issue in all_issues]
        return all_issues_files

    @staticmethod
    def check_if_issue_extists(issues_directory: str, issue_id: int) -> bool:
        if issue_id in IssueFinder.get_all_issues_ids(issues_directory):
            return True
        else:
            return False

    @staticmethod
    def return_issue_info(issue_directory: str) -> dict:
        with open(issue_directory, "r") as issue_xml:
            issue_info = xmltodict.parse(issue_xml.read())
        return issue_info

    @staticmethod
    def return_issues_directory_for_kanban(
        kanbans_directory: str, kanban_id: int
    ) -> str:
        issues_directory = os.path.join(kanbans_directory, str(kanban_id), "issues")
        return issues_directory

    def return_issue_info_for_kanban(
        self, kanbans_directory: str, kanban_id: int, issue_id
    ) -> list:
        kanban_directory = os.path.join(kanbans_directory, str(kanban_id))
        issue_directory = os.path.join(
            kanban_directory, "issues", f"{str(issue_id)}.xml"
        )
        issue_info = self.return_issue_info(issue_directory=issue_directory)

        return issue_info

    def return_all_issues_info_for_kanban(
        self, kanbans_directory: str, kanban_id: int
    ) -> list:
        kanbans_directory = os.path.join(kanbans_directory, str(kanban_id))
        issues_directory = os.path.join(kanbans_directory, "issues")
        all_issues_directories = self.get_all_issues_files_with_dir(
            issues_directory=issues_directory
        )
        all_issues_directories = sorted(all_issues_directories)
        all_issues_info = []
        for issue_directory in all_issues_directories:
            all_issues_info.append(
                self.return_issue_info(issue_directory=issue_directory)
            )

        return all_issues_info


class IssueUpdater:
    """ Class consisting of methods for updating issues and issues related objects """

    @staticmethod
    def update_issue_for_kanban(
        kanbans_directory: str,
        kanban_id: int,
        issue_id: int,
        attribute_name: str,
        attribute_value: str,
    ):
        issue_file_with_dir = os.path.join(
            kanbans_directory, str(kanban_id), "issues", f"{str(issue_id)}.xml"
        )
        update_xml_attribute(
            xml_file=issue_file_with_dir,
            attribute_name=attribute_name,
            new_value=attribute_value,
        )

    @staticmethod
    def update_issue(
        issues_directory: str, issue_id: int, attribute_name: str, attribute_value: str
    ):
        issue_file_with_dir = os.path.join(issues_directory, f"{str(issue_id)}.xml")
        update_xml_attribute(
            xml_file=issue_file_with_dir,
            attribute_name=attribute_name,
            new_value=attribute_value,
        )


class IssueDeleter:
    """ Class consisting of methods for deleting issues and issues related objects """

    @staticmethod
    def delete_issue_for_kanban(kanbans_directory: str, kanban_id: int, issue_id: int):
        issue_file_with_dir = os.path.join(
            kanbans_directory, str(kanban_id), "issues", f"{str(issue_id)}.xml"
        )
        os.remove(issue_file_with_dir)


class IssueStageHandler:
    """ Class consisting of methods for handling issues stages and issues stages related objects """

    @staticmethod
    def check_stage(kanbans_directory: str, kanban_id: int, issue_id: int) -> str:
        issue_xml = os.path.join(
            kanbans_directory, str(kanban_id), "issues", f"{str(issue_id)}.xml"
        )

        return return_xml_attribute_value(xml_file=issue_xml, attribute_name="stage")

    @staticmethod
    def change_stage(
        kanbans_directory: str, kanban_id: int, issue_id: int, stage_to_assign: str
    ):
        kanban_config = os.path.join(kanbans_directory, str(kanban_id), "config.xml")
        issue_xml = os.path.join(
            kanbans_directory, str(kanban_id), "issues", f"{issue_id}.xml"
        )
        current_stage = return_xml_attribute_value(
            xml_file=issue_xml, attribute_name="stage"
        )

        update_xml_attribute(issue_xml, "stage", stage_to_assign)
        add_xml_attribute_to_child(
            xml_file=kanban_config,
            attribute_name=stage_to_assign,
            new_attribute_name="issue_id",
            new_attribute_value=str(issue_id),
        )
        remove_xml_attribute_with_value(
            xml_file=kanban_config,
            attribute_name=current_stage,
            attribute_name_delete="issue_id",
            attribute_value_delete=str(issue_id),
        )


if __name__ == "__main__":
    isfind = IssueFinder()
    print(
        int(
            isfind.define_next_issue_id(
                issues_directory="/home/persil/rabbit/kanbans/2/issues"
            )
        )
    )
