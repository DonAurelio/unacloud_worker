# -*- encoding: utf-8 -*-


import yaml


class VirtualMachineDefFile(object):
   
    @staticmethod
    def _load_from_text(text):
        data = yaml.load(text)
        return data

    @staticmethod
    def _load_from_file(file_path):
        with open(file_path,'r') as file:
            data = yaml.load(file)
            return data

    def __init__(self,raw_text=None,file_path=None, data=None):
        if raw_text:
            self._data = self._load_from_text(raw_text)
        elif file_path:
            self._data = self._load_from_file(file_path)
        elif data:
            self._data = data
        else:
            self._data = None

    @property
    def data(self):
        return self._data

    @property
    def name(self):
        return self._data.get('name', None)

    @property
    def type(self):
        return self._data.get('cpus', None)

    @property
    def cpus(self):
        return self._data.get('cpus', 1)

    @property
    def memory(self):
        return self._data.get('memory', 512)

    @property
    def ports(self):
        return self._data.get('ports', None)
    