from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="dsal",
    version="1.0.0",
    description="A Python package to implement datastructures .",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/chelladuraimohanraj/datastructures",
    author="mohanraj",
    author_email="chelladuraimohanraj@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["datastructures"],
    include_package_data=True,
  
)