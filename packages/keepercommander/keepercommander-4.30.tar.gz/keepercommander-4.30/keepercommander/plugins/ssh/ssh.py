# -*- coding: utf-8 -*-
#  _  __  
# | |/ /___ ___ _ __  ___ _ _ ®
# | ' </ -_) -_) '_ \/ -_) '_|
# |_|\_\___\___| .__/\___|_|
#              |_|            
#
# Keeper Commander 
# Copyright 2016 Keeper Security Inc.
# Contact: ops@keepersecurity.com
#

import logging

from pexpect import pxssh, exceptions

"""Commander Plugin for SSH Command
   Dependencies: 
       pip3 install pexpect
"""

def rotate(record, newpassword):
    """ Grab any required fields from the record """
    user = record.login
    oldpassword = record.password

    result = False

    host = record.get('cmdr:host')

    try:
        s = pxssh.pxssh()
        s.login(host, user, oldpassword)
        s.sendline('passwd')
        i = s.expect(['[Oo]ld.*[Pp]assword', '[Cc]urrent.*[Pp]assword', '[Nn]ew.*[Pp]assword'])
        if i == 0 or i == 1:
            s.sendline(oldpassword)
            s.expect('[Nn]ew.*[Pp]assword')
        s.sendline(newpassword)
        s.expect("Retype [Nn]ew.*[Pp]assword:")
        s.sendline(newpassword)
        s.prompt()

        pass_result = s.before

        if "success" in str(pass_result):
            logging.info("Password changed successfully")
            record.password = newpassword
            result = True
        else:
            logging.error("Password change failed: ", pass_result)

        s.logout()
    except exceptions.TIMEOUT as t:
        logging.error("Timed out waiting for response.")
    except pxssh.ExceptionPxssh as e:
        logging.error("Failed to login with ssh.")

    return result
