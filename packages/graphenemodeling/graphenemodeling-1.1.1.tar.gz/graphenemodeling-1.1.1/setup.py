import pathlib
import os
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file

with open(os.path.join(HERE,"README.md")) as file:
    README = file.read()

setup(
        name="graphenemodeling",
        version="1.1.1",
        description="Code for modeling graphene",
        long_description=README,
        long_description_content_type="text/markdown",
        url="https://github.com/gholdman1/graphenemodeling.git",
        author="gholdman",
        author_email="gholdman@protonmail.com",
        packages=find_packages(),
        include_package_data=True,
        install_requires=["numpy","scipy","matplotlib"]
        )

