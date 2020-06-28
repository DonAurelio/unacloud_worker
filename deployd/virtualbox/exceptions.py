# -*- encoding: utf-8 -*-


class VBoxManageCommandException(Exception):
    def __init__(self,command,text):
        message = (
            "Command '%s': "
            "%s."
        ) % (command, text)

        Exception.__init__(self,message)

class VBoxManageDepoymentException(Exception):
    def __init__(self,command,text):
        message = (
            "Action '%s': "
            "%s."
        ) % (command, text)

        Exception.__init__(self,message)