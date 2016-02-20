import subprocess
import os
import docker
import utils


def decrypt_key(key_path, password=None):
    out_filename = key_path.rstrip('.encrypted')
    cmd = docker.get_docker_container_cmd() + ['openssl', 'aes-256-cbc', '-salt', '-a', '-d', '-in', key_path, '-out', out_filename]
    if password is not None:
        cmd += ['-k', password]
    r = subprocess.call(cmd)
    if r == 0:
        os.chmod(out_filename, 0600)
        utils.ok('Decrypted', key_path, 'to', out_filename)
        return out_filename
    else:
        utils.error('Fail decrypt key', key_path, 'to', out_filename)


def encrypt_key(key_path, password):
    out_filename = key_path
    if not key_path.endswith('.pem'):
        out_filename += '.pem'
    out_filename += '.encrypted'
    cmd = docker.get_docker_container_cmd() + ['openssl', 'aes-256-cbc', '-salt', '-a', '-in', key_path, '-out', out_filename]
    if password is not None:
        cmd += ['-k', password]
    r = subprocess.call(cmd)
    if r == 0:
        os.chmod(out_filename, 0600)
        utils.ok('Encrypted', key_path, 'to', out_filename)
        return out_filename
    else:
        utils.error('Fail encrypt key', key_path, 'to', out_filename)