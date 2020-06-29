# -*- encoding: utf-8 -*-

from metadata import DeploymentManifest
from virtualbox.deployment import VirtualBoxManifestDeployment

import logging
import requests
import time
import glob
import os


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s')
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)


# Absolute path to the deployd directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to the resources directory holding .vdi template disc.
MANIFESTS_PATH = os.path.join(BASE_DIR,'manifests')

# Base API url without the ending slash
API_BASE_URL = 'http://localhost:8082'

# Wait time for next iteration (seconds)
SLEEP_SECONDS = 5


def get_manifests():
    logger.info("Loading manifests from '%s' directory ...", MANIFESTS_PATH)
    lookup = os.path.join(MANIFESTS_PATH,'*.yml')
    paths = glob.glob(lookup)
    logger.info("Finded manifests '%s'" % len(paths))
    return paths

def report_deployment_status(manifest,vbox_deployment):
    if vbox_deployment.is_success():
        vm_data, statistics = vbox_deployment.get_deployment_data()

        try:
            environment_id = vm_data.get('name')
            environment_address = vm_data.get('address')
            environment_ssh_port = vm_data.get('ssh_port')

            environment = {
                'name': environment_id,
                'id': environment_id,
                'address': environment_address,
                'ssh_port': environment_ssh_port
            }

            data = {
                'deployment_is_success': True,
                'environment': environment,
                'statistics': statistics
            }

            endpoint = '/environments/status_updates/'
            url = API_BASE_URL + endpoint
            response = requests.post(url,json=data)
            response.raise_for_status()

        except requests.exceptions.ConnectionError as e:
            message = (
                "Can't repot enviroment '%s' success deployment "
                "status to API SERVER"
            ) % vm_data.get('name')

            logger.error(message)
            logger.error(e)
        except Exception as e:
            vbox_deployment.delete()
            delete_manifest(manifest)
            logger.error(e)

    else:
        message = vbox_deployment.get_deployment_message()
        data = {
            'deployment_is_success': False,
            'message': message
        }

        try:
            endpoint = '/environments/status_updates/'
            url = API_BASE_URL + endpoint
            response = requests.post(url,json=data)
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            message = (
                "Can't repot enviroment '%s' failed deployment "
                "status to API SERVER"
            ) % manifest.name
            logger.error(message)
            logger.error(e)

def delete_manifest(manifest):
    file_path = manifest.file_path
    if  os.path.exists(file_path):
        os.remove(file_path)

def deploy_environment(file_path):
    logger.info("Deploy manifest '%s'" % file_path)
    manifest = DeploymentManifest(file_path=file_path)
    vbox_deployment = VirtualBoxManifestDeployment(manifest)
    vbox_deployment.run()
    report_deployment_status(manifest,vbox_deployment)
    delete_manifest(manifest)

def deploy():
    logger.info("Deployment ...")
    manifests_paths = get_manifests()
    for manifest_path in manifests_paths:
        deploy_environment(manifest_path)
    logger.info("End deployment ...")


if __name__ == '__main__':
    logger.info("Deployd started !!")
    while True:
        try: 
            time.sleep(SLEEP_SECONDS)
            deploy()
        except requests.exceptions.ConnectionError as e:
            logger.exception(e)
        except Exception as e:
            logger.exception(e)
