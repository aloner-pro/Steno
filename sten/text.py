import os
import subprocess
__author__ = "Sohel Ahmed"
'''
Module text.py for performing text stenography using SNOW
link - http://darkside.com.au/snow/   -- here you will get to 
about SNOW and also download it.
'''


def size(file: str):

    cmd = subprocess.Popen(['snow', '-S', file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = cmd.communicate()
    return str(stdout, 'utf-8').split()[-2]


def encode(passwd: str, infile: str, outfile: str, file: str = None, message: str = None):
    if message is not None:
        command = 'snow -C -Q -p "{}" -m "{}" {} {}'.format(passwd, message, infile, outfile)
        os.system('cmd /c' + command)
    elif file is not None:
        command = 'snow -C -Q -p "{}" -f {} {} {}'.format(passwd, file, infile, outfile)
        os.system('cmd /c' + command)


def decode(passwd: str, file: str):
    cmd = subprocess.Popen(['snow', '-C', '-p', passwd, file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = cmd.communicate()
    return str(stdout, 'utf-8')
