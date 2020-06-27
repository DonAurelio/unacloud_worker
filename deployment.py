# -*- encoding: utf-8 -*-

import logging

from virtualbox import VirtualBoxManager

logging.basicConfig(
    format='%(levelname)s : %(asctime)s : %(message)s',
    level=logging.DEBUG
)


class VirtualBoxManifestDeployment(object):

    def __init__(self, obj_manifest):
        self._manifest = obj_manifest

    def run(self):
        if self._manifest.is_resource_deployment:
            self.run_deployment()
        elif self._manifest.is_action_deployment:
            self.run_action()
        else:
            raise Exception('No action or resource deployment')

    def run_action(self):
        vbox.controlvm(vmname=self._manifest.name,action='acpipowerbutton')

    def run_deployment(self):
        logging.info(
            "Running '%s' deployment with '%s' provider !!",
            self._manifest.name,self._manifest.provider
        )

        vbox = VirtualBoxManager()
        try:
            vbox.createvm(
                name=self._manifest.name,
                ostype='Ubuntu_64',
                register=None
            )

            vbox.modifyvm(
                vmname = self._manifest.name,
                cpus = self._manifest.cpus,
                memory = self._manifest.memory,
                nic1 = 'nat',
                natpf1 = '"rule1,tcp,,2224,,22"'
            )

            vbox.storagectl(
                vmname=self._manifest.name,
                name='sata1',
                add='sata'
            )

            vbox.storageattach(
                vmname=self._manifest.name,
                storagectl='sata1',
                port=0,
                device=0,
                type='hdd',
                medium='/home/aureavm/Desktop/prototipo/base.vdi',
                mtype='multiattach'
            )

            vbox.startvm(vmname=self._manifest.name,type='headless')
        except Exception as e:
            logging.error(
                "Failed '%s' deployment with '%s' provider: %s",
                self._manifest.name,self._manifest.provider, str(e)
            )
            # Report error and clean the enviornment
            vbox.unregistervm(vmname=self._manifest.name,delete=None)
        