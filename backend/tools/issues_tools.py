import xml.etree.cElementTree as ET
import os
from glob import glob
import xmltodict
from tools.xml_tools import prettify

class IssueFinder:
    @staticmethod
    def return_all_issues_info_for_kanban(kanbans_directory: str, kanban_id: str) -> list:
        all_issues_info = []
        issues_directory = os.path.join(kanbans_directory, str(kanban_id), 'issues')
        if IssueCreator.check_if_issues_directory_exists(issues_directory=issues_directory):
            all_issues = glob(os.path.join(issues_directory, '*.xml'))
            for issue in all_issues:
                with open(issue, 'r') as issue_xml:
                    all_issues_info.append(xmltodict.parse(issue_xml.read()))
            return all_issues_info
        else:
            raise FileNotFoundError("No issues exist for this kanban")

class IssueCreator:
    @staticmethod
    def create_issues_folder(kanbans_directory: str, kanban_id: int) -> str:
        kanban_directory = os.path.join(kanbans_directory, str(kanban_id))
        issues_directory = os.path.join(kanban_directory, 'issues')
        if not IssueCreator.check_if_issues_directory_exists(issues_directory=issues_directory):
            os.mkdir(issues_directory)
        
        return issues_directory
    
    @staticmethod
    def check_if_issues_directory_exists(issues_directory: str) -> bool:
        return os.path.isdir(issues_directory)
    
    @staticmethod
    def check_if_issue_exists(issues_directory: str, issue_name: str) -> bool:
        return os.path.isfile(os.path.join(issues_directory, f'{issue_name}.xml'))

    @staticmethod
    def create_new_issue_config(kanbans_directory: str, kanban_id: int, issues_directory: str, issue_name: str, xml_tree):
        kanban_directory = os.path.join(kanbans_directory, str(kanban_id))
        new_issues_directory = os.path.join(kanban_directory, issues_directory)
        new_issue_config = os.path.join(new_issues_directory, f'{issue_name}.xml')
        if not IssueCreator.check_if_issue_exists(new_issues_directory, issue_name):
            with open(new_issue_config, 'w+') as issue_config:
                issue_config.write(xml_tree)
        else:
            raise FileExistsError("Issue already exists!")

    @staticmethod
    def create_xml_tree_for_issue_config(issue_name: str, kanban_id: int, issue_description: str = ""):
        """Method for creating xml tree for issue config"""
        try:
            root = ET.Element("issue")
            ET.SubElement(root, "name").text = issue_name
            ET.SubElement(root, "kanban_id").text = str(kanban_id)
            ET.SubElement(root, "description").text = issue_description
            tree = prettify(root)
            return tree
        except Exception as e:
            print(e)
            return None

if __name__ == '__main__':
    issue_finder = IssueFinder()
    all_issues = issue_finder.return_all_issues_info_for_kanban(kanbans_directory='/home/persil/rabbit/kanbans', kanban_id=1)