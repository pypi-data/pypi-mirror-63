import setuptools
 
# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
 
setuptools.setup(
    name="kopper",
    version="0.1.1",
    author="Seongmok Byeon",
    author_email="smbyun0214@gmail.com",
    description="This is a Korail seat reservation support service. \
        If you cannot make a reservation, we will tell you how to make a reservation \
            by adding an intermediate station.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/smbyeon/Kopper",
    packages=setuptools.find_packages(exclude = ['docs', 'dev']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests', 'beautifulsoup4'],
)