

__version__ = '1.0'
__author__ = 'Aurelio Vivas'

from virtualbox import VirtualBoxManager
from linux import LinuxCommandLine


if __name__ == '__main__':
    vbox = VirtualBoxManager()
    vbox.createvm(vmname='vm1',ostype='Ubuntu_64',register='')
    vbox.modifyvm(
    	vmname='vm1',cpus=1,memory=512,
    	nic1='nat',natpf1='"rule1,tcp,,2224,,22"'
    )
    vbox.storagectl(vmname='vm1',name='sata1',add='sata')
    vbox.storageattach(
    	vmname='vm1',storagectl='sata1',
    	port=0,device=0,type='hdd',
    	medium='~/base.vdi',mtype='multiattach'
    )
