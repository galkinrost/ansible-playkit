import argparse
import os
import utils


HOOK_FILE_CONTENTS = 'ansible-playkit vault verify\n'


def install():
    filepath = os.path.join(os.getcwd(), '.git', 'hooks', 'pre-commit')
    if os.path.exists(filepath):
        utils.error('Git pre-commit hook already exists')
    with open(filepath, 'w+') as f:
        f.write(HOOK_FILE_CONTENTS)
    os.chmod(filepath, 0755)
    utils.ok('Git pre-commit hook installed')


def uninstall():
    filepath = os.path.join(os.getcwd(), '.git', 'hooks', 'pre-commit')
    if not os.path.exists(filepath):
        utils.error('Git pre-commit hook not exists')
    with open(filepath, 'r') as f:
        contents = f.read()
    if contents != HOOK_FILE_CONTENTS:
        utils.error('Git pre-commit hook looks modified. Uninstall it manually')
    os.remove(filepath)
    utils.ok('Git pre-commit hook uninstalled')


def is_git():
    return os.path.isdir(os.path.join(os.getcwd(), '.git/'))


def run(args_list):
    parser = argparse.ArgumentParser(prog='ansible-playkit hook', description='git pre-commit hook management')
    parser.add_argument('command', help='Command to execute (install/uninstall)')
    args = parser.parse_args(args_list)
    if args.command not in ['install', 'uninstall']:
        parser.print_help()
        utils.error('Unrecognized command')

    if not is_git():
        utils.error('This is not git project')

    if args.command == 'install':
        install()
    elif args.command == 'uninstall':
        uninstall()
