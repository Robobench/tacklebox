from __future__ import print_function
import subprocess

import logging
import base_component
import os

class RenderingComponent(base_component.BaseComponent):
    def __init__(self):
        super(RenderingComponent, self).__init__()
        self.name = "GL Rendering Component"
        self.description = " Enable the client container to access OpenGL"
        self.required_commands = ["glxinfo", "strace", "cut", "glxgears"]
        self.library_rejection_filter=["libm","libdl", "ld","libc"]
        self.device_rejection_filter=["shm"]
        self.container_lib_path = "/external_libs"


    def update_arguments(self):
        """Update the produced arguments
        """
        opened_objects = self.introspect_host()
        self.libraries = self.extract_libraries(opened_objects)
        self.devices = self.extract_devices(opened_objects)
        return self.get_docker_argument_dict()

    def get_docker_argument_dict(self):
        """Get a dictionary of docker arguments from discovered configuration
        """
        volume_dict = {}
        device_dict = {}
        env_dict = {'LD_LIBRARY_PATH':'/external_libs'}
        for library in self.libraries:
            libname = os.path.split(library)[1]
            container_lib = os.path.join("/external_libs",libname)
            if container_lib in volume_dict.values():
                pass
            volume_dict[library]=container_lib
        for device in self.devices:
            device_dict[device] = device

        volume_dict.update(self.extract_required_commands())

        return {'volumes': volume_dict, 'devices': device_dict, 'environment': env_dict}


    def introspect_host(self):
        """Introspect the host to find the parameters necessary for the components
        """
        p = subprocess.Popen("strace glxinfo 2>&1| grep open | cut -d '\"'  -f 2 | sort | uniq -c | awk '{print $2}\n'", shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        (stdout, stderr) = p.communicate()

        opened_objects = stdout.split()

        #FIXME - some of the time, there is no link found between libXX.XX.so.# to libXX.XX.so.
        #FIXME - We may need a way to make sure that there is always such a symlink.

        return opened_objects

    def test_component(self, process_maker=subprocess.Popen):
        """ Test basic component compatibility with host.

        For GL, test the direct rendering.
        """
        return self.__test_direct_rendering(process_maker)


    def __test_direct_rendering(self, process_maker=subprocess.Popen):
        p = process_maker("glxinfo", shell=False, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        (stdout, stderr) = p.communicate()
        direct_rendering = "direct rendering: Yes" in stdout
        if not direct_rendering:
            logging.error("Direct rendering not enabled on host! Cannot enable on client. Examine host configuration.")
            return False
        return True

    def demo_component(self, process_maker=subprocess.Popen):
        self.__demo_glxgears(process_maker)

    def __demo_glxgears(self, process_maker):
        logging.warn("Starting GLX gears to test rendering component. Close windows to continue.\n ***CTRL-C WILL NOT EXIT!*** \n [Note that errors of the form 'XIO:  fatal IO error 11 (Resource temporarily unavailable)' are expected]")
        p = process_maker("glxgears", shell=False, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        (stdout, stderr) = p.communicate()
        print(stdout)
        print(stderr)
        return
