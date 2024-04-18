from distutils.core import setup

setup(
    name='multiprocessing_logger',
    author='Martin Privat',
    version='0.2.6',
    packages=['multiprocessing_logger','multiprocessing_logger.tests'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    description='log from separate processes into a single file',
    long_description=open('README.md').read(),
    install_requires=[]
)