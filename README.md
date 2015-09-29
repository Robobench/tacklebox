This project attempts to provide a toolkit for bringing your hardware with you into a Docker container. This is done by linking the appropriate libraries from the host machine into the container and automatically finding the correct device flags.

The primary mechanism for doing this is using strace on an examplar utility on the host and deriving the appropriate flags directly from there.

First, install Dependencies:
  
  sudo pip install -r requirements.txt

Try it by doing the following:

  python tackle.py component-demo

This test case demonstrates that the container is correctly configured to access the hosts' gl capabilities using the vanilla ubuntu:trusty image, without installing X or the GL driver explicitly in the container!

