import setuptools
from preprocessing_text import _version as version

with open('README.md', 'r') as f:
    long_description = f.read()

dependencies = [
    'numpy',
    'pandas',
    'spacy',
    'textblob',
    'bs4',
]

setuptools.setup(
    name='preprocessing_text',
    version=str(version.__version__),
    author='linnkern',
    author_email='kerncl@hotmail.com',
    description='Preprocessing package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=dependencies,
)
