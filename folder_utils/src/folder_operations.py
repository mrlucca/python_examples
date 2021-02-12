import os
import shutil
from folder_utils.src.get_folder_info import FolderInfo


class FolderOperations(object):
    def __init__(self, path: str) -> None:
        self.path = path
        self.info = FolderInfo(self.path)

    def remove_tree(self) -> bool: ...

    def copy_tree(self) -> bool: ...

    def delete_tree_folder_by_date(self) -> bool: ...
