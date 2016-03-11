from __future__ import print_function
import argparse
import utils
import os
import shutil
import getpass
import keyring


ANSIBLE_PLAYKIT_VAULT_SERVICE_NAME = 'ansible-playkit-vault'


def create_project(path):
    template_path = os.path.join(os.path.dirname(__file__), 'project_template')
    shutil.copytree(template_path, path)


def set_vault_password(project_name, password):
    keyring.set_password(ANSIBLE_PLAYKIT_VAULT_SERVICE_NAME, project_name, password)


def interactive_create_project():
    name = utils.user_input('Project name: ').strip()
    if len(name) == 0:
        utils.error('Project name is required')
    path = os.path.join(os.getcwd(), name)
    if os.path.exists(path):
        utils.error('Path already exists')
    create_project(name)
    password = getpass.getpass('Vault password: ')
    if len(password) == 0:
        utils.error('Vault password is required')
    set_vault_password(name, password)


def run(args_list):
    parser = argparse.ArgumentParser(prog='ansible-playkit project', description='project management')
    parser.add_argument('command', help='Command to execute (create)')
    args = parser.parse_args(args_list)

    if args.command == 'create':
        interactive_create_project()
    else:
        parser.print_help()
        utils.error('Unrecognized command')

