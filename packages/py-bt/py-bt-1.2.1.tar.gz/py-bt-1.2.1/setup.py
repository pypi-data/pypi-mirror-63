from setuptools import setup, find_packages

deps = [
    "PyYAML==5.3",
    "jsonschema==3.2.0",
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="py-bt",
    version="1.2.1",
    author="David Lavelle",
    author_email="davidlavelle1@hotmail.com",
    description="Python package for modelling and executing Behaviour Trees.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dlavelle7/py-bt",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_dir={'': '.'},
    include_package_data=True,
    install_requires=deps,
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
)
