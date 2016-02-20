import subprocess
import os
import utils


DOCKER_IMAGE_TAG='playkit/ansible'


def build_docker_image():
    cmd = ['docker', 'build', '-q', '--force-rm', '-t', DOCKER_IMAGE_TAG, os.path.dirname(__file__)]
    utils.ok("Building docker image with tag", "'" + DOCKER_IMAGE_TAG + "'")
    r = subprocess.call(cmd)
    if r > 0:
        utils.error('Error building docker image')


def get_docker_container_cmd():
    return ['docker', 'run', '-it', '--rm', '-v', os.getcwd() + ':/opt', DOCKER_IMAGE_TAG]