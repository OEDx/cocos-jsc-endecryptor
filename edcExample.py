#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: khanzhang

import edc
import sys
import os


# this is an efficient way to change the code,
# with no need to wait for a long time to rebuild cocos

def edcExample(is_zip, key, jsc_path):

    # prepare
    prefix = 'edcExample'
    if os.path.exists(prefix) is True:
        os.system('rm -r ' + prefix)
    os.mkdir(prefix)

    # invoke the edc.decrypt function to decrypt .jsc file
    is_decrypt_suc = edc.decrypt(is_zip, key, jsc_path)
    if is_decrypt_suc is False:
        print 'decrypt failed.'
        return

    # change .js code
    print 'begin to change the code.'
    project_file_name = 'decryptOutput/decrypt.js'
    project_file = open(project_file_name)
    changed_project_file = open(prefix + '/projectChanged.js', 'w')

    for one_line in project_file.readlines():
        # first parameter is the code need to be replaced,
        # second parameter is the new code
        original_code = "This is a special code to be replaced"
        replace_code = "This is the code to replace"
        temp_content = one_line.replace(original_code, replace_code)
        changed_project_file.write(temp_content)

    project_file.close()
    changed_project_file.close()

    # invoke the edc.encrypt function to encrypt .js file
    is_encrypt_suc = edc.encrypt(is_zip, key, 'decryptOutput/decrypt.js')
    if is_encrypt_suc is False:
        print 'encrypt failed.'
        return


def main():
    edcExample(True, '', '')


if __name__ == "__main__":
    main()
