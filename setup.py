from setuptools import find_packages, setup


def get_description():
    with open('README.md') as file:
        return file.read()


def get_requirements():
    with open('requirements.txt') as fp:
        reqs = list()
        for lib in fp.read().split("\n"):
            if not lib.startswith("-") or lib.startswith("#"):
                reqs.append(lib.strip())
        return reqs

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
    install_requires=get_requirements(),
    python_requires=">=3.7, <4",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ]
)
