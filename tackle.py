import sys

from components import rendering_component
from components import host_x_component
from components import docker_subprocess
reload(rendering_component)
reload(host_x_component)
reload(docker_subprocess)



def get_arguments_from_dict(argument_dict):
    argument_strings =[]
    for key,value in argument_dict.get('volumes',{}).iteritems():
        argument_strings.append('--volume={}:{}'.format(key, value))
    for key,value in argument_dict.get('devices',{}).iteritems():
        argument_strings.append('--device={}:{}'.format(key, value))
    for key,value in argument_dict.get('environment',{}).iteritems():
        argument_strings.append('--env={}={}'.format(key, value))
    return argument_strings


if __name__=="__main__":
    r = rendering_component.RenderingComponent()
    x = host_x_component.HostXComponent()
    argument_strings = get_arguments_from_dict(r.update_arguments())
    argument_strings.extend(get_arguments_from_dict(x.update_arguments()))

    if len(sys.argv) > 1:
        image_name = sys.argv[1]
    else:
        image_name = "ubuntu:trusty"
    docker_runner = docker_subprocess.DockerRunPopen(image_name, interactive=True, dockerargs=argument_strings)
    process = docker_runner('/bin/bash')
    (stdout,stderr) = process.communicate()
