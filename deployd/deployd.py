# -*- encoding: utf-8 -*-

from metadata import DeploymentManifest
from virtualbox.deployment import VirtualBoxManifestDeployment

import requests
import time


class Deployd(object):
    """docstring for Deployd"""

    def __init__(self,api_base_url):
        self._api_base_url = api_base_url
        self._worker_id = worker_id

    def _get_worker_id(self):

    def _get_environments(self):
        endpoint = '/environment/environments/' 
        query = '?deployment__status=Pending&worker=%s' % self._worker_id
        url = self._api_base_url + endpoint + query
        response = requests.get(url)

        # Check if an error has occurred
        response.raise_for_status()
        environments = response.json()

        return environments


    def _parse_environments(self,environments):
        parsed = []
        for environment in environments:
            provider = environment.get('provider')
            name = environment.get('name')
            cpus = environment.get('cores')
            memory = environment.get('memory')

            data = {
                'provider': provider,
                'name': name,
                'specs': {
                    'cpus': cpus,
                    'memory': memory
                }
            }

            parsed.append(data)

        return parsed

    def _deploy_environment(self,environment):
        manifest = DeploymentManifest(data=environment)
        vbox_deployment = VirtualBoxManifestDeployment(manifest)
        vbox_deployment.run()

    def _deploy_environments(self):
        environments = self._get_environments()
        environments = self._parse_environments(environments)

        for environment in environments:
            self._deploy_environment(data=environment)

    def start(self):
        # what for a minute
        time.sleep(60)

        # (1) Register the node
        self._register_worker()

        # (2) Report worker status
        self._report_worker_status()

        # (2) Request and Deploy environments 
        self._deploy_environments()

    def run(self):
        while True:
            self.start()
