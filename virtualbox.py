class VirtualBoxManager(object):

    def createvm(self,name,ostype,**kwargs):
        """
        Creates a new virtual machine XML definition file.
        
        Args:
            name (str): the name of the virtual machine.
            ostype (str): valid os types are Ubuntu_64
                and others, use 'VBoxManage list ostypes'
                command to get a full list of available
                os types.
            register (bool): registers a XML virtual machine 
                definition file into Oracle VM VirtualBox.
        """

        command_format = "VBoxManage createvm {name} {ostype}".format(
            name=name, ostype=ostype
        )

        for key, value in kwargs.items():
            command_format += " --{key} {value}".format(key=key,value=value)

        print(command_format)


    def modifyvm(self,name,**kwargs):
        """
        Changes the properties of a registered virtial machine.

        Args:
            name (str): the name of the virtual machine.
            kwargs (dict): --name, --memory, --cpus, --nic1.
                use 'VBoxManage modifyvm' command to get a 
                full list of args supported. 
        """
        command_format = "VBoxManage modifyvm {name}".format(name=name)
        for key, value in kwargs.items():
            command_format += " --{key} {value}".format(key=key,value=value)

        print(command_format)

    def storagectl(self,name,**kwargs):
        """
        Attaches, modifies and removes a storage controller.
        After this, virtual media can be attached to the controller 
        with the 'storageattach' command. use 'VBoxManage storagectl' 
        command to get a full list of args supported.

        Args:
            name (str): the name of the virtual machine.
            add (str): ide|sata|scsi|floppy|sas|usb|pcie.
        """

        command_format = "VBoxManage storagectl {name}".format(name=name)
        for key, value in kwargs.items():
            command_format += " --{key} {value}".format(key=key,value=value)

        print(command_format)