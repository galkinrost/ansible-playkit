from __future__ import print_function
import argparse
import sys
import os
import re
import docker
import subprocess
import utils
import crypt


ENCRYPTED_TAG = '^\$ANSIBLE_VAULT'
DECRYPTED_TAG = '^#.*vault: true'
EXCLUDE_DIRECTORIES = ['.git']


def match(pattern, string):
    return re.match(pattern, string) is not None


def find_matching_files(pattern):
    current_directory = os.getcwd()
    for root, directories, filenames in os.walk(current_directory):
        directories[:] = [d for d in directories if d not in EXCLUDE_DIRECTORIES]
        for filename in filenames:
            filepath = os.path.join(root, filename)
            with open(filepath, 'r') as f:
                if match(pattern, f.readline()):
                    rel_dir = os.path.relpath(root, current_directory)
                    rel_file = os.path.join(rel_dir, filename)
                    yield rel_file
    return


def run_ansible_vault(command, files):
    cmd = docker.get_docker_container_cmd() + ['ansible-vault', command] + files
    r = subprocess.call(cmd)
    if r > 0:
        sys.exit(r)


def run_encrypt_key(args):
    parser = argparse.ArgumentParser(prog='ansible-playkit vault encryptkey', description='encrypt ssh key')
    parser.add_argument('FILE', help='path to ssh key file')
    parser.add_argument('--password', dest='password', help='key password to encrypt', required=False)
    args = parser.parse_args(args)
    if not os.path.exists(args.FILE):
        utils.error('File not found')
    crypt.encrypt_key(args.FILE, args.password)


def verify():
    for filename in find_matching_files(DECRYPTED_TAG):
        utils.error('Found decrypted file', "'" + filename + "'.", "Run 'ansible-playkit vault encrypt' before commit")
    utils.ok('All files encrypted. Ok.')
    sys.exit(0)


def run(args_list):
    parser = argparse.ArgumentParser(prog='ansible-playkit vault', description='vault')
    parser.add_argument('command', help='Command to execute (encrypt/decrypt/encryptkey/verify)')
    args = parser.parse_args(args_list[:1])

    if args.command not in ['encrypt', 'decrypt', 'encryptkey', 'verify']:
        parser.print_help()
        utils.error('Unrecognized command')

    if args.command in ['encrypt', 'decrypt']:
        docker.build_docker_image()
        files = []
        if args.command == 'encrypt':
            files = [fn for fn in find_matching_files(DECRYPTED_TAG)]
        elif args.command == 'decrypt':
            files = [fn for fn in find_matching_files(ENCRYPTED_TAG)]
        run_ansible_vault(args.command, files)
    elif args.command == 'encryptkey':
        docker.build_docker_image()
        run_encrypt_key(args_list[1:])
    elif args.command == 'verify':
        verify()
