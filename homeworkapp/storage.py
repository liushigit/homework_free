# coding:utf-8
from django.core.files.storage import FileSystemStorage
import os


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name):
        p = self.path(name).encode('utf-8')
        if os.path.exists(p):
            os.remove(p)
        return name
