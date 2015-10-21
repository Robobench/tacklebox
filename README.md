This project attempts to provide a toolkit for bringing your hardware with you into a Docker container. This is done by linking the appropriate libraries from the host machine into the container and automatically finding the correct device flags.

This is primarily tested on Ubuntu (12.04, 14.04), but should work on other Linux distributions. Whether it will work on another platform in a virtual machine is completely untested.

The primary mechanism for doing this is using strace on an examplar utility on the host and deriving the appropriate flags directly from there.

First, install Docker following here: https://docs.docker.com/installation/

Then install the dependencies of this package:
  	
	sudo pip install -r requirements.txt
	sudo apt-get install mesa-utils
	
Then install into your workspace - use a virtualenv, or run as root:
        
        python setup.py install

Try it by doing the following:

	tackle component-demo

This test case demonstrates that the container is correctly configured to access the hosts' gl capabilities using the vanilla ubuntu:trusty image, without installing X or the GL driver explicitly in the container!

###TODOs

  Refactor ``argument_dict`` in ``def __get_arguments_from_dict(self, argument_dict):`` as python module for reuseability


