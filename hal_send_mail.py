# -*- coding: utf-8 -*-

import os
import sys
import libmct.mct_crawl as mct_crawl
import libmct.mct_mail as mct_mail

if __name__ == '__main__':
    a_args = sys.argv

    #JP='iso-2022-jp'
    auth = {
        "IS_SSL":True,
        "SMTP":"",
        "SMTP_SSL":"smtp.gmail.com",
        "PORT":465,
        "LOGIN_MAIL":a_args[2],
        "LOGIN_PASS":a_args[3],
    }

    a_files = os.listdir(a_args[1])
    for a_file in a_files:
        if os.path.isfile(a_args[1] + "/" + a_file) == True:
            #Python2
            #a_sr = open(a_args[1] + "/" + a_file, 'r')
            #Python3
            a_sr = open(a_args[1] + "/" + a_file, 'r', encoding='utf-8')
            a_result = a_sr.read()
            a_sr.close()

            msg = {
                #Python2
                #"SUBJECT":a_args[5],
                #Python3
                "SUBJECT":a_args[5].encode('utf-8'),
                "FROM":a_args[2],
                "TO":a_args[4],
                "BODY":a_result
            }

            mct_mail.Mail_Send(auth, msg)
