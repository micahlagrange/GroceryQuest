from distutils.core import setup
import py2exe
import glob

setup(
    console=['main.py'],
    name='Grocery quest',
    version='0.1',
    url='multivoxmuse.duckdns.org',
    author='multivoxmuse',
    zipfile=None,
    data_files=[
        ("resources\\sprites",
            glob.glob("resources\\sprites\\*.*"),),
        ("resources\\sounds",
         glob.glob("resources\\sounds\\*.*"),),
        ("resources\\maps",
         glob.glob("resources\\maps\\*.*"),),
        ("resources\\backgrounds",
         glob.glob("resources\\backgrounds\\*.*"),),
        ("resources\\entities",
         glob.glob("resources\\entities\\*.*"),),
        ("resources\\fonts",
         glob.glob("resources\\fonts\\*.ttf"),),
        (".",
         ["README.txt"],),
    ],
)