from __future__ import print_function
import subprocess
import logging

class BaseComponent(object):
    def __init__(self):
        self.devices = []
        self.libraries = []
        self.environment = []
        self.misc = []
        self.name = "Base Component"
        self.description = "Base class for specifying components"
        self.required_commands = []
        self.library_rejection_filter=[]
        self.device_rejection_filter=[]

    def introspect_host(self):
        """Introspect the host to find the parameters necessary for the components


        """
        return []

    def update_arguments(self):
        """Update the produced arguments
        """
        return []

    def extract_libraries(self, opened_objects):
        """ Given a list of opened objects, extract a list of only the relevant libraries.

        :param opened_objects - The objects opened when the test is run according to strace.
        :type opened_objects - [str,]
        """
        libraries = [lib for lib in opened_objects if '.so' in lib and not
                     any([reject in lib for reject in self.library_rejection_filter])]
        return libraries

    def extract_devices(self, opened_objects):
        """ Given a list of opened objects, extract a list of only the relevant devices

        :param opened_objects - The objects opened when the test is run according to strace.
        :type opened_objects - [str,]
        """
        devices = [dev for dev in opened_objects if dev.startswith('/dev') and not
                     any([reject in lib for reject in self.device_rejection_filter])]
        return devices

    def extract_environment(self, opened_objects):
        """ Given a list of opened objects, extract a list of relevant environment variables.
        """
        pass


    def test_required_commands(self, process_maker=subprocess.Popen):
        """Get a list of the required host commands to test before actually looking
        for the information.
        """
        passed = True
        for cmd in self.required_commands:
            if not self._has_command(process_maker, command=cmd):
                logging.error("Command {} could not be found.".format(cmd) +
                "Please basic platform requirements.")
                passed = False
        return passed


    def test_component(self, process_maker=subprocess.Popen):
        """ Test basic component compatibility with host.

        """
        return False


    def _has_command(self, process_maker, command):
        p = process_maker('which {}'.format(command), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        return not p.wait()


