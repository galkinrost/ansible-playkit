from __future__ import print_function
import argparse
import utils
import sys
import os
import shutil


def user_input(question):
     if (sys.version_info > (3, 0)):
         return input(question)
     else:
         return raw_input(question)


def create_project(path):
    template_path = os.path.join(os.path.dirname(__file__), 'project_template')
    shutil.copytree(template_path, path)


def interactive_create_project():
    name = user_input('Project name: ').strip()
    if len(name) == 0:
        utils.error('Project name is required')
    path = os.path.join(os.getcwd(), name)
    if os.path.exists(path):
        utils.error('Path already exists')
    create_project(name)


def run(args_list):
    parser = argparse.ArgumentParser(prog='ansible-playkit project', description='project management')
    parser.add_argument('command', help='Command to execute (create)')
    args = parser.parse_args(args_list)

    if args.command == 'create':
        interactive_create_project()
    else:
        parser.print_help()
        utils.error('Unrecognized command')

