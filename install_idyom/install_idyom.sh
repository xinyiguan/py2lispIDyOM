#!/bin/bash

SCRIPTPATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd ~ || exit
curl -L http://prdownloads.sourceforge.net/sbcl/sbcl-2.2.9-x86-64-darwin-binary.tar.bz2 > sbcl-2.2.9-x86-64-darwin-binary.tar.bz2
bzip2 -cd sbcl-2.2.9-x86-64-darwin-binary.tar.bz2 | tar xvf -
cd sbcl-2.2.9-x86-64-darwin || exit
sudo sh install.sh

cd ~ || exit
mkdir -p quicklisp
cd quicklisp || exit
curl -O https://beta.quicklisp.org/quicklisp.lisp
INSTALL2_PATH=${SCRIPTPATH}/install_pt2.lisp
cd ~ || exit
cd quicklisp || exit
sbcl --load $INSTALL2_PATH


cd ~ || exit
mkdir -p idyom/db/
mkdir -p idyom/data/cache/
mkdir -p idyom/data/models/
mkdir -p idyom/data/resampling/

cd ~ || exit
curl -L https://github.com/mtpearce/idyom/archive/refs/tags/v1.6.zip > idyom-1.6.tar.gz
tar -xvf idyom-1.6.tar.gz -C quicklisp/local-projects/
INSTALL3_PATH=${SCRIPTPATH}/install_pt3.lisp
cat $INSTALL3_PATH  >> ~/.sbclrc


INSTALL4_PATH=${SCRIPTPATH}/install_pt4.lisp
cd ~ || exit
sbcl --load $INSTALL4_PATH