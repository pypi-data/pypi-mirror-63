from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["Faker>=4", "StringGenerator>=0", "termcolor>=1"]

setup(
    name="randomplayground",
    version="0.0.4",
    author="@PyOctoCat",
    author_email="davidinco@gmail.com",
    description="A package to help with random generator methods",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/RandomPlayGround/random-play-ground",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)