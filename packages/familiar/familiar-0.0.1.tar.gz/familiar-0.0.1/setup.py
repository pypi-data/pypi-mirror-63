from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='familiar',
    version='0.0.1',
    description='Dungeons and Dragons helper functions',
    py_modules=['familiar'],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment :: Role-Playing"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JDSalisbury/familiar",
    author='Jeff Salisbury',
    author_email='pip.familiar@gmail.com'
)
