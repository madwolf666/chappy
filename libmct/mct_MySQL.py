# -*- coding: utf-8 -*-

import sys
from urllib.parse import urlparse
import mysql.connector

class mct_MySQL():
    url = None
    conn = None

    def Connect(self):
        try:
            self.url = urlparse('mysql://root:kanri999@localhost:3306/hal_kanri')

            self.conn = mysql.connector.connect(
                host = self.url.hostname or 'localhost',
                port = self.url.port or 3306,
                user = self.url.username or 'root',
                password = self.url.password or '',
                database = self.url.path[1:],
            )
        except Exception as exp:
            a_strErr = " ".join(map(str, exp.args))
        except:
            a_strErr = sys.exc_info()

    def Quering(self, h_sql, h_condition):
        a_cursor = None
        try:
            a_cursor = self.conn.cursor()
            a_query = (h_sql)
            a_cursor.execute(a_query, h_condition)

        except Exception as exp:
            a_cursor = None
            a_strErr = " ".join(map(str, exp.args))
        except:
            a_cursor = None
            a_strErr = sys.exc_info()

        return a_cursor

    def Disconnect(self):
        try:
            if (self.conn != None):
                self.conn.close()
        except Exception as exp:
            a_strErr = " ".join(map(str, exp.args))
        except:
            a_strErr = sys.exc_info()
