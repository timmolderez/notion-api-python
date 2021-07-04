from setuptools import find_packages, setup


def get_description():
    with open("README.md") as file:
        return file.read()


setup(
    name="notion-api-python",
    version="0.1",
    url="https://github.com/timmolderez/notion-api-python",
    author="Tim Molderez",
    author_email="id@timmolderez.be",
    description="Unofficial Python client for the public Notion API",
    long_description=get_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.7, <4",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ]
)
