# -*- encoding: utf-8 -*-

"""
Defines how a Virtual Machines should be deployed
Given the deployemt or virtual machine specifications
"""

from virtualbox.manager import VirtualBoxManager
from virtualbox.exceptions import VBoxManageDepoymentException
from virtualbox.linux import LinuxCommandLine


import logging
import os
import time


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s')
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)


# Absolute path to the 'deployd' directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to the resources directory holding .vdi template disc.
RESOURCES_PATH = os.path.join(BASE_DIR,'resources')

# Path to the resources directory holding .vdi template disc.
PORTS_PATH = os.path.join(BASE_DIR,'ports')


class VirtualBoxManifestDeployment(object):

    def __init__(self, manifest):
        self._vbox = VirtualBoxManager()
        self._mft = manifest
        self._cmd = LinuxCommandLine()

        # Configurations
        self._ports_forder_path = PORTS_PATH
        self._port_min_number = 2221
        

        self._vm_ip_address = None
        self._vm_ssh_port = None

        # Holding exceptions
        self._deployment_exception = None
        self._action_exception = None

        self.is_deployment = False
        self.is_action = False

    def _get_reserved_ports(self):
        vms_folders = self._cmd.content_dir(self._ports_forder_path)
        reserved_ports = []
        for vm_folder in vms_folders:
            path = os.path.join(self._ports_forder_path,vm_folder)
            ports = self._cmd.content_dir(path)
            # Remove the '.txt' from the file name
            ports = [int(port[:-4]) for port in ports]
            reserved_ports += ports
        reserved_ports.sort()
        return reserved_ports

    def _get_next_available_port(self):
        reserved = self._get_reserved_ports()
        if reserved:
            return reserved[-1] + 1
        else:
            return self._port_min_number

    def _reserve_port(self):
        """Reserve a port for use in the deployment.
        The ports that are already in use are stored in 
        the ports folder.

        Ex: 2221.txt, 2222.txt 

        A new port must be the next in the sequent of used ports.
        """
        port_available = self._get_next_available_port()
        

        # Create VM folder to hold the ports
        ports_folder = os.path.join(
            self._ports_forder_path,
            self._mft.name
        )
        self._cmd.create_folder(ports_folder)

        # Create the port file assigned to the machine
        port_file_name = str(port_available) + '.txt'
        port_file_path = os.path.join(
            ports_folder,
            port_file_name
        )
        self._cmd.create_file(port_file_path)

        return port_available

        assigned_ports = os.listdir(self._ports_forder_path)
        last_port = None

    def _cleanup_reserved_ports(self):
        """
        Release the reserved ports for a given 
        Virtual machine
        """
        ports_folder = os.path.join(
            self._ports_forder_path,
            self._mft.name
        )

        self._cmd.delete_folder(ports_folder)

    def _createvm(self):
        self._vbox.createvm(
            name=self._mft.name,
            ostype='Ubuntu_64',
            register=None
        )

    def _modifyvm(self):
        ssh_rule_name = 'ssh'
        ssh_host_port = self._reserve_port()
        ssh_gest_port = 22

        natpf1 = '"%s,tcp,,%s,,%s"' % (
            ssh_rule_name,ssh_host_port,ssh_gest_port
        )

        self._vbox.modifyvm(
            vmname = self._mft.name,
            cpus = self._mft.cpus,
            memory = self._mft.memory,
            nic1 = 'nat',
            natpf1 = natpf1
        )

        self._vm_ip_address = self._cmd.get_host_ip_address()
        self._vm_ssh_port = ssh_host_port

    def _storagectl(self):
        self._vbox.storagectl(
            vmname=self._mft.name,
            name='sata1',
            add='sata'
        )

    def _storageattch(self):

        # Template disk
        medium = os.path.join(RESOURCES_PATH,'base.vdi')

        self._vbox.storageattach(
            vmname=self._mft.name,
            storagectl='sata1',
            port=0,
            device=0,
            type='hdd',
            medium=medium,
            mtype='multiattach'
        )

    def _startvm(self):
        self._vbox.startvm(vmname=self._mft.name,type='headless')

    def _deletevm(self):
        logger.info("Start '%s' virtual machine delection",self._mft.name)
        if self._vbox.vm_exists(self._mft.name):
            # If the virtual machine is running, turn it off.
            # Then delete it.
            if self._vbox.vm_is_running(self._mft.name):
                logger.info("Poweroff '%s' virtual machine",self._mft.name)
                self._vbox.controlvm(vmname=self._mft.name,action='poweroff')
                
                logger.info("Wait until '%s' virtual machine is off",self._mft.name)
                # While the virtual machine is running, wait
                # if the maximún wait time is reached
                # abort and report the error
                maximun_wait_time = 300
                while self._vbox.vm_is_running(self._mft.name) and maximun_wait_time > 0:
                    time.sleep(10)
                    maximun_wait_time = maximun_wait_time - 10

                if maximun_wait_time < 0:
                    message = 'maximum delection wait time reached'
                    raise VBoxManageDepoymentException('deletevm',message)

                logger.info("Unregister and delete '%s' virtual machine",self._mft.name)
                # When the virtul machine is off delete it.
                self._vbox.unregistervm(vmname=self._mft.name,delete=None)
                self._cleanup_reserved_ports()

            # If the virtual machine is not running just delete it.
            else:
                logger.info("Unregister and delete '%s' virtual machine",self._mft.name)
                self._vbox.unregistervm(vmname=self._mft.name,delete=None)
                self._cleanup_reserved_ports()

    def _stopvm(self):
        self._vbox.controlvm(vmname=self._mft.name,action='acpipowerbutton')
        # self._vbox.controlvm(vmname=self._mft.name,action='poweroff')

    def _resetvm(self):
        self._vbox.controlvm(vmname=self._mft.name,action='reset')

    def _vm_exists(self):
        return self._vbox.vm_exists(self._mft.name)

    def _run_deployment(self):
        self.is_deployment = True
        logger.info(
            "Running '%s' deployment with '%s' provider !!",
            self._mft.name,self._mft.provider
        )

        try:
            if not self._vm_exists():
                self._createvm()
                self._modifyvm()
                self._storagectl()
                self._storageattch()
                self._startvm()
            else:
                message = (
                    "The Virtual Machine '%s' already exists. "
                    "so not deployed again !!"
                )
                logger.info(message,self._mft.name)

        except Exception as e:
            logger.error(
                "Deployment '%s' with '%s' provider failed !!",
                self._mft.name,self._mft.provider
            )

            logger.exception(e)
            self._deployment_exception = e

            # If an error occurs during deployment and the machines 
            # was create we delete the machie as the whole deployment 
            # must be atomic
            logger.info(
                "Start cleanup deployment !!"
            )
            self._deletevm()
        
    def _run_action(self):
        self.is_action = True
        try:
            if 'start' in self._mft.action:
                self._startvm()
            elif 'stop' in self._mft.action:
                self._stopvm()
            elif 'reset'in self._mft.action:
                self._resetvm()
            elif 'delete'in self._mft.action:
                self._deletevm()
            else:
                message = (
                    "Unkown action received '%s', "
                    "available actions start|stop|reset." 
                ) % self._mft.action
                raise Exception(message)
        except Exception as e:
            logger.error(
                "Action '%s' on machine '%s' with '%s' provider failed !!",
                self._mft.action,self._mft.name,self._mft.provider
            )

            logger.exception(e)
            self._action_exception = e

    def _dispatch(self):
        if self._mft.is_resource_deployment:
            self._run_deployment()
        elif self._mft.is_action_deployment:
            self._run_action()
        else:
            message = "No 'action' or 'specs' on deployment manifest"
            raise Exception(message)

    def run(self):
        self._dispatch()

    def delete(self):
        """Delete virtual machine"""
        self._deletevm()

    def is_success(self):
        """If no execption take place the deployment was succesfull."""
        return self._deployment_exception is None

    def is_action_success(self):
        return self._action_exception is None

    def get_deployment_message(self):
        return str(self._deployment_exception)

    def get_action_message(self):
        return str(self._action_exception)

    def get_deployment_data(self):
        """Return staticts of the deplayment and also virtual machine data."""
        vm = {
            'name': self._mft.name,
            'address': self._vm_ip_address,
            'ssh_port': self._vm_ssh_port
        }
        statistics = None
        return vm, statistics
