import logging
import shutil, os
from distutils import dir_util

#会社PC：HAL用
backup_tree = [
    ['C:\\Users\\hal\Documents\\HAL', 'H:\\HAL'],
    ['C:\\Users\\hal\\Documents\\NetBeansProjects\\hal-kanri', 'H:\\NetBeansProjects\\hal-kanri'],
    ['C:\\Users\\hal\\Documents\\NetBeansProjects\\IT-engineer-school', 'H:\\NetBeansProjects\\IT-engineer-school'],
    ['C:\\Users\\hal\\Documents\\NetBeansProjects\\owt-remote-observe-relay', 'H:\\NetBeansProjects\\owt-remote-observe-relay'],
    ['C:\\Users\\hal\\Documents\\OWT\\見える化サーバ', 'H:\\OWT\\見える化サーバ'],
]
#会社PC：個人用
'''
backup_tree = [
    ['C:\\Users\\hal\\Documents\\CTI', 'H:\\CTI'],
    ['C:\\Users\\hal\Documents\\HAL', 'H:\\HAL'],
    ['C:\\Users\\hal\\Documents\\HCS', 'H:\\HCS'],
    ['C:\\Users\\hal\\Documents\\jno', 'H:\\jno'],
    ['C:\\Users\\hal\\Documents\\Kali-Linux', 'H:\\Kali-Linux'],
    ['C:\\Users\\hal\\Documents\\NetBeansProjects', 'H:\\NetBeansProjects'],
    ['C:\\Users\\hal\\Documents\\OWT', 'H:\\OWT'],
    ['C:\\Users\\hal\\Documents\\マルカツ', 'H:\\マルカツ'],
    ['C:\\Users\\hal\\PycharmProjects', 'H:\\PycharmProjects'],
]
'''

#自宅PC

def _checkFile(h_path):
    a_files = os.listdir(h_path)
    for a_file in a_files:
        if os.path.isfile(h_path + "\\" + a_file) == True:
            if not os.access(h_path + "\\" + a_file, os.W_OK):
                os.chmod(h_path + "\\" + a_file, 128)   # Windows用
                #os.chmod(a_file, FILE_ATTRIBUTE_NORMAL)    0x00000080

        if os.path.isdir(h_path + "\\" + a_file) == True:
            _checkFile(h_path + "\\" + a_file)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

for a_tree in backup_tree:
    logging.info('バックアップ元：%s', a_tree[0])
    logging.info('バックアップ先：%s', a_tree[1])

    #ディレクトリ削除
    #shutil.rmtree(a_tree[1])

    #copytreeでは追加で上書きができない
    #shutil.copytree(a_tree[0],a_tree[1])
    dir_util.copy_tree(a_tree[0], a_tree[1])

    _checkFile(a_tree[1])

    logging.info('****** バックアップ完了 ******')
