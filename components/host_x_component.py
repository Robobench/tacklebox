import base_component
import os
import subprocess



class HostXComponent(base_component.BaseComponent):
    def __init__(self):
        self.name = "X Host Rendering Component"
        self.description = "Enable the docker client container to access X"
        self.required_commands = ['xauth', 'xdpyinfo']
        self.setup_x11_access(self.__get_xauth_fname())

    def __get_display_args(self):
        return "unix:0.0"


    def __get_xauth_fname(self):
        return "/tmp/.docker.xauth"


    def __get_xsock_fname(self):
        return "/tmp/.X11-unix"

    def setup_x11_access(self, xauthFilename):

        """ Make sure the AUTH exists -- Pythonic "touch" """
        with open(xauthFilename, 'a'):
            os.utime(xauthFilename, None)

        if not 'DISPLAY' in os.environ:
            display = self.__get_display_args()
        else:
            display=os.environ['DISPLAY']

        args="xauth nlist %s | sed -e 's/^..../ffff/' | xauth -f %s nmerge -"%(display, xauthFilename)
        p = subprocess.Popen(args , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print p.stdout.read()

    def update_arguments(self):
        return self.get_docker_argument_dict()

    def get_docker_argument_dict(self):
        """Get a dictionary of docker arguments from discovered configuration
        """
        environment_dict = self.extract_environment()
        volume_dict = self.extract_volumes()
        return {'environment':environment_dict, 'volumes':volume_dict}

    def extract_environment(self):
        """
        @brief - Get the enviroment mapping arguments.

        To forward the docker socket, the container needs environment variables that define the
        XAuthority file and the socket. The QT_GRAPHICSSYSTEM variable also needs to be set to avoid
        graphical artifacts.
        @returns env_args - The environment variables.
        """
        env_args = dict()
        env_args["DISPLAY"] = self.__get_display_args()
        env_args["XAUTHORITY"] = self.__get_xauth_fname()

        """
        QT_GRAPHICSSYSTEM is raster by default, which for some reason leads to graphics artifacts
        when forwarded through the X socket.
        """
        env_args["QT_GRAPHICSSYSTEM"] = "native"
        return env_args


    def extract_volumes(self):
        """Volume mount list
        """
        volume_dict = dict()
        volume_dict[self.__get_xauth_fname()]  = self.__get_xauth_fname() # Add volume mapping to xauth file
        volume_dict[self.__get_xsock_fname()]  = self.__get_xsock_fname() # Add volume mapping for X11 socket
        return volume_dict
