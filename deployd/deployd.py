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
API_BASE_URL = 'http://localhost:8082/api'

# Wait time for next iteration (seconds)
SLEEP_SECONDS = 5


def get_manifests():
    logger.info("Loading manifests from '%s' directory ...", MANIFESTS_PATH)
    lookup = os.path.join(MANIFESTS_PATH,'*.yml')
    paths = glob.glob(lookup)
    logger.info("Finded manifests '%s'" % len(paths))
    return paths


def deploy_environment(file_path):
    logger.info("Deploy manifest '%s'" % file_path)
    manifest = DeploymentManifest(file_path=file_path)
    vbox_deployment = VirtualBoxManifestDeployment(manifest)
    vbox_deployment.run()
    logger.info("End manifest '%s' deployment" % file_path)

    # Get enviroment
    # environment_id = manifest.name
    # endpoint = '/environment/environments/{id}/'.format(
    #     id=environment_id
    # )

    # url = API_BASE_URL + endpoint
    # response = requests.get(url)
    # response.raise_for_status()

    # environment = response.json()


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
