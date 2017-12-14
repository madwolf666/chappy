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
    EXISTS (SELECT engineer_number FROM t_contract_report WHERE (engineer_number=ts.engineer_number) AND (claim_agreement_end > \'' + a_dt_str + '\')) AS is_exists_next, \
    EXISTS (SELECT end_status FROM t_contract_end_report WHERE (cr_id=ts.cr_id) AND (insurance_crad=\'非対象者\')) AS is_exists_end, \
    IFNULL((SELECT email_addr FROM m_user WHERE (idx=ts.reg_id)), (SELECT email_addr FROM m_user WHERE (idx=ts.upd_id))) AS email_addr \
    FROM t_contract_report ts \
    WHERE (claim_agreement_end >= \'' + a_dt_str_prev + '\') \
    AND (claim_agreement_end <= \'' + a_dt_str + '\') \
    ORDER BY email_addr;',
    '')

    a_file_list = []
    a_email_addr_now = ''
    a_email_addr_prev = ''

    if (a_cursor != None):
        a_sw = None
        for a_row in a_cursor.fetchall():
            if (a_row['is_exists_next'] == 0) and (a_row['is_exists_end'] == 0):
                #次の契約レポートなし、かつ非対称者でない
                a_email_addr_now = a_row['email_addr']
                if (a_email_addr_now == None):
                    a_email_addr_now = ""
                if (a_email_addr_now != ''):
                    a_fname = a_args[1] + '/' + a_row['email_addr']
                    a_sw = open(a_fname, 'a')
                    if (a_email_addr_prev != a_email_addr_now):
                        a_sw.write('以下のエンジニアは、' + a_dt_str2 + '時点で契約終了のものがありますが、次の契約情報が登録されていません。\n\n')
                        a_file_list.append(a_email_addr_now)

                    a_sw.write('-' * 20 + '\n')
                    a_sw.write('契約開始日：' + a_row['claim_agreement_start'].strftime('%Y年%m月%d日') + '\n')
                    a_sw.write('契約終了日：' + a_row['claim_agreement_end'].strftime('%Y年%m月%d日') + '\n')
                    a_sw.write('契約No：' + a_row['contract_number'].encode('utf-8') + '\n')
                    a_sw.write('エンジニアNo：' + a_row['engineer_number'].encode('utf-8') + '\n')
                    a_sw.write('エンジニア名：' + a_row['engineer_name'].encode('utf-8') + '\n')
                    a_sw.write('フリガナ：' + a_row['engneer_name_phonetic'].encode('utf-8') + '\n')
                    #print(a_row[0], a_row[1], a_row[2], a_row[3], a_row[4], a_row[5], a_row[6])
                    a_sw.close()
                a_email_addr_prev = a_email_addr_now

    a_mysql.Disconnect()

    for a_f in a_file_list:
       os.system('cat ' + a_args[1] + '/' + a_f + ' | ssh -i ../hal-rds.pem 172.31.27.122 \'cat > python/hal-mail/' + a_f + '\'')
       os.remove(a_args[1] + '/' + a_f)

