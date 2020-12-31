from setuptools import find_packages
from setuptools import setup


setup(
    name='web-ssh-proxy',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-SocketIO',
        'Flask-Executor',
        'paramiko',
    ],
)
