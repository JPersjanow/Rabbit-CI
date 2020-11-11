import xml.etree.cElementTree as ET
import os
from glob import glob
from typing import Tuple
from datetime import datetime
from enum import Enum
import xmltodict

from tools.xml_tools import (
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


class IssueFinder:
    """ Class consisting of methods for finding and returning specific issue info """

    @staticmethod
    def return_all_issues_info_for_kanban(
        kanbans_directory: str, kanban_id: int
    ) -> list:
        all_issues_info = []
        issues_directory = os.path.join(kanbans_directory, str(kanban_id), "issues")
        if IssueFinder.check_if_issues_directory_exists(
            issues_directory=issues_directory
        ):
            all_issues = glob(os.path.join(issues_directory, "*.xml"))
            for issue in all_issues:
                with open(issue, "r") as issue_xml:
                    all_issues_info.append(xmltodict.parse(issue_xml.read()))
        return all_issues_info

    @staticmethod
    def check_if_issues_directory_exists(issues_directory: str) -> bool:
        return os.path.isdir(issues_directory)

    @staticmethod
    def check_if_issue_exists(issues_directory: str, issue_name: str) -> bool:
        return os.path.isfile(os.path.join(issues_directory, f"{issue_name}.xml"))

    @staticmethod
    def return_specific_issue_for_kanban(
        kanbans_directory: str, kanban_id: int, issue_name: str
    ) -> Tuple[str, bool]:
        issues_directory = os.path.join(kanbans_directory, str(kanban_id), "issues")
        if IssueFinder.check_if_issues_directory_exists(
            issues_directory=issues_directory
        ):
            all_issues = glob(os.path.join(issues_directory, "*.xml"))
            for issue in all_issues:
                if f"{issue_name}.xml" in os.path.split(issue):
                    found = issue
                    break

            if "found" in locals():
                return found, True
            else:
                return "", False
        else:
            raise FileNotFoundError(
                "No issues exist for this kanban or kanban doesn't exits"
            )

    @staticmethod
    def return_issue_info(issue_directory: str) -> dict:
        with open(issue_directory, "r") as issue_xml:
            issue_info = xmltodict.parse(issue_xml.read())

        return issue_info


class IssueCreator:
    """ Class consisting of methods for creating issue objects """

    @staticmethod
    def create_issues_folder(kanbans_directory: str, kanban_id: int) -> str:
        kanban_directory = os.path.join(kanbans_directory, str(kanban_id))
        issues_directory = os.path.join(kanban_directory, "issues")
        if not IssueFinder.check_if_issues_directory_exists(
            issues_directory=issues_directory
        ):
            os.mkdir(issues_directory)

        return issues_directory

    @staticmethod
    def create_new_issue_config(
        kanbans_directory: str,
        kanban_id: int,
        issues_directory: str,
        issue_name: str,
        xml_tree,
    ):
        kanban_directory = os.path.join(kanbans_directory, str(kanban_id))
        new_issues_directory = os.path.join(kanban_directory, issues_directory)
        new_issue_config = os.path.join(new_issues_directory, f"{issue_name}.xml")
        if not IssueFinder.check_if_issue_exists(new_issues_directory, issue_name):
            with open(new_issue_config, "w+") as issue_config:
                issue_config.write(xml_tree)
        else:
            raise FileExistsError("Issue already exists!")

    @staticmethod
    def rename_issue(issue_directory: str, issue_name: str, new_issue_name: str):
        new_issue_directory = issue_directory.replace(issue_name, new_issue_name)
        update_xml_attribute(
            xml_file=issue_directory, attribute_name="name", new_value=new_issue_name
        )
        os.rename(issue_directory, new_issue_directory)

    @staticmethod
    def create_xml_tree_for_issue_config(
        issue_name: str,
        kanban_id: int,
        issue_description: str = "",
        creator: str = "anonymous",
    ):
        """Method for creating xml tree for issue config"""
        date = datetime.date(datetime.now())
        try:
            root = ET.Element("issue")
            ET.SubElement(root, "name").text = issue_name
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


class IssueDeleter:
    """ Class consisting of methods for deleting given issue """
    @staticmethod
    def delete_issue(kanbans_directory: str, kanban_id: int, issue_name: str):
        kanban_directory = os.path.join(kanbans_directory, str(kanban_id))
        issues_directory = os.path.join(kanban_directory, "issues")
        if IssueFinder.check_if_issue_exists(
            issues_directory=issues_directory, issue_name=issue_name
        ):
            os.remove(os.path.join(issues_directory, f"{issue_name}.xml"))
        else:
            raise FileNotFoundError


class IssueStageHandler:
    """ Class consisting of methods for handling issues within stages """
    @staticmethod
    def check_stage(kanbans_directory: str, kanban_id: int, issue_name: str) -> str:
        kanban_directory = os.path.join(kanbans_directory, str(kanban_id))
        issues_directory = os.path.join(kanban_directory, "issues")
        issue_xml = os.path.join(issues_directory, f"{issue_name}.xml")

        return return_xml_attribute_value(xml_file=issue_xml, attribute_name="stage")

    @staticmethod
    def change_stage(
        kanbans_directory: str, kanban_id: int, issue_name: str, stage_to_assign: str
    ):
        kanban_directory = os.path.join(kanbans_directory, str(kanban_id))
        kanban_config = os.path.join(kanban_directory, "config.xml")
        issues_directory = os.path.join(kanban_directory, "issues")
        issue_xml = os.path.join(issues_directory, f"{issue_name}.xml")
        current_stage = return_xml_attribute_value(
            xml_file=issue_xml, attribute_name="stage"
        )

        update_xml_attribute(issue_xml, "stage", stage_to_assign)
        add_xml_attribute_to_child(
            xml_file=kanban_config,
            attribute_name=stage_to_assign,
            new_attribute_name="issue",
            new_attribute_value=issue_name,
        )
        remove_xml_attribute_with_value(
            xml_file=kanban_config,
            attribute_name=current_stage,
            attribute_name_delete="issue",
            attribute_value_delete=issue_name,
        )
