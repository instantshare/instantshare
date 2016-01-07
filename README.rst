============
instantshare
============
Tool for taking screenshots and instantly sharing them using a number of services.

Currently supported are:

- Dropbox
- Google Drive
- SFTP

Services to be added in the future:

- FTP
- Owncloud (once their API gets updated to Python 3)
- maybe a specialized self-made Webservice
- ...

Installation
============
At this point, the supported platforms are Windows and GNU/Linux.
We might consider adding MAC OSX support at some point in the future.

Currently, we do not ship any binaries or packages, but you can download and extract the sources.
Or just clone the repository to any directory using

.. code-block:: bash
  
    $ git clone https://github.com/instantshare/instantshare.git

Windows
-------
- Download and install Python 3.5: https://www.python.org/downloads/
- Install the dependencies using pip:

    pip install -r requirements.txt

Sometimes installing paramiko leads to problems. Depending on your python version, there are different solutions to this problem. The following solution should fix the problem:

- Install Visual Studio Community 2015 with Visual C++ (VS2015 only for Python 3.5+, Check which version you need first)
- Download pycrypto source (https://www.dlitz.net/software/pycrypto/) (currently (01/2016) the stable release is pycrypto-2.6.1. Use this one and not the experimental 2.7a1 version below. Your version numbers may vary depending on when you read this.)
- Extract the archive
- Edit the file "lib/Crypto/Random/OSRNG/nt.py" and replace

.. code-block:: bash

    import winrandom
    
with

.. code-block:: bash

    from Crypto.Random.OSRNG import winrandom

See also: https://github.com/dlitz/pycrypto/commit/10abfc8633bac653eda4d346fc051b2f07554dcd#diff-f14623ba167ec6ff27cbf0e005d732a7

- Run the following commands from cmd:

    python setup.py build -c msvc
    python setup.py install
    python setup.py test
    
- If the test gets you some errors, you might get away with it anyways
- Test, if you can build the instantshare project now
- If not, try installing paramiko again:

    pip install paramiko

- If you get an error about vcvarsall.bat missing, start the Visual Studio installer again, click edit and make sure you install Visual C++ from Programming Languages

Useful links to this issue:

http://stackoverflow.com/questions/24804829/another-one-about-pycrypto-and-paramiko

http://www.paramiko.org/installing.html#pycrypt

https://yorickdowne.wordpress.com/2010/12/22/compiling-pycrypto-on-win7-64/

http://stackoverflow.com/questions/23769892/pycrypto-for-python-3-4-on-windows-8-1-cannot-find-winrandom-module

Linux
-----
- Install Python 3.5 using your package manager if it does not come with your distro
- Install gnome-screenshot and xclip using your package manager
- Install dependencies using pip (if pip is not installed yet, install python-pip using your package manager)
- You might need to manually change the permissions of the cacerts.txt file used by httplib2 to 644.

.. code-block:: bash

    $ sudo chmod 644 /usr/lib/python3.5/[...]/httplib2/cacerts.txt
