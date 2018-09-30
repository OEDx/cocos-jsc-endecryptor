#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: khanzhang

import os
import xxtea
import zipfile
import sys
import getopt
import string
import gzip
from optparse import OptionParser


def write_content_to_file(file_name, content):
    file_ob = open(file_name, 'w')
    file_ob.write(content)
    file_ob.close()


def read_file_content(file_name):
    file_ob = open(file_name, 'r')
    content = file_ob.read()
    file_ob.close()
    return content


def zip_file(file_name, file_name_in_zip, zip_file_name):
    z_f = zipfile.ZipFile(zip_file_name, 'w')
    z_f.write(file_name, file_name_in_zip, zipfile.ZIP_DEFLATED)
    z_f.close()


def unzip_file(file_name, target_dir):
    try:
        z_f = zipfile.ZipFile(file_name, 'r')
        z_f.extractall(target_dir)
        z_f.close()
    except zipfile.BadZipfile:
        print 'error: unzip failed, please confirm zip opt and key is right.'
        return False
    else:
        return True


# the decrypt function contains :
# 1. decrypt .jsc file
# 2. unzip file if required

def decrypt(is_zip, input_key, input_jsc_path):

    print 'begin decrypt.'
    prefix = 'decryptOutput'

    jsc_path = input_jsc_path
    if jsc_path == '':
        jsc_path = raw_input('please input your .jsc path:')

    if os.path.exists(jsc_path) is False:
        print "error: your .jsb file is not exist."
        return False

    enc_file_content = read_file_content(jsc_path)

    key = input_key
    if key == '':
        key = raw_input('please input your encrypt key:')

    if key == '':
        print "error: your key is empty."
        return False

    dec = xxtea.decrypt(enc_file_content, key)
    des_file_name = prefix + '/dec.js'
    if os.path.exists(des_file_name) is True:
        os.remove(des_file_name)

    if os.path.exists(prefix) is True:
        os.system('rm -r ' + prefix)
    os.mkdir(prefix)
    write_content_to_file(des_file_name, dec)

    decrypt_file_name = prefix + '/decrypt.js'
    if is_zip is True:
        print 'begin unzip.'
        isUnzipSuc = unzip_file(des_file_name, prefix)
        os.remove(des_file_name)
        if isUnzipSuc is False:
            return False
        else:
            os.rename(prefix + '/encrypt.js', decrypt_file_name)
    else:
        os.rename(des_file_name, decrypt_file_name)

    print "success. please check 'decryptOutput' directory."
    print '> note: if your decrypt.js is 0b,',
    print 'please confirm your zip option and your decrypt key is right.'
    return True


# the encrypt function contains :
# 1. zip file if required
# 2. encrypt the code and write to file

def encrypt(is_zip, input_key, input_js_path):

    prefix = 'encryptTemp'
    if os.path.exists(prefix) is True:
        os.system('rm -r ' + prefix)
    os.mkdir(prefix)

    if os.path.exists("encryptOutput") is True:
        os.system('rm -r ' + "encryptOutput")
    os.mkdir("encryptOutput")

    js_path = input_js_path
    if js_path == '':
        js_path = raw_input('please input your .js path:')

    if os.path.exists(js_path) is False:
        print "error: your .js file is not exist."
        return False

    key = input_key
    if key == '':
        key = raw_input('please input your encrypt key:')

    if key == '':
        print "error: your key is empty."
        return False

    # zip .jsc
    if is_zip is True:
        print 'begin zip.'
        project_zip_name = prefix + '/projectChanged.zip'
        os.system("cp " + js_path + " " + prefix + '/encrypt.js')
        zip_file(prefix + '/encrypt.js', 'encrypt.js', project_zip_name)
        project_content = read_file_content(project_zip_name)
    else:
        project_content = read_file_content(js_path)
    # encrypt
    print 'begin encrypt.'
    enc = xxtea.encrypt(project_content, key)
    final_jsc_name = prefix + '/projectChanged.jsc'
    write_content_to_file(final_jsc_name, enc)

    os.system('cp ' + final_jsc_name + " encryptOutput/projectChanged.jsc")

    print 'remove temp file.'
    if os.path.exists(prefix) is True:
        os.system('rm -r ' + prefix)
    print "success. please check 'encryptOutput' directory."
    return True


def main():
    parser = OptionParser()

    path_help = "this is the encrypt/decrypt's source file path"
    nozip_help = "if set this param to 'true', it won't excute zip/unzip"
    key_help = "this is the encrypt/decrypt's key"

    parser.add_option("-p", "--path", dest="path", help=path_help)
    parser.add_option("-n", "--nozip", dest="nozip", help=nozip_help)
    parser.add_option("-k", "--key", dest="key", help=key_help)

    is_decrypt = True
    argv_len = len(sys.argv)
    if argv_len < 2:
        parser.print_help()
        return
    else:
        if sys.argv[1] == 'decrypt':
            is_decrypt = True
        elif sys.argv[1] == 'encrypt':
            is_decrypt = False
        elif (sys.argv[1] == '-h') | (sys.argv[1] == '--help'):
            parser.print_help()
            return
        else:
            print "please choose your function: decrypt or encrypt.",
            print "run the command like './edc.py decrypt'"
            return
        sys.argv.pop(1)

    (options, args) = parser.parse_args(sys.argv)

    is_zip = True
    key = ''
    path = ''

    if options.nozip == 'true':
        is_zip = False
    if options.key is not None:
        key = options.key

    if is_decrypt is True:
        if options.path is not None:
            path = options.path
        decrypt(is_zip, key, path)
    else:
        if options.path is not None:
            path = options.path
        encrypt(is_zip, key, path)


if __name__ == "__main__":
    main()
