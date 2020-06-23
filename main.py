

__version__ = '1.0'
__author__ = 'Aurelio Vivas'

from virtualbox import VirtualBoxManager


if __name__ == '__main__':
    vbox = VirtualBoxManager()
    vbox.createvm(name='vm1',ostype='Ubuntu_64',register='')
    vbox.modifyvm(name='vm1',cpus=1,memory=512,nic1='nat',natpf1='"rule1,tcp,,2224,,22"')
