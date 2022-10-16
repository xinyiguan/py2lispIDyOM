import os


def command_install_sbcl(version='sbcl-2.2.9-x86-64-darwin'):
    """
    :param version: should be downloaded file name without extention '-binary...'
    """
    file_name = f'{version}-binary.tar.bz2'
    download = f'curl -L http://prdownloads.sourceforge.net/sbcl/{file_name} > {file_name}'
    unzip = f'bzip2 -cd {file_name} | tar xvf -'
    cd = f'cd {version}'
    install = 'sudo sh install.sh'
    command = '\n'.join([download,
                         unzip,
                         cd,
                         install])
    with open('install_sbcl.sh', 'w') as sbcl_sh:
        command = f'#!/bin/bash \n{command}'
        sbcl_sh.write(command)


def command_install_quicklisp() -> str:
    pass


def command_install_sqlite3() -> str:
    pass


def command_install_idyom() -> str:
    pass


def install() -> None:
    os.system(command_install_sbcl())
    os.system(command_install_quicklisp())
    os.system(command_install_sqlite3())
    os.system(command_install_idyom())


if __name__ == '__main__':
    command_install_sbcl()
