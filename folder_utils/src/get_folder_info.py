import os
from datetime import datetime
from pathlib import Path
from glob import glob


class FolderInfo(object):
    def __init__(self, path: str) -> None:
        self.path = Path(path).resolve()

    def folder_exists(self) -> bool:
        if os.path.exists(self.path):
            return True
        return False

    def get_memory_usage(self) -> int: ...
    
    def get_last_data_update(self) -> datetime: ...

    def get_directories_in_path(self) -> list: ...

    def get_files_in_path(self) -> list:
        return glob(f'{self.path}{os.sep}*.*')

    def __get_type(self):
        if self.path.is_dir():
            return 'Directory'
        if self.path.is_file():
            return 'File'
    
    def __repr__(self):
        _type = self.__get_type()
        _exists = self.folder_exists()
        return f'Type: {_type} Exists: {_exists}'
