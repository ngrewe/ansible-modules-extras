import collections
import inspect
import mock
from packet.Project import Project
import yaml


def param_setter_from_doc(module_name, func):
    '''Convert the documenation of the method to module parameters

    This function extracts the docstring from the specified function,
    parses it as a YAML document, and returns parameters for the
    module.

    '''

    doc = inspect.getdoc(func)
    cfg = yaml.load(doc)

    for task in cfg:
        for module, params in task.items():
            task[module] = collections.defaultdict(str,
                                               params)

    return lambda self: setattr(self, 'params', cfg[0][module_name])


class Manager(object):

    def __init__(self):
        self.projects = []

    def list_projects(self, params={}):
        return self.projects

    @mock.patch('packet.Project.Project')
    def create_project(self, name, mock_cls):
        p = mock_cls()
        p.name = name
        return p


class AnsibleExitOk(Exception):
    """Marker exception for positive exit conditions."""
    pass
