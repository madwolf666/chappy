import mct_scrap

g_cl = mct_scrap.ConversationLearning('ptna', 'dics/random.txt', 'dics/pattern.txt', 'dics/template.txt', 'dics/log.txt')  # Ptnaオブジェクトを保持
g_log = []


def putlog(str):
    """ 対話ログをリストボックスに追加する関数
        @str  入力文字列または応答メッセージ
    """
    # lb.insert(tk.END, str)
    # インプットと応答をリストlogに追加
    g_log.append(str + '\n')


def writeLog():
    """ ログファイルに辞書を更新した日時を記録
    """
    # ログを作成
    # now = 'Ptna System Dialogue Log: ' + datetime.now().strftime(
    #    '%Y-%m-%d %H:%m::%S' + '\n')
    # log.insert(0, now)
    # ログファイルへの書き込み
    with open('dics/log.txt', 'a', encoding='utf_8') as f:
        f.writelines(g_log)

if __name__ == '__main__':
    while True:
        a_input_words = input(u"You: ")
        putlog(a_input_words)
        if a_input_words:
            a_response = g_cl.dialogue(a_input_words)
            putlog(a_response)
            print(u"Me: " + a_response)

        else:
            break

    g_cl.save()  # 記憶メソッド実行
    writeLog()  # ログの保存
