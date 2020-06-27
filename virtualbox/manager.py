# -*- encoding: utf-8 -*-


from linux import LinuxCommandLine
from exceptions import VBoxManageException

import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s')
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)


class VirtualBoxManager(object):


    @staticmethod
    def _parse_error_message(message):
        """Parse VBoxManage Error Messages.

        An error in VBoxManage is reported with the following format.
        We separet the usefull information and the detailed information.
        VBoxManage: error: Cannot unregister the machine 'vm1' while it is locked
        VBoxManage: error: Details: code VBOX_E_INVALID_OBJECT_STATE (0x80bb0007)...
        VBoxManage: error: Context: "Unregister(CleanupMode_DetachAllReturnHardDisksOnly... 

        Args:
            message (str): the stdout of the VBoxManage command.

        Returns:
            The usefull information of the message.
        """
        message_lines = message.splitlines()

        # we extract only the usefull information form the message which is
        # 'Cannot unregister the machine 'vm1' while it is locked'
        message_summary = message_lines[0].split(':')[2]

        return message_summary


    @staticmethod
    def _build_command(*args,**kwargs):
        command_str = "VBoxManage"

        for arg in args:
            command_str += " {arg}".format(arg=arg)

        for key, value in kwargs.items():
            if value is None:
                command_str += " --{key}".format(key=key)
            else:
                command_str += " --{key} {value}".format(key=key,value=value)
                
        return command_str

    @staticmethod
    def _send_command(command_str):
        cmd = LinuxCommandLine()
        rcode, stdout, stderr = cmd.execute(command_str)

        if rcode == 0:
            logger.info("Command '%s' successfully executed !!", command_str)
        else:
            logger.error("Command '%s' failed !!", command_str)

            message_summary = VirtualBoxManager._parse_error_message(stderr)
            raise VBoxManageException(command_str,message_summary)

        return rcode, stdout, stderr


    def createvm(self,name,**kwargs):
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

        command_str = self._build_command('createvm',name=name,**kwargs)
        rcode, stdout, stderr = self._send_command(command_str)

    def modifyvm(self,vmname,**kwargs):
        """
        Changes the properties of a registered virtial machine.

        Args:
            vmname (str): the name of the virtual machine.
            kwargs (dict): --name, --memory, --cpus, --nic1.
                use 'VBoxManage modifyvm' command to get a 
                full list of args supported. 
        """
        command_str = self._build_command('modifyvm',vmname,**kwargs)
        rcode, stdout, stderr = self._send_command(command_str)

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

        command_str = self._build_command('storagectl',vmname,**kwargs)
        rcode, stdout, stderr = self._send_command(command_str)

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

        command_str = self._build_command('storageattach',vmname,**kwargs)
        rcode, stdout, stderr = self._send_command(command_str)

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

        Args:
            vmname (str): the name of the virtual machine.
        """
        command_str = self._build_command('unregistervm',vmname,**kwargs)
        rcode, stdout, stderr = self._send_command(command_str)

    def startvm(self,vmname,**kwargs):
        """
        This command starts a virtual machine that is currently in the Powered Off
        or Saved states.

        Args:
            vmname (str): the name of the virtual machine.
            type (str): gui|headless|separate
        """

        command_str = self._build_command('startvm',vmname,**kwargs)
        rcode, stdout, stderr = self._send_command(command_str)


    def controlvm(self,vmname,action):
        """
        The controlvm subcommand enables you to change the state of a 
        virtual machine that is currently running.
        """
        command_str = self._build_command('controlvm',vmname,action)
        rcode, stdout, stderr = self._send_command(command_str)

    def list_vms(self):
        """
        The controlvm subcommand enables you to change the state of a 
        virtual machine that is currently running.
        """
        command_str = self._build_command('list','vms')
        rcode, stdout, stderr = self._send_command(command_str)

        # Parse the output of 'VBoxManage list vms' command 
        # and return the names of the registered vms
        output = stdout.replace('"','')
        output_lines = output.splitlines()
        vms = [line.split(' ')[0] for line in output_lines]

        return vms
