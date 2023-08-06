**Pudo Package**

This is an Python Package for running Linux commands with root permission.
We can see this as an alternative to Linux sudo command without password prompt.
This is very handy when you are writing python automation scripts and need to deal with root privileges.
You can use this as an python module or an Linux command.

Before using the pudo, please accept the Disclaimer:

    user$ sudo python3 -m pudo.disclaimer # or python2
	We trust you have received the usual lecture from the local System
	Administrator. It usually boils down to these three things:

		#1) Respect the privacy of others.
		#2) Think before you type.
		#3) With great power comes great responsibility.

	PLEASE NOTE:
		Pudo Developers are not responsible for any misuse of Root Privileges

	Yes I Agree [Y/n]: y
	Thank you for Accepting and using Pudo
	Enjoy Automation !!!

Below is the code snippet for using in python automation for running commands under root privilege:

    user$ python3 # or python2
    >>> import pudo
    >>> (ret, out) = pudo.run(('ls', '/root')) # or pudo.run('ls /root')
    >>> print(ret)
    >>> 0
    >>> print(out)
    >>> b'Desktop\nDownloads\nPictures\nMusic\n'

Below is the cmd example for running commands under root privilege:

    user$ pudo ls /root
    Desktop  Downloads  Pictures  Music
