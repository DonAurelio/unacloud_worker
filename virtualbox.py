# -*- encoding: utf-8 -*-


class VirtualBoxManager(object):

    def createvm(self,vmname,ostype,**kwargs):
        """
        Creates a new virtual machine XML definition file.
        
        Args:
            vmname (str): the name of the virtual machine.
            ostype (str): valid os types are Ubuntu_64
                and others, use 'VBoxManage list ostypes'
                command to get a full list of available
                os types.
            register (bool): registers a XML virtual machine 
                definition file into Oracle VM VirtualBox.
        """

        command_format = "VBoxManage createvm {vmname} {ostype}".format(
            vmname=vmname, ostype=ostype
        )

        for key, value in kwargs.items():
            command_format += " --{key} {value}".format(key=key,value=value)

        print(command_format)


    def modifyvm(self,vmname,**kwargs):
        """
        Changes the properties of a registered virtial machine.

        Args:
            vmname (str): the name of the virtual machine.
            kwargs (dict): --name, --memory, --cpus, --nic1.
                use 'VBoxManage modifyvm' command to get a 
                full list of args supported. 
        """
        command_format = "VBoxManage modifyvm {vmname}".format(vmname=vmname)
        for key, value in kwargs.items():
            command_format += " --{key} {value}".format(key=key,value=value)

        print(command_format)

    def storagectl(self,vmname,**kwargs):
        """
        Attaches, modifies and removes a storage controller.
        After this, virtual media can be attached to the controller 
        with the 'storageattach' command. Use 'VBoxManage storagectl' 
        command to get a full list of args supported.

        Args:
            name (str): the name of the virtual machine.
            add (str): ide|sata|scsi|floppy|sas|usb|pcie.
        """

        command_format = "VBoxManage storagectl {vmname}".format(vmname=vmname)
        for key, value in kwargs.items():
            command_format += " --{key} {value}".format(key=key,value=value)

        print(command_format)

    def storageattach(self,vmname,**kwargs):
        """
        Attaches, modifies and removes a storage medium connacted to
        a storage controller that was previously added with 
        the 'storagectl' command. Use 'VBoxManage storageattach' 
        command to get a full list of args supported.

        Args:
            vmname (str): the name of the virtual machine.
            storagectl (str): the name of the storage controller
                added previously with 'storagectl'.
            port (str): port number.
            device (str): device number.
            type (str): dvddrive|hdd|fdd.
            medium (str): none|filename.
            mtype (str): normal|writethrough|immutable
                |shareable|readonly|multiattach.

        """

        command_format = "VBoxManage storageattach {vmname}".format(vmname=vmname)
        for key, value in kwargs.items():
            command_format += " --{key} {value}".format(key=key,value=value)

        print(command_format)

    def unregistervm(self,vmname,**kwargs):
        """
        The unregistervm command unregisters a virtual machine.
        If --delete is also specified the following fils will be
        also be deleted autimatically.

            * All hard disk image files, including differencing files, 
            which are used by the machine and not shared with other 
            machines.

            * Saved state files that the machine created. One if the 
            machine was in Saved state and one for each online snapshot.

            * The machine XML file and its backups.

            * The machine log files.

            * The machine directory, if it is empty after having deleted 
            all of the above files.
        """

        command_format = "VBoxManage unregistervm {vmname}".format(vmname=vmname)
        for key, value in kwargs.items():
            command_format += " --{key} {value}".format(key=key,value=value)

        print(command_format)