# -*- encoding: utf-8 -*-

import subprocess 


class LinuxCommandLine(object):
    """
    This class is used to exceute command in 
    the Linux Command Line.
    """

    def execute(self,command_str):
        """
        Execute the given command in a child program (a new process).

        Args:
            command_str (str): the command to be executed.
                The format if this string must be 
                "command1 arg1 arg2 ... argN".
        """

        stdout = None
        stderr = None
        return_code = None

        command_list = command_str.split(' ')
        # command_list.remove('')
        print(command_list)

        try:
            # Popen use the format ["command1", "arg1", "arg2"]
            # we can not use pipes in the command, example:
            # cat file.txt | less
            # subprocess.PIPE indicates that a PIPE must be open 
            # so we can be able to read stdin and stdout
            process = subprocess.Popen(
                command_list,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )

            # When you run .communicate(), it will wait until 
            # the process is complete.
            stdout, stderr = process.communicate()

            # Get the return code, 0 core is success execution
            # otherwise and error has occurred. 
            return_code = process.poll()

        except OSError as e:
            # When the command is not well writed subprocess
            # will raise an exception.
            return_code = None
            stdout = None 
            stderr = str(e)
        except Exception as e:
            return_code = None
            stdout = None 
            stderr = str(e)
        finally:
            return return_code, stdout, stderr
