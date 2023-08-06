#!/usr/bin/python3
import os
import sys

__WARN__ = '''
We trust you have received the usual lecture from the local System
Administrator. It usually boils down to these three things:

    #1) Respect the privacy of others.
    #2) Think before you type.
    #3) With great power comes great responsibility.

PLEASE NOTE:
	Pudo Developers are not responsible for any misuse of Root Privileges
'''
def disclaimer():
	from . import PUDO_BINARY
	from . import MODE
	if (os.stat(PUDO_BINARY).st_mode == MODE):
		print('Looks like you have already accepted the Disclaimer')
		print('Enjoy Automation !!!')
		return
	print(__WARN__)
	sys.stdout.write('Yes I Agree [Y/n]: ')
	sys.stdout.flush()
	agree = os.read(sys.stdin.fileno(), 1).strip().decode()
	if agree in ('Y', 'y'):
		os.chmod(PUDO_BINARY, MODE)
		print('Thank you for Accepting and using Pudo')
		print('Enjoy Automation !!!')
		return
	print("It is great quality of you to respect other's privacy")
	print(":( But we miss you !!!")


if (__name__ == '__main__'):
	disclaimer()
