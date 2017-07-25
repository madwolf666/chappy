import logging
import shutil, os
from distutils import dir_util

backup_tree = [
    ['C:\\Users\\hal\\Documents\\OWT\\PBXリモート開発', 'G:\\OWT\\PBXリモート開発'],
]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

for a_tree in backup_tree:
    logging.info('バックアップ元：%s', a_tree[0])
    logging.info('バックアップ先：%s', a_tree[1])
    #copytreeでは追加で上書きができない
    #shutil.copytree(a_tree[0],a_tree[1])
    dir_util.copy_tree(a_tree[0], a_tree[1])
    logging.info('****** バックアップ完了 ******')
