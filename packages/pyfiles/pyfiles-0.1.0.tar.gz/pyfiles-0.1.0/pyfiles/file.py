import os
import stat
from pathlib import Path
from dataclasses import dataclass

class File:
    def __init__(self, filepath: str):
        self.path = Path(filepath)
        if not self.path.exists():
            raise FileNotFoundError(f"{filepath} doesn't exists")
        if not self.path.is_file():
            raise TypeError(f"{filepath} doesn't a file")
        self.info = os.stat(filepath)
        self._size = self.info.st_size
        self._mode = stat.filemode(self.info.st_mode)
        self._inode = self.info.st_ino
        self.permission = FilePermission(self)
        self.content = FileContent(self.path)
    
    @property
    def size(self):
        return self._size
    
    @property
    def mode(self):
        return self._mode
    
    @property
    def inode(self):
        return self._inode

    def change_at(self):
        return self.info.st_ctime
    
    def modify_at(self):
        return self.info.st_mtime
    
    def access_at(self):
        return self.info.st_atime
    

class FileContent:
    def __init__(self, path: str):
        self._path = path
    
    def append_to_file(self, content):
        with open(self._path, '+a') as file:
            file.write(content)

    def read_only(self):
        with open(self._path, 'r') as file:
            for line in file.readlines():
                yield line

class FilePermission:
    def __init__(self, file: File):
        self.owner = _Permission(*file.mode[1:4])
        self.group = _Permission(*file.mode[4:7])
        self.others = _Permission(*file.mode[7:])
    

    

class _Permission:
    def __init__(self, read: str, write: str, execute: str):
        self.read = read
        self.write = write
        self.execute = execute
    
    def is_executable(self) -> bool:
        return True if self.execute == "x" else False
    
    def is_writable(self) -> bool:
        return True if self.write == "w" else False
    
    def is_readable(self) -> bool:
        return True if self.read == "r" else False
    


@dataclass
class Permissions:
    read: str
    write: str
    execute: str

    def is_executable(self) -> bool:
        return True if self.execute == "x" else False
    
    def is_writable(self) -> bool:
        return True if self.write == "w" else False
    
    def is_readable(self) -> bool:
        return True if self.read == "r" else False


    





class InfoFile:
    def __init__(self, file: File):
        self.info_file = stat(file.path)
    
    @property
    def size(self) -> str:
        return self.info_file.st_size
    
    @property
    def mode(self):
        return self.info_file.st_mode
    
