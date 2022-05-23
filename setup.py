import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    install_requires = fh.read().splitlines()

setuptools.setup(
    name="py2lispIDyOM",
    version="0.0.1",
    author="Xinyi Guan",
    author_email="xinyi.guan@nyu.edu",
    description="A Python package for IDyOM model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xinyiguan/py2lispIDyOM",
    packages=setuptools.find_packages(exclude=['tests']),
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
