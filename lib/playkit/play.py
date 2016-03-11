from __future__ import print_function
import argparse
import os
import sys
import fnmatch
import utils
import vault

from ansible.cli.playbook import PlaybookCLI
from ansible.cli.galaxy import GalaxyCLI

INVENTORIES_PATH='inventories'
KEYS_PATH = 'keys'


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


def __run_playbook(inventory_path, playbook_path, key_path, tags, ansibleopts):
    cmd = ['ansible-playbook', '-i', inventory_path, '--private-key', key_path,
           '--vault-password-file={}'.format(vault.VAULT_PASSWORD_FILENAME), playbook_path]
    if len(tags) > 0:
        cmd += ['--tags', ','.join(tags)]
    if ansibleopts is not None:
        cmd += ansibleopts.strip().split()
    cli = PlaybookCLI(cmd)
    cli.parse()
    sys.exit(cli.run())


def run_playbook(inventory_path, playbook_path, key_path, tags, ansibleopts):
    if os.path.exists(playbook_path):
        utils.ok('Running playbook', playbook_path)
        __run_playbook(inventory_path, playbook_path, key_path, tags, ansibleopts)
    else:
        utils.error('Playbook not found', os.path.basename(playbook_path))


def install_ansible_requirements():
    cmd = ['ansible-galaxy', 'install', '-r', 'ansible-requirements.yml']
    cli = GalaxyCLI(cmd)
    cli.parse()
    sys.exit(cli.run())


def run(args):
    parser = argparse.ArgumentParser(prog='ansible-playkit play', description='deploy')
    parser.add_argument('inventory', help='inventory name')
    parser.add_argument('playbook', help='playbook name')
    parser.add_argument('tags', nargs='*', help='Playbook tags which should be used')
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
        install_ansible_requirements()
        vault.run_ansible_vault('decrypt', [key_path])
        run_playbook(inventory_path,
                     playbook_filename,
                     key_path,
                     args.tags,
                     args.ansible_opts)
    finally:
        vault.run_ansible_vault('encrypt', [key_path])


