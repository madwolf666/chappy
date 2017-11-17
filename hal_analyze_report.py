# -*- coding: utf-8 -*-

import os
import sys
import datetime
import libmct.mct_MySQL as mct_MySQL

if __name__ == '__main__':
    a_args = sys.argv

    a_dt_now = datetime.datetime.now()
    a_dt_prev = a_dt_now
    a_dt_str = a_dt_now.strftime('%Y-%m-%d')
    a_dt_str2 = a_dt_now.strftime('%Y年%m月%d日')
    a_dt_prev += datetime.timedelta(days=-int(a_args[2]))
    a_dt_str_prev = a_dt_prev.strftime('%Y-%m-%d')
    #print(a_dt_str_prev)

    a_mysql = mct_MySQL.mct_MySQL(
        'mysql://root:kanri999@localhost:3306/hal_kanri',
        '',
        3306,
        '',
        '',
    )

    a_mysql.Connect()

    a_cursor = a_mysql.Quering(
    'SELECT \
    claim_agreement_start, \
    claim_agreement_end, \
    contract_number, \
    engineer_number, \
    engineer_name, \
    engneer_name_phonetic, \
    EXISTS (SELECT engineer_number FROM t_contract_report WHERE (engineer_number=ts.engineer_number) AND (claim_agreement_end > \'' + a_dt_str + '\')) AS is_exists \
    FROM t_contract_report ts \
    WHERE (claim_agreement_end >= \'' + a_dt_str_prev + '\') \
    AND (claim_agreement_end <= \'' + a_dt_str + '\') \
    ORDER BY engineer_number;',
    '')

    a_fname_only = a_dt_str + '.txt'
    a_fname = a_args[1] + '/' + a_fname_only
    a_isFirst = True

    if (a_cursor != None):
        a_sw = None
        for a_row in a_cursor.fetchall():
            if (a_row[6] == 0):
                if (a_isFirst == True):
                    a_sw = open(a_fname, 'w')
                    a_sw.write('以下のエンジニアは、' + a_dt_str2 + '時点で契約終了のものがありますが、次の契約情報が登録されていません。\n\n')
                    a_isFirst = False
                a_sw.write('-' * 20 + '\n')
                a_sw.write('契約開始日：' + a_row[0].strftime('%Y年%m月%d日') + '\n')
                a_sw.write('契約終了日：' + a_row[1].strftime('%Y年%m月%d日') + '\n')
                a_sw.write('契約No：' + a_row[2].encode('utf-8') + '\n')
                a_sw.write('エンジニアNo：' + a_row[3].encode('utf-8') + '\n')
                a_sw.write('エンジニア名：' + a_row[4].encode('utf-8') + '\n')
                a_sw.write('フリガナ：' + a_row[5].encode('utf-8') + '\n')
                #print(a_row[0], a_row[1], a_row[2], a_row[3], a_row[4], a_row[5], a_row[6])
        if (a_sw != None):
            a_sw.close()

    a_mysql.Disconnect()

    if (a_isFirst == False):
       os.system('cat ' + a_fname + ' | ssh -i ../hal-rds.pem 172.31.27.122 \'cat > python/hal-mail/' + a_fname_only + '\'')
       os.remove(a_fname)

