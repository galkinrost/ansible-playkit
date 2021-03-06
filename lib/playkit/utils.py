from __future__ import print_function
import sys


def ok(*msgs):
    msgs = list(msgs)
    msgs[0] = '\033[92m' + msgs[0]
    msgs[-1] = msgs[-1] + '\033[0m'
    print(*msgs)


def error(*msgs):
    msgs = list(msgs)
    msgs[0] = '\033[91m' + msgs[0]
    msgs[-1] = msgs[-1] + '\033[0m'
    print(*msgs, file=sys.stderr)
    sys.exit(1)


def user_input(question):
    if sys.version_info > (3, 0):
        return input(question)
    else:
        return raw_input(question)
