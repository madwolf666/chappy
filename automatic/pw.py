#! python3
# pw.py - パスワード管理プログラム（脆弱性あり）

PASSWORDS = {
    'office365': 'harry666',
    'onamae.com': 'chappy666',
    'facebook': 'chappy666',
    'twitter': 'harry666',
    'git': 'chappy666',
    'teamservice': 'chappy666',
    'oracle': 'ChappyHarry666',
    'rakuten': 'chappy999'
    }

import sys
import pyperclip

if len(sys.argv) < 2:
    print('使い方: python pw.py [アカウント名]')
    print('パスワードをクリップボードにコピーします')
    sys.exit()

account = sys.argv[1] # 最初のコマンドライン引数がアカウント名

if account in PASSWORDS:
    pyperclip.copy(PASSWORDS[account])
    print(account + 'のパスワードをクリップボードにコピーしました')
else:
    print(account + 'というアカウント名はありません')
