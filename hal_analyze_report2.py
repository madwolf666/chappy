# -*- coding: utf-8 -*-

import os
import sys
import datetime
import libmct.mct_MySQL as mct_MySQL

if __name__ == '__main__':
    a_args = sys.argv

    a_dt_now = datetime.datetime.now()
    #a_dt_prev = a_dt_now
    a_dt_str = a_dt_now.strftime('%Y-%m-%d')
    a_dt_str2 = a_dt_now.strftime('%Y年%m月%d日')
    #a_dt_prev += datetime.timedelta(days=-int(a_args[2]))
    #a_dt_str_prev = a_dt_prev.strftime('%Y-%m-%d')
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
    t1.*, \
    t2.*, \
    IFNULL((SELECT email_addr FROM m_user WHERE (idx=t2.reg_id)), (SELECT email_addr FROM m_user WHERE (idx=t2.upd_id))) AS email_addr \
    FROM \
    (SELECT cr_id, subject, accounts_contract_purchase_no, accounts_bai_previous_day FROM t_acceptance_ledger WHERE (accounts_bai_previous_day<= \'' + a_dt_str + '\') AND (NOT accounts_invoicing LIKE \'%○%\')) t1 \
    JOIN \
    (SELECT cr_id, contract_number, engineer_number, engineer_name, engneer_name_phonetic, claim_settlement_closingday, claim_accounts_invoicing, reg_id, upd_id FROM t_contract_report) t2 \
    ON (t1.cr_id=t2.cr_id) \
    ORDER BY email_addr;',
    '')

    a_file_list = []
    a_email_addr_now = ''
    a_email_addr_prev = ''

    if (a_cursor != None):
        a_sw = None
        for a_row in a_cursor.fetchall():
            a_dt_closing = a_row['accounts_bai_previous_day'];
            #締日の取得
            if (a_row['claim_settlement_closingday'] == '月末') or  (a_row['claim_settlement_closingday'] == ''):
                #月末の日を計算
                a_dt_str_tmp = a_dt_closing.strftime('%Y-%m') + "-01"
                a_dt_tmp = datetime.datetime.strptime(a_dt_str_tmp, '%Y-%m-%d')
                a_dt_tmp += datetime.timedelta(days=30)
                a_dt_str_tmp = a_dt_tmp.strftime('%Y-%m') + "-01"
                a_dt_tmp = datetime.datetime.strptime(a_dt_str_tmp, '%Y-%m-%d')
                a_dt_closing = a_dt_tmp + datetime.timedelta(days=-1)

                #次の日の曜日を判定
                a_dt_send = a_dt_closing + datetime.timedelta(days=1)
                if (a_dt_send.weekday() == 5):
                    #土曜日：プラス2
                    a_dt_send += datetime.timedelta(days=2)
                elif (a_dt_send.weekday() == 6):
                    #日曜日：プラス1
                    a_dt_send += datetime.timedelta(days=1)

            else:
                #数字での日を計算
                #a_dt_closing += datetime.timedelta(days=30)
                a_dt_str_tmp = a_dt_closing.strftime('%Y-%m') + "-" + a_row['claim_settlement_closingday']
                a_dt_closing = datetime.datetime.strptime(a_dt_str_tmp, '%Y-%m-%d')

                #締日の曜日を判定
                a_dt_send = a_dt_closing + datetime.timedelta(days=7)
                a_dt_send += datetime.timedelta(days=-(a_dt_send.weekday()))

            print('締日：' + a_dt_closing.strftime('%Y-%m-%d'))
            print(a_row['claim_accounts_invoicing'])
            if (a_row['claim_accounts_invoicing'] != None) and (int(a_row['claim_accounts_invoicing']) != 1):
                a_dt_send += datetime.timedelta(days=7*(int(a_row['claim_accounts_invoicing'])-1))

            print('請求書送付日：' + a_dt_send.strftime('%Y-%m-%d'))

            if (a_dt_send < a_dt_now):
                a_email_addr_now = a_row['email_addr']
                if (a_email_addr_now == None):
                    a_email_addr_now = ""
                if (a_email_addr_now != ''):
                    a_fname = a_args[1] + '/' + a_row['email_addr']
                    a_sw = open(a_fname, 'a')
                    if (a_email_addr_prev != a_email_addr_now):
                        a_sw.write('以下のエンジニアに対しては、' + a_dt_str2 + '時点で請求書が発行されていません。\n\n')
                        a_file_list.append(a_email_addr_now)

                    a_sw.write('-' * 20 + '\n')
                    #a_sw.write('契約開始日：' + a_row[0].strftime('%Y年%m月%d日') + '\n')
                    #a_sw.write('契約終了日：' + a_row[1].strftime('%Y年%m月%d日') + '\n')
                    a_sw.write('契約No：' + a_row['contract_number'].encode('utf-8') + '\n')
                    a_sw.write('エンジニアNo：' + a_row['engineer_number'].encode('utf-8') + '\n')
                    a_sw.write('エンジニア名：' + a_row['engineer_name'].encode('utf-8') + '\n')
                    a_sw.write('フリガナ：' + a_row['engneer_name_phonetic'].encode('utf-8') + '\n')
                    a_sw.write('件名：' + a_row['subject'].encode('utf-8') + '\n')
                    a_sw.write('注文書/契約書No：' + a_row['accounts_contract_purchase_no'].encode('utf-8') + '\n')
                    a_sw.write('売上日：' + a_row['accounts_bai_previous_day'].encode('utf-8') + '\n')

                    #print(a_row[0], a_row[1], a_row[2], a_row[3], a_row[4], a_row[5], a_row[6])
                    a_sw.close()
                a_email_addr_prev = a_email_addr_now

    a_mysql.Disconnect()

    for a_f in a_file_list:
       os.system('cat ' + a_args[1] + '/' + a_f + ' | ssh -i ../hal-rds.pem 172.31.27.122 \'cat > python/hal-mail2/' + a_f + '\'')
       os.remove(a_args[1] + '/' + a_f)

