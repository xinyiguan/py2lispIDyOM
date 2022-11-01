import setuptools

long_description = 'py2lispIDyOM is an open-source Python package that serves as a unifying Python interface that ' \
                   'simplifies and streamlines the research workflow for running the information dynamics of music ' \
                   '(IDyOM) model and analyzing output data.'

with open("requirements.txt", "r") as fh:
    install_requires = fh.read().splitlines()

setuptools.setup(
    name="py2lispIDyOM",
    version="1.0.2",
    author="Xinyi Guan",
    author_email="xinyi.guan@nyu.edu",
    description="A Python package for the information dynamics of music (IDyOM) model",
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
