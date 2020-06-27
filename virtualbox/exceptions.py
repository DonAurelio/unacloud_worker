# -*- encoding: utf-8 -*-


class VBoxManageException(Exception):
    def __init__(self,command,text):
        message = (
            "Command '%s': "
            "%s."
        ) % (command, text)

        Exception.__init__(self,message)