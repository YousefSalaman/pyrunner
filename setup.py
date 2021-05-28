
import pathlib
import setuptools

PARENT_DIR = pathlib.Path(__file__).parent

setuptools.setup(
    name='pyrunner',
    version='0.0.0',
    packages=['pyrunner'],
    install_requires=['numpy'],
    long_description=(PARENT_DIR/'README.md').read_text()
)
