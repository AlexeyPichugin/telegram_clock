try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

from os.path import join, dirname
import io, re

with io.open("telegram_clock/__init__.py", "r") as f:
    version = re.search(r"__version__ = \"(.*?)\"", f.read()).group(1)

setup(
    name='telegram_clock',
    version=version,
    packages=find_packages(),
    license='MIT',
    author="Alexey Pichugin",
    author_email="a.o.pichugin@outlook.com",
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    install_requires=['telegram_clock']
)
