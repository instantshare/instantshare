from distutils.core import setup

setup(
    name="instantshare",
    version="0.1dev",
    description="Tool for taking screenshots and instantly sharing them using a number of services",
    long_description="\n" + open("README.rst").read(),
    author="instantshare",
    author_email="instantsharegit@gmail.com",
    url="https://github.com/instantshare/instantshare",
    download_url="https://drive.google.com/folderview?id=0B1oOthWBBgZyNVM1Z0ZfTzZfckk&usp=sharing",
    platforms="Microsoft Windows, GNU/Linux",
    license="GNU General Public License v2.0",
    install_requires=[
        "dropbox",
        "google-api-python-client",
        "pillow",
        "paramiko",
        "pyocclient"
    ],
    packages=["src", "src.screenshot", "src.storage", "src.tools"]
)
