from setuptools import setup, find_packages
from os import path

# Read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="zoho-client-django",
    version="1.2.2",  # Update this for new versions
    description="Django app which is a client for the Zoho CRM API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Guy Moller",
    author_email="guy.moller@gmail.com",
    url="https://github.com/gosourcellc/zoho-client-django",
    packages=find_packages(),
    package_data={
        "zoho_client": ["templates/admin/zoho_client/zohotoken/*.html"],
    },
    install_requires=[
        "Django>=4.1,<5.0",
        "requests>=2.31.0,<3.0",
    ],
)
