# -*- encoding: utf-8 -*-

from metadata import DeploymentManifest
from virtualbox.deployment import VirtualBoxManifestDeployment

import os
import glob


class Deployd(object):
    """docstring for Deployd"""

    def __init__(self, manifests_folder):
        super(Deployd, self).__init__()
        self._manifests_folder = manifests_folder

    def _get_manifests(self):
        lookup = os.path.join(self._manifests_folder,'*.yml')
        files_paths = glob.glob(lookup)
        return files_paths


    def _deploy_manifest(self,path):
        manifest = DeploymentManifest(file_path=path)
        vbox_deployment = VirtualBoxManifestDeployment(manifest)
        vbox_deployment.run()

    def _deploy_manifests(self):
        manifests_paths = self._get_manifests()
        for manifest_path in manifests_paths:
            self._deploy_manifest(manifest_path)

    def run(self):
        self._deploy_manifests()