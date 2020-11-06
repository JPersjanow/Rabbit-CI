from glob import glob
import os

class KanbanFinder:
    @staticmethod
    def find_kanban_dir_with_id(kanban_id: int, kanbans_directory: str) -> str:
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
