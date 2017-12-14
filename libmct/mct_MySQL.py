# -*- coding: utf-8 -*-

import sys
#Python2
#from urlparse import urlparse
#Python3
from urllib.parse import urlparse
import mysql.connector

class mct_MySQL:
    def __init__(
            self,
            h_url,
            h_host,
            h_port,
            h_user,
            h_password
            ):
        self.url_src = h_url
        self.host = h_host
        self.port = h_port
        self.user = h_user
        self.password = h_password

        self.conn = None

    def Connect(self):
        try:
            self.url = urlparse(self.url_src)
            #self.url = urlparse('mysql://root:kanri999@localhost:3306/hal_kanri')

            self.conn = mysql.connector.connect(
                host = self.url.hostname or self.host,
                port = self.url.port or self.port,
                user = self.url.username or self.user,
                password = self.url.password or self.password,
                database = self.url.path[1:],
            )
        except Exception as exp:
            a_strErr = " ".join(map(str, exp.args))
            #print a_strErr
        except:
            a_strErr = sys.exc_info()
            #print a_strErr

    def Quering(self, h_sql, h_condition):
        a_cursor = None
        try:
            #print(h_sql)
            a_cursor = self.conn.cursor(dictionary=True)
            a_query = (h_sql)
            a_cursor.execute(a_query, h_condition)

        except Exception as exp:
            a_cursor = None
            a_strErr = " ".join(map(str, exp.args))
            #print a_strErr
        except:
            a_cursor = None
            a_strErr = sys.exc_info()
            #print a_strErr

        return a_cursor

    def Disconnect(self):
        try:
            if (self.conn != None):
                self.conn.close()
        except Exception as exp:
            a_strErr = " ".join(map(str, exp.args))
        except:
            a_strErr = sys.exc_info()
