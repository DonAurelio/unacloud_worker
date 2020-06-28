#!/bin/python3
# -*- encoding: utf-8 -*-

"""
Main module
"""

__author__ = 'Aurelio Vivas'
__version__ = '1.0'


# from virtualbox.manager import VirtualBoxManager
# from virtualbox.deployment import VirtualBoxManifestDeployment
# from metadata import DeploymentManifest
# from deployd import Deployd

import requests
import datetime


if __name__ == '__main__':
    
    # VIRTUAL MACHINE CREATION AND DELECTION
    # vbox = VirtualBoxManager()
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
    # vbox.unregistervm(vmname='vm1',delete=None)

    # VIRTUAL MACHINE METADATA
    # manifest = DeploymentManifest(file_path='./manifests/vm1.yml')
    # vbox_deployment = VirtualBoxManifestDeployment(manifest)
    # vbox_deployment.run()

    # DEPLOYD
    # deployd = Deployd(manifests_folder='./manifests')
    # deployd.run()

    data = {
        # 'id':1,
        'worker':"http://localhost:8081/api/worker/workers/1/",
    }
    # 'https://httpbin.org/post'
    r = requests.patch('http://localhost:8081/api/environment/environments/1/', data = data)
    print(r.status_code)
    print(r.content)

    # r = requests.get('http://localhost:8000/executionenvironments/?status=Pending')
    # print(r.status_code)
    # data = r.json()
    # print(data)
    # sorted_nodes = sorted(data, key=lambda k: k['available_cpus']) 
    # print(sorted_nodes)
    # r = requests.get('http://localhost:8000/workernodes/')
    # print(r.status_code)
    # print(type(r.json()))
    # print(r.status_code)
    # data = r.json()
    # print(data)
    # sorted_nodes = sorted(data, key=lambda k: k['available_cpus'], reverse=True) 
    # print(sorted_nodes)