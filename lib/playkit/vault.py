from __future__ import print_function
import argparse
import sys
import os
import re
import utils

from ansible.cli.vault import VaultCLI


ENCRYPTED_TAG = '^\$ANSIBLE_VAULT'
DECRYPTED_TAG = '^#.*vault: true'
EXCLUDE_DIRECTORIES = ['.git']
VAULT_PASSWORD_FILENAME = 'vault_password'


def match(pattern, string):
    return re.match(pattern, string) is not None


def file_matches(filepath, pattern):
    with open(filepath, 'r') as f:
        return match(pattern, f.readline())


def find_matching_files(pattern, directory=os.getcwd()):
    for root, directories, filenames in os.walk(directory):
        directories[:] = [d for d in directories if d not in EXCLUDE_DIRECTORIES]
        for filename in filenames:
            filepath = os.path.join(root, filename)
            if pattern is None:
                rel_dir = os.path.relpath(root, directory)
                rel_file = os.path   .join(rel_dir, filename)
                yield rel_file
            elif file_matches(filepath, pattern):
                rel_dir = os.path.relpath(root, directory)
                rel_file = os.path.join(rel_dir, filename)
                yield rel_file
    return


def run_ansible_vault(command, files):
    args = ['ansible-vault', command, '--vault-password-file={}'.format(VAULT_PASSWORD_FILENAME,)] + files
    cli = VaultCLI(args)
    cli.parse()
    return cli.run()


def get_keys_dir():
    return os.path.join(os.getcwd(), 'keys')


def get_keys(pattern):
    keys_dir = get_keys_dir()
    pattern_keys = set([filename for filename in
                          find_matching_files(pattern, directory=keys_dir) if filename.endswith('.pem')])
    all_keys = set([filename for filename in
                          find_matching_files(None, directory=keys_dir) if filename.endswith('.pem')])
    return [os.path.join(keys_dir, f) for f in all_keys.difference(pattern_keys)]


def get_unencrypted_keys():
    return get_keys(ENCRYPTED_TAG)


def verify():
    # verify that all ansible files are encrypted
    for filename in find_matching_files(DECRYPTED_TAG):
        utils.error('Found decrypted file', "'" + filename + "'.", "Run 'ansible-playkit vault encrypt' before commit")
    # verify that all keys are encrypted
    unencrypted_keys = [os.path.basename(f) for f in get_unencrypted_keys()]
    if len(unencrypted_keys) > 0:
        utils.error("Found unencrypted keys: ", ', '.join(unencrypted_keys))

    utils.ok('All files encrypted. Ok.')
    sys.exit(0)


def run(args_list):
    parser = argparse.ArgumentParser(prog='ansible-playkit vault', description='vault')
    parser.add_argument('command', help='Command to execute (encrypt/decrypt/verify)')
    args = parser.parse_args(args_list[:1])

    if args.command not in ['encrypt', 'decrypt', 'encryptkey', 'verify']:
        parser.print_help()
        utils.error('Unrecognized command')

    if args.command in ['encrypt', 'decrypt']:
        files = []
        if args.command == 'encrypt':
            files = [fn for fn in find_matching_files(DECRYPTED_TAG)] + get_unencrypted_keys()
        elif args.command == 'decrypt':
            files = [fn for fn in find_matching_files(ENCRYPTED_TAG)]
        if run_ansible_vault(args.command, files) != 0:
            sys.exit(1)
    elif args.command == 'verify':
        verify()
