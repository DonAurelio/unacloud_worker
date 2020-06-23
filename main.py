"""
Main module
"""

__author__ = 'Aurelio Vivas'
__version__ = '1.0'

from virtualbox import VirtualBoxManager
from linux import LinuxCommandLine


if __name__ == '__main__':
    vbox = VirtualBoxManager()
    # vbox.createvm(name='vm1',ostype='Ubuntu_64',register=None)

    # vbox.modifyvm(
    #     vmname='vm1',cpus=1,memory=512,
    #     nic1='nat',natpf1='"rule1,tcp,,2224,,22"'
    # )
    # vbox.storagectl(vmname='vm1',name='sata1',add='sata')
    # vbox.storageattach(
    #     vmname='vm1',storagectl='sata1',
    #     port=0,device=0,type='hdd',
    #     medium='/home/aureavm/Desktop/prototipo/base.vdi',mtype='multiattach'
    # )

    # vbox.startvm(vmname='vm1',type='headless')
    # vbox.controlvm(vmname='vm1',action='acpipowerbutton')
    vbox.unregistervm(vmname='vm1',delete=None)
