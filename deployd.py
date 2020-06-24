# -*- encoding: utf-8 -*-

"""
VirtualMachines deployment daemon
"""


import glob
import os


class Deployd(object):
    """docstring for Deployd"""

    def __init__(self, manifests_folder):
        super(Deployd, self).__init__()
        self._manifests_folder = manifests_folder

    @staticmethod
    def check_for_manifests():
        lookup = os.path.join(self._manifests_folder,'*.yml')
        files_names = glob.glob(lookup)



class DeployVirtualBoxManifest(object):
    """docstring for DeployManifest"""
    def __init__(self, arg):
        super(DeployManifest, self).__init__()
        self.arg = arg
        