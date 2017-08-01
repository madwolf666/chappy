import logging
import shutil, os
from distutils import dir_util

#会社PC
backup_tree = [
    ['C:\\Users\\hal\Documents\\HCS\電子教材印刷用PDF作成', 'G:\\なんだかんだ\\HCS\電子教材印刷用PDF作成'],
    ['C:\\Users\\hal\\Documents\\Kali-Linux', 'G:\\なんだかんだ\\Kali-Linux'],
    ['C:\\Users\\hal\\Documents\\OWT\\見える化サーバ', 'G:\\なんだかんだ\\OWT\\見える化サーバ'],
    ['C:\\Users\\hal\\Documents\\マルカツ\\レンタルシステム\\trouble', 'G:\\マルカツ\\レンタルシステム\\trouble'],
]
#['C:\\Users\\hal\Documents\\NetBeansProjects\\owt-remote-observe-relay', 'G:\\なんだかんだ\\NetBeansProjects\\owt-remote-observe-relay'],

#自宅PC

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

for a_tree in backup_tree:
    logging.info('バックアップ元：%s', a_tree[0])
    logging.info('バックアップ先：%s', a_tree[1])
    #copytreeでは追加で上書きができない
    #shutil.copytree(a_tree[0],a_tree[1])
    dir_util.copy_tree(a_tree[0], a_tree[1])
    logging.info('****** バックアップ完了 ******')
