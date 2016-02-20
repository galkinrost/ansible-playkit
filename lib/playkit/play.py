from __future__ import print_function
import subprocess
import argparse
import os
import sys
import fnmatch
import docker
import crypt
import utils

INVENTORIES_PATH='inventories'
KEYS_PATH = 'keys'
VAULT_PASS_FILENAME = '.vault_password'


def clean_keys():
    keys = find_all('*.pem', KEYS_PATH)
    for key in keys:
        os.remove(key)


def clean_vault_pass():
    vault_pass = find_first(VAULT_PASS_FILENAME, os.getcwd())
    if vault_pass is not None:
        os.remove(vault_pass)


def clean():
    clean_keys()
    clean_vault_pass()


def find_first(pattern, path):
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                return os.path.join(root, name)
    return None


def find_all(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def __run_playbook(docker_cmd, inventory_path, playbook_path, vault_password, key_path, tags, ansibleopts):
    cmd = docker_cmd + ['ansible-playbook', '-i', inventory_path, '--private-key', key_path]
    if vault_password is not None:
        with open(VAULT_PASS_FILENAME, 'w') as f:
            f.write(vault_password)
        cmd += ['--vault-password-file', VAULT_PASS_FILENAME]
    else:
        cmd += ['--ask-vault-pass']
    cmd += [playbook_path]
    if len(tags) > 0:
        cmd += ['--tags', ','.join(tags)]
    if ansibleopts is not None:
        cmd += ansibleopts.strip().split()
    r = subprocess.call(cmd)
    if r > 0:
        sys.exit(r)


def run_playbook(docker_cmd, inventory_path, playbook_path, vault_password, key_path, tags, ansibleopts):
    if os.path.exists(playbook_path):
        utils.ok('Running playbook', playbook_path)
        __run_playbook(docker_cmd, inventory_path, playbook_path, vault_password, key_path, tags, ansibleopts)
    else:
        utils.error('Playbook not found', os.path.basename(playbook_path))


def install_ansible_requirements(docker_cmd):
    cmd = docker_cmd + ['ansible-galaxy', 'install', '-r', 'ansible-requirements.yml']
    r = subprocess.call(cmd)
    if r > 0:
        sys.exit(r)


def run(args):
    parser = argparse.ArgumentParser(prog='ansible-playkit play', description='deploy')
    parser.add_argument('inventory', help='inventory name')
    parser.add_argument('playbook', help='playbook name')
    parser.add_argument('tags', nargs='*', help='Playbook tags which should be used')
    parser.add_argument('--ssh_key_password', dest='ssh_key_password', required=False, help='SSH key password')
    parser.add_argument('--vault_password', dest='vault_password', required=False, help='Ansible Vault password')
    parser.add_argument('--ansible_opts', dest='ansible_opts', required=False, help='Additional Ansible Playbook options')
    args = parser.parse_args(args)

    inventory_path = os.path.join(INVENTORIES_PATH, args.inventory)
    if os.path.exists(inventory_path):
        utils.ok('Using inventory', inventory_path)
    else:
        utils.error('Inventory not found', inventory_path)

    key_path = os.path.join(KEYS_PATH, '{}.pem.encrypted'.format(args.inventory))
    if os.path.exists(key_path):
        utils.ok('Using encrypted key', key_path)
    else:
        utils.error('Encrypted key not found', key_path)

    playbook_filename = args.playbook + '.yml'
    try:
        docker.build_docker_image()
        docker_cmd = docker.get_docker_container_cmd()
        install_ansible_requirements(docker_cmd)
        ssh_key = crypt.decrypt_key(key_path, args.ssh_key_password)
        run_playbook(docker_cmd,
                     inventory_path,
                     playbook_filename,
                     args.vault_password,
                     ssh_key,
                     args.tags,
                     args.ansible_opts)
    finally:
        clean()

