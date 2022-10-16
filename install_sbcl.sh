#!/bin/bash 
curl -L http://prdownloads.sourceforge.net/sbcl/sbcl-2.2.9-x86-64-darwin-binary.tar.bz2 > sbcl-2.2.9-x86-64-darwin-binary.tar.bz2
bzip2 -cd sbcl-2.2.9-x86-64-darwin-binary.tar.bz2 | tar xvf -
cd sbcl-2.2.9-x86-64-darwin
sudo sh install.sh