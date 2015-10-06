from __future__ import print_function
import subprocess
import logging
import shlex

class DockerRunPopen(object):
    def __init__(self, image_name="ubuntu:trusty", rm=True,
                 interactive=False, dockerargs=[]):
        """A wrapper for popen that runs the command in a docker image

        :param image_name: The name of the image to run
        :type str
        :param rm: Whether to rm the resulting container after running it.
        :type bool
        :param dockerargs
        :type (str,)
        """
        self.image_name = image_name
        self.dockerargs = dockerargs
        self.rm = rm
        self.interactive = interactive

    def __call__(self, command_args, **kwargs):
        """Call the popen

        :param command_args: The args to pass to /bin/bash
        :type (str,)
        :param kwargs: The keyword args to pass to the Popen function
        :type {string,string}
        """
        args =  ["docker", "run"] + self.generate_docker_args(command_args)
        return subprocess.Popen(args=args, **kwargs)

    def generate_docker_args(self, command_args):


        """Return docker specific arguments to be passed into "docker run"

        :param command_args: The args to pass to /bin/bash
        :type (str,)
        :type {string}
        """
        # command_list = ["docker run"]
        command_list = []
        if self.interactive:
            command_list.extend(["-ti"])
        command_list.append('--rm={}'.format(self.rm).lower())
        command_list.extend(self.dockerargs)
        command_list.append(self.image_name)
        command_list.append('"{}"'.format(command_args))
        logging.warn(' '.join(command_list))
        docker_args=shlex.split(' '.join(command_list))
        return docker_args
        #return subprocess.Popen(args=' '.join(command_list))
    