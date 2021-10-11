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

# setuptools.setup(
#     name='preprocessing_text',
#     version=str(version.__version__),
# #     version='0.0.2'
#     author='linnkern',
#     author_email='kerncl@hotmail.com',
#     description='Preprocessing package',
#     long_description=long_description,
#     long_description_content_type='text/markdown',
#     packages=setuptools.find_packages(),
#     python_requires='>=3.6',
#     install_requires=dependencies,
# )


setuptools.setup(
	name = 'preprocess_text', #this should be unique
	version = str(version.__version__),
	author = 'linnkern',
	author_email = 'kerncl@hotmail.com',
	description = 'This is preprocessing package',
	long_description = long_description,
	long_description_content_type = 'text/markdown',
	packages = setuptools.find_packages(),
	classifiers = [
	'Programming Language :: Python :: 3',
	'License :: OSI Aproved :: MIT License',
	"Operating System :: OS Independent"],
	python_requires = '>=3.5',
	install_requires = dependencies
	)
