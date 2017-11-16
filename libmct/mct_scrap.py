import sys
import MeCab
from janome.tokenizer import Tokenizer
import random
import re
from itertools import chain # itertoolsモジュールからchainをインポート

###############################################################################
# 辞書学習
###############################################################################
def analyze(text):
    t = Tokenizer()
    tokens = t.tokenize(text)
    result = []
    for token in tokens:
        result.append(
            [token.surface,
             token.part_of_speech])
    return(result)

def keyword_check(part):
    return re.match('名詞,(一般|固有名詞|サ変接続|形容動詞語幹)', part)

def parse(text):
    t = Tokenizer()
    tokens = t.tokenize(text)
    result = []
    for token in tokens:
        result.append(token.surface)
    return(result)

class Dictionary:
    def __init__(self, h_randomDict, h_patternDict, h_templateDict, h_passedSentence):    #updated.
        """ 辞書を作成
        """

        #updated start
        self.a_randomDict = h_randomDict
        self.a_patternDict = h_patternDict
        self.a_templateDict = h_templateDict
        self.a_passedSentence = h_passedSentence
        #updated end

        self.load_random()
        self.load_pattern()
        self.load_template()
        self.load_markov()

    def load_random(self):
        """ ランダム辞書を作成
        """
        # ランダム辞書を保持するリスト
        self.random = []
        # ランダム辞書ファイルオープン
        #updated start
        #rfile = open('dics/random.txt', 'r', encoding='utf_8')
        rfile = open(self.a_randomDict, 'r', encoding='utf_8')
        #updated end
        # 各行を要素としてリストに格納
        r_lines = rfile.readlines()
        rfile.close()

        # 末尾の改行と空白文字を取り除いて
        # インスタンス変数（リスト）に格納
        for line in r_lines:
            str = line.rstrip('\n')
            if (str != ''):
                self.random.append(str)

    def load_pattern(self):
        """ パターン辞書を作成
        """
        # パターン辞書を保持するリスト
        self.pattern = []
        # パターン辞書オープン
        #updated start
        #pfile = open('dics/pattern.txt', 'r', encoding='utf_8')
        pfile = open(self.a_patternDict, 'r', encoding='utf_8')
        #updated end
        # 各行を要素としてリストに格納
        p_lines = pfile.readlines()
        pfile.close()
        # 末尾の改行と空白文字を取り除いて
        # インスタンス変数（リスト）に格納
        self.new_lines = []
        for line in p_lines:
            str = line.rstrip('\n')
            if (str != ''):
                self.new_lines.append(str)

        # 辞書データの各行をタブで切り分ける
        # ptn 正規表現のパターン
        # prs 応答例
        # ParseItemオブジェクトを生成(引数はptn、prs）して
        # インスタンス変数pattern（リスト）に追加
        for line in self.new_lines:
            ptn, prs = line.split('\t')
            self.pattern.append(ParseItem(ptn, prs))

    def load_template(self):
        """ テンプレート辞書を作成
        """
        # テンプレート辞書を保持する辞書
        self.template = {}
        # テンプレート辞書ファイルオープン
        #updated start
        #tfile = open('dics/template.txt', 'r', encoding='utf_8')
        tfile = open(self.a_templateDict, 'r', encoding='utf_8')
        #updated end
        # 各行を要素としてリストに格納
        t_lines = tfile.readlines()
        tfile.close()

        # 末尾の改行と空白文字を取り除いて
        # インスタンス変数（リスト）に格納
        self.new_t_lines = []
        for line in t_lines:
            str = line.rstrip('\n')
            if (str != ''):
                self.new_t_lines.append(str)
                # print(self.new_t_lines)

        # テンプレート辞書の各行をタブで切り分ける
        # count    %noun%の出現回数
        # template テンプレート文字列
        # ParseItemオブジェクトを生成(引数はptn、prs）して
        # インスタンス変数pattern（リスト）に追加
        for line in self.new_t_lines:
            # テンプレート行をタブでcount, templateに分割
            count, template = line.split('\t')
            # self.templateのキーにcount(出現回数)が存在しなければ
            # countをキーにして空のリストを要素として追加
            if not count in self.template:
                self.template[count] = []

            # countキーのリストにテンプレート文字列を追加
            self.template[count].append(template)

    def load_markov(self):
        """ マルコフ辞書を作成
        """
        # ログ辞書からマルコフ連鎖で生成した文章を保持するリスト
        self.sentences = []
        # Markovオブジェクトを生成
        #↓updated.
        #markov = Markov()
        ## マルコフ連鎖で生成された文章群を取得
        #text = markov.make()
        #print(self.a_passedSentence)
        a_wordlist = Scrap_Janome_Parse("", self.a_passedSentence, "")
        a_dict = Scrap_Janome_Markov_Dict(a_wordlist, "")
        text = Scrap_Janome_Markov_Chain(a_wordlist, a_dict)
        #↑Updated.
        # 各文章の末尾の改行で分割してリストに格納
        self.sentences = text.split('\n')
        # リストから空の要素を取り除く
        if '' in self.sentences:
            self.sentences.remove('')

    def study(self, input, parts):
        """ study_random()、study_pattern()、study_template()を呼ぶ

            @param input  ユーザーの発言
            @param parts  形態素解析結果
        """
        # インプット文字列末尾の改行は取り除いておく
        input = input.rstrip('\n')
        # 各学習メソッドを呼び分ける
        # @param input インプット文字列
        # @param parts  インプット文字列の形態素
        self.study_random(input)
        self.study_pattern(input, parts)
        self.study_template(parts)

    def study_random(self, input):
        """ ユーザーの発言を学習する

            @param input  ユーザーの発言
        """
        # 発言がランダム辞書に存在しなければ
        # self.randomの末尾に追加
        if not input in self.random:
            self.random.append(input)

    def study_pattern(self, input, parts):
        """ パターンを学習する

            @param input  ユーザーの発言
            @param input  ユーザーの発言
        """
        for word, part in parts:
            # 名詞であるかをチェック
            if (keyword_check(part)):
                depend = False  # ParseItemオブジェクトを保持する変数
                # patternリストのpatternキーを反復処理
                for ptn_item in self.pattern:
                    m = re.search(ptn_item.pattern, word)
                    # インプットされた名詞が既存のパターンとマッチしたら
                    # patternリストからマッチしたParseItemオブジェクトを取得
                    if (re.search(ptn_item.pattern, word)):
                        depend = ptn_item
                        break  # マッチしたら止める
                # 既存パターンとマッチしたParseItemオブジェクトから
                # add_phraseを呼ぶ
                if depend:
                    depend.add_phrase(input)  # 引数はインプット文字列

                else:
                    # 既存パターンに存在しない名詞であれば
                    # 新規のPatternItemオブジェクトを
                    # patternリストに追加
                    self.pattern.append(ParseItem(word, input))

    def study_template(self, parts):
        """ テンプレートを学習する

        @param parts  形態素解析の結果（リスト）
        """
        template = ''
        count = 0
        for word, part in parts:
            # 名詞であるかをチェック
            if (keyword_check(part)):
                word = '%noun%'
                count += 1
            template += word

        # self.templateのキーにcount(出現回数)が存在しなければ
        # countをキーにして空のリストを要素として追加

        if count > 0:
            count = str(count)

            if not count in self.template:
                self.template[count] = []
            # countキーのリストにテンプレート文字列を追加
            if not template in self.template[count]:
                self.template[count].append(template)

    def save(self):
        """ self.random、self.pattern、self.templateの内容を
            辞書にファイルに書き込む
        """
        # 各要素の末尾に改行を追加する
        for index, element in enumerate(self.random):
            self.random[index] = element + '\n'
        # ランダム辞書に書き込む
        #updated start
        #with open('dics/random.txt', 'w', encoding='utf_8') as f:
        with open(self.a_randomDict, 'w', encoding='utf_8') as f:
            f.writelines(self.random)
        #updated end

        pattern = []
        for ptn_item in self.pattern:
            # make_line()呼び出し
            pattern.append(ptn_item.make_line() + '\n')

        # パターン辞書に書き込む
        #updated start
        #with open('dics/pattern.txt', 'w', encoding='utf_8') as f:
        with open(self.a_patternDict, 'w', encoding='utf_8') as f:
            f.writelines(pattern)
        #updated end

        template = []
        # self.templateのすべてのキーと値のペアを取得して
        # 反復処理を行う
        for key, val in self.template.items():
            # 値のリストをイテレートし
            # 「キー + タブ + リストの個々の要素 + 改行」の1行を作る
            for v in val:
                template.append(key + '\t' + v + '\n')
                # print(template)
        # テンプレート辞書に書き込む
        #updated start
        #with open('dics/template.txt', 'w', encoding='utf_8') as f:
        with open(self.a_templateDict, 'w', encoding='utf_8') as f:
            f.writelines(template)
        #updated end

class ParseItem:
    SEPARATOR = '^((-?\d+)##)?(.*)$'

    def __init__(self, pattern, phrases):
        """ @param pattern  パターン
            @param phrases  応答例
        """
        # 辞書のパターンの部分にSEPARATORをパターンマッチさせる
        m = re.findall(ParseItem.SEPARATOR, pattern)
        # インスタンス変数modifyに0を代入
        self.modify = 0
        # マッチ結果の整数の部分が空でなければ値を代入
        if m[0][1]:
            self.modify = int(m[0][1])
        # インスタンス変数patternにマッチ結果のパターン部分を代入
        self.pattern = m[0][2]

        self.phrases = []  # 応答例を保持するインスタンス変数
        self.dic = {}  # インスタンス変数
        # 引数で渡された応答例を'|'で分割し、
        # 個々の要素に対してSEPARATORをパターンマッチさせる
        # self.phrases[ 'need'  : 応答例の整数部分
        #               'phrase': 応答例の文字列部分 ]
        for phrase in phrases.split('|'):
            # 応答例に対してパターンマッチを行う
            m = re.findall(ParseItem.SEPARATOR, phrase)
            # 'need'キーの値を整数部分m[0][1]にする
            # 'phrase'キーの値を応答文字列m[0][2]にする
            self.dic['need'] = 0
            if m[0][1]:
                self.dic['need'] = int(m[0][1])
            self.dic['phrase'] = m[0][2]
            # 作成した辞書をphrasesリストに追加
            self.phrases.append(self.dic.copy())

    def match(self, str):
        """self.pattern(各行ごとの正規表現)を
           インプット文字列にパターンマッチ
        """
        return re.search(self.pattern, str)

    def choice(self, mood):
        """インスタンス変数phrases(リスト）の
           要素('need''phrase'の辞書)
            'need':数値を

            @param mood 現在の機嫌値
        """
        choices = []
        # self.phrasesが保持するリストの要素（辞書）を反復処理する
        for p in self.phrases:
            # self.phrasesの'need'キーの数値と
            # パラメーターmoodをsuitable()に渡す
            # 結果がTrueであればchoicesリストに'phrase'キーの応答例を追加
            if (self.suitable(p['need'], mood)):
                choices.append(p['phrase'])
        # choicesリストが空であればNoneを返す
        if (len(choices) == 0):
            return None
            # choicesリストが空でなければランダムに
            # 応答文字列を選択して返す
        return random.choice(choices)

    def suitable(self, need, mood):
        """必要機嫌値を現在の機嫌値と比較

            @param need 必要機嫌値
            @param mood 現在の機嫌値
        """

        #updated start
        return True
        #updated end

        # 必要機嫌値が0であればTrueを返す
        if (need == 0):
            return True
        # 必要機嫌値がプラスの場合は機嫌値が必要機嫌値を超えているか判定
        elif (need > 0):
            return (mood > need)
        # 応答例の数値がマイナスの場合は機嫌値が下回っているか判定
        else:
            return (mood < need)

    def add_phrase(self, phrase):
        """インスタンス変数phrases(リスト）の
           要素('need''phrase'の辞書)
            'need':数値を

            @param phrase インプット文字列
        """
        # インプット文字列がphrasesリストの応答例に一致するか
        # self.phrases  インプットにマッチした応答フレーズの辞書リスト
        # [ {'need'  : 応答例の整数部分, 'phrase': 応答例の文字列部分}, ... ]
        for p in self.phrases:
            # 既存の応答例に一致したら終了
            if p['phrase'] == phrase:
                return
        # phrasesリストに辞書を追加
        # {'need'  :0, 'phrase':インプット文字列}
        self.phrases.append({'need': 0, 'phrase': phrase})

    def make_line(self):
        """

        """
        # 必要機嫌値 + '##' + パターン
        pattern = str(self.modify) + '##' + self.pattern
        phrases = []
        for p in self.phrases:
            resp = str(p['need']) + '##' + str(p['phrase'])
            phrases.append(str(p['need']) + '##' + str(p['phrase']))
        line = pattern + '\t' + '|'.join(phrases)
        return pattern + '\t' + '|'.join(phrases)


class Responder:
    """ 応答クラスのスーパークラス
    """

    def __init__(self, name, dictionary):
        """ Responderオブジェクトの名前をnameに格納

            @param name       Responderオブジェクトの名前
            @param dictionary Dictionaryオブジェクト
        """
        self.name = name
        self.dictionary = dictionary

    def response(self, input, mood, parts):
        """ オーバーライドを前提としたresponse()メソッド

            @param  input 入力された文字列
            @param  mood  機嫌値
            戻り値  空の文字列
        """
        return ''

    def get_name(self):
        """ 応答オブジェクトの名前を返す
        """
        return self.name


class RepeatResponder(Responder):
    """ オウム返しのための行うサブクラス
    """

    def response(self, input, mood, parts):
        """ 応答文字列を作って返す

            @param  input 入力された文字列
            @param  mood  機嫌値
        """
        return '{}ってなに？'.format(input)


class RandomResponder(Responder):
    """ ランダムな応答のための行うサブクラス
    """

    def response(self, input, mood, parts):
        """ 応答文字列を作って返す

            @param  input 入力された文字列
            戻り値  リストからランダムに抽出した文字列
        """
        return random.choice(self.dictionary.random)


class PatternResponder(Responder):
    """ パターンに反応するためのサブクラス
    """

    def response(self, input, mood, parts):
        """ パターンにマッチした場合に応答文字列を作って返す

            @param  input 入力された文字列
        """
        self.resp = None
        for ptn_item in self.dictionary.pattern:
            # match()でインプット文字列にパターンマッチを行う
            m = ptn_item.match(input)
            # マッチした場合は機嫌値moodを引数にしてchoice()を実行、
            # 戻り値の応答文字列、またはNoneを取得
            if (m):
                self.resp = ptn_item.choice(mood)
            # choice()の戻り値がNoneでない場合は
            # 応答例の中の%match%をインプットされた文字列内の
            # マッチした文字列に置き換える
            if self.resp != None:
                return re.sub('%match%', m.group(), self.resp)
        # パターンマッチしない場合はランダム辞書から返す
        return random.choice(self.dictionary.random)


class TemplateResponder(Responder):
    """ テンプレートを利用して応答を生成するためのサブクラス
    """

    def response(self, input, mood, parts):
        """ パターンに反応するためのサブクラス
        @param input インプット文字列
        @param parts インプット文字列の形態素解析結果
        @param mood  アップデート後の機嫌値
        """
        # インプット文字列の名詞の部分のみを格納するリスト
        keywords = []
        template = ''
        # 解析結果partsの「文字列」→word、「品詞情報」→partに順次格納
        for word, part in parts:
            # 名詞であるかをチェックしてkeywordsリストに格納
            if (keyword_check(part)):
                keywords.append(word)
        # keywordsリストに格納された名詞の数を取得
        count = len(keywords)
        # keywordsリストに1つ以上の名詞が存在し、
        # 名詞の数に対応するテンプレートが存在するかをチェック
        if (count > 0) and (str(count) in self.dictionary.template):
            # テンプレートリストから名詞の数に対応するテンプレートを
            # ランダムに抽出
            template = random.choice(self.dictionary.template[str(count)])

            for word in keywords:
                template = template.replace('%noun%', word, 1)

            return template
        return random.choice(self.dictionary.random)


class MarcovResponder(Responder):
    """ マルコフ連鎖を利用して応答を生成するためのサブクラス

    """

    def response(self, input, mood, parts):
        m = []  #
        # 解析結果の形態素と品詞に対して反復処理
        for word, part in parts:
            # print('word===',word)
            # print('part===',part)

            # インプット文字列に名詞があればそれを含むマルコフ連鎖文を検索
            if keyword_check(part):
                # マルコフ連鎖で生成した文章を1つずつ処理
                for sentence in self.dictionary.sentences:
                    # 形態素の文字列がマルコフ連鎖の文章に含まれているか検索する
                    # 最後を'.*?'にすると検索文字列だけにもマッチするので
                    # + '.*'として検索文字列だけにマッチしないようにする
                    find = '.*?' + word + '.*'
                    # マルコフ連鎖文にマッチさせる
                    tmp = re.findall(find, sentence)
                    if tmp:
                        # マッチする文章があればリストmに追加
                        m.append(tmp)
        # findall()はリストを返してくるので多重リストをフラットにする
        m = list(chain.from_iterable(m))
        # 集合に変換して重複した文章を取り除く
        check = set(m)
        # 再度、リストに戻す
        m = list(check)

        if m:
            # インプット文字列の名詞にマッチしたマルコフ連鎖文からランダムに選択
            return (random.choice(m))

        # マッチするマルコフ連鎖文がない場合
        return random.choice(self.dictionary.random)

class ConversationLearning:
    """ ピティナの本体クラス
    """

    def __init__(self, name, h_randomDict, h_patternDict, h_templateDict, h_passedSentence):    #updated
        """ Ptnaオブジェクトの名前をnameに格納
            応答オブジェクトをランダムに生成してresponderに格納

            @param name Ptnaオブジェクトの名前
        """
        self.name = name
        # Dictionaryを生成
        #updated start
        #self.dictionary = Dictionary()
        self.dictionary = Dictionary(h_randomDict, h_patternDict, h_templateDict, h_passedSentence)
        #updated end

        #updated start
        ## Emotionを生成
        self.emotion = Emotion(self.dictionary)
        #self.emotion = ""
        #updated end

        # RandomResponderを生成
        self.res_random = RandomResponder('Random', self.dictionary)
        # RepeatResponderを生成
        self.res_what = RepeatResponder('Repeat', self.dictionary)
        # PatternResponderを生成
        self.res_pattern = PatternResponder('Pattern', self.dictionary)
        # TemplateResponderを生成
        self.resp_template = TemplateResponder('Template', self.dictionary)
        # MarkovResponderを生成
        self.resp_markov = MarcovResponder('Markov', self.dictionary)

    def dialogue(self, input):
        """ 応答オブジェクトのresponse()を呼び出して
            応答文字列を取得する

            @param input ユーザーによって入力された文字列
            戻り値 応答文字列
        """
        #updated start
        ## 機嫌値を更新
        #self.emotion.update(input)
        #updated end
        # インプット文字列を解析
        parts = analyze(input)

        # 1から100をランダムに生成
        x = random.randint(1, 100)
        # 30以下ならPatternResponderオブジェクトにする
        if x <= 30:
            self.responder = self.res_pattern
        # 31～50以下ならTemplateResponderオブジェクトにする
        elif 31 <= x <= 50:
            self.responder = self.resp_template
        # 51～70以下ならRandomResponderオブジェクトにする
        elif 51 <= x <= 70:
            self.responder = self.res_random
        elif 71 <= x <= 90:
            self.responder = self.resp_markov
        # それ以外はRepeatResponderオブジェクトにする
        else:
            self.responder = self.res_what

        # 応答フレーズを生成
        resp = self.responder.response(input, self.emotion.mood, parts)  ####
        # 学習メソッドを呼ぶ
        # @param input インプット文字列
        # @param parts  インプット文字列の形態素
        self.dictionary.study(input, parts)
        # 応答フレーズを返す
        return resp

    def save(self):
        """ Dictionaryのsave()を呼ぶ中継メソッド
        """
        self.dictionary.save()

class Emotion:
    """ ピティナの感情モデル
    """
    # 機嫌値の上限／加減と回復値を設定
    MOOD_MIN = -15
    MOOD_MAX = 15
    MOOD_RECOVERY = 0.5

    def __init__(self, dictionary):
        """ Dictionaryオブジェクトをdictionaryに格納
            機嫌値moodを0で初期化

            @param dictionary Dictionaryオブジェクト
        """
        self.dictionary = dictionary
        # 機嫌値を保持するインスタンス変数
        self.mood = 0

    def update(self, input):
        """ ユーザーからの入力をパラメーターinputで受け取り
            パターン辞書にマッチさせて機嫌値を変動させる

            @param input ユーザーからの入力
        """
        # 機嫌を徐々にもとに戻す処理
        if self.mood < 0:
            self.mood += Emotion.MOOD_RECOVERY
        elif self.mood > 0:
            self.mood -= Emotion.MOOD_RECOVERY
        # パターン辞書の各行を繰り返しパターンマッチさせる
        for ptn_item in self.dictionary.pattern:
            # パターンマッチすればadjust_mood()で機嫌値を変動させる
            if ptn_item.match(input):
                self.adjust_mood(ptn_item.modify)
                break

    def adjust_mood(self, val):
        """ 機嫌値を増減させる

            @param val 機嫌変動値
        """
        # 機嫌値moodの値を機嫌変動値によって増減する
        self.mood += int(val)
        # MOOD_MAXとMOOD_MINと比較して、機嫌値が取り得る範囲に収める
        if self.mood > Emotion.MOOD_MAX:
            self.mood = Emotion.MOOD_MAX
        elif self.mood < Emotion.MOOD_MIN:
            self.mood = Emotion.MOOD_MIN

###############################################################################
# Mecab
###############################################################################
# Mecabによる分かち
def Scrap_Mecab_Wakati(h_wordlist, h_inFile, h_outFile):
    if (h_inFile != ""):
        a_f = open(h_inFile, "r", encoding="utf-8")
        # f = open("tweet.txt", "rb")
        h_wordlist = a_f.read()
        a_f.close()

    a_mt = MeCab.Tagger("-Owakati")

    a_wordlist = a_mt.parse(h_wordlist)

    if (h_outFile != ""):
        a_f = open(h_outFile, "w", encoding='utf-8')
        a_f.write(a_wordlist)
        a_f.flush()
        a_f.close()

    return a_wordlist

# マルコフ辞書作成
def Scrap_Mecab_Markov_Dict(h_wordlist, h_inFile):
    if (h_inFile != ""):
        a_f = open(h_inFile, "r", encoding="utf-8")
        h_wordlist = a_f.read()
        a_f.close()

    a_wordlist = h_wordlist.rstrip(" \n").split(" ")
    # print(wordlist)
    a_markov = {}
    a_w = ""

    for a_x in a_wordlist:
        if a_w:
            # print("w---> " + w)
            # if (markov.has_key(w)):
            if (a_w in a_markov):
                # print("w in markov")
                a_new_list = a_markov[a_w]
            else:
                # print("else2")
                a_new_list = []

            a_new_list.append(a_x)
            a_markov[a_w] = a_new_list

        a_w = a_x
        # print("w = x ---> " + w)

        # print("*** new_list ***")
        # print(new_list)
        # print("*** markov ***")
        # print(markov)

    return a_markov

# マルコフ連鎖による文章組み立て
def Scrap_Mecab_Markov_Chain(h_wordlist, h_dict, h_loop, h_reg):
    #ここでもsplitの処理が必要
    a_wordlist = h_wordlist.rstrip(" \n").split(" ")
    a_choice_words = a_wordlist[0]
    #print(a_choice_words)
    a_sentence = ""
    a_count = 0

    while a_count < h_loop:
        a_sentence += a_choice_words
        a_choice_words = random.choice(h_dict[a_choice_words])
        a_count += 1

        a_sentence = a_sentence.split(" ", 1)[0]
        #print("*** sentence")
        #print(a_sentence)
        a_p = re.compile(h_reg)
        a_sus = a_p.sub("", a_sentence)
        #print("*** sus")
        #print(a_sus)

    return a_sus

###############################################################################
# Janome
###############################################################################
# 形態素を取得
# .surface          分かち書き
# .part_of_speech   品詞
# .infl_form        活用形
# .infl_type        活用型
# .base_form        原型
# .reading          読み方
# .phonetic         発音
def Scrap_Janome_Parse(h_text, h_inFile, h_outFile):
    """ 形態素解析によって形態素を取り出す

        @param h_text マルコフ辞書のもとになるテキスト
        戻り値 形態素のリスト
    """
    if (h_inFile != ""):
        a_f = open(h_inFile, "r", encoding="utf-8")
        # f = open("tweet.txt", "rb")
        h_text = a_f.read()
        a_f.close()

    # 空白行が含まれていると\n\nが続くので\n1つにする
    h_text = re.sub('\n\n', '\n', h_text)
    # 文末の改行文字を取り除く
    h_text = re.sub("\n", "", h_text)

    a_t = Tokenizer()# Tokenizerオブジェクトを生成

    a_tokens = a_t.tokenize(h_text)# 形態素解析を実行
    a_result = []# 形態素を格納するリスト

    if (h_outFile != ""):
        a_f = open(h_outFile, "w", encoding='utf-8')

    for a_token in a_tokens:
        a_result.append(a_token.surface)
        if (h_outFile != ""):
            a_f.write(a_token.surface + "\n")
            a_f.flush()

    if (h_outFile != ""):
        a_f.close()

    return(a_result)

#マルコフ辞書を作成
def Scrap_Janome_Markov_Dict(h_wordlist, h_inFile):
    if (h_inFile != ""):
        a_f = open(h_inFile, "r", encoding="utf-8")
        h_wordlist = a_f.read()
        a_f.close()

    a_markov = {}
    a_p1 = ''
    a_p2 = ''
    a_p3 = ''

    for a_word in h_wordlist:
        # p1、p2、p3のすべてに値が格納されているか
        if a_p1 and a_p2 and a_p3:
            # markovに(p1, p2, p3)キーが存在するか
            if (a_p1, a_p2, a_p3) not in a_markov:
                # なければキー：値のペアを追加
                a_markov[(a_p1, a_p2, a_p3)] = []
            # キーのリストにサフィックスを追加（重複あり）
            a_markov[(a_p1, a_p2, a_p3)].append(a_word)
        # 3つのプレフィックスの値を置き換える
        a_p1, a_p2, a_p3 = a_p2, a_p3, a_word

    return  a_markov

#マルコフ文章を作成
def Scrap_Janome_Markov_Chain(h_wordlist, h_dict):
    a_sentence = ''

    """ マルコフ辞書から文章を作り出す
    """
    # markovのキーをランダムに抽出し、プレフィックス1～3に代入
    a_p1, a_p2, a_p3 = random.choice(list(h_dict.keys()))
    # 単語リストの単語の数だけ繰り返す
    a_count = 0
    while a_count < len(h_wordlist):
        # キーが存在するかチェック
        if ((a_p1, a_p2, a_p3) in h_dict) == True:
            # 文章にする単語を取得
            a_tmp = random.choice(h_dict[(a_p1, a_p2, a_p3)])
            # 取得した単語をsentenceに追加
            a_sentence += a_tmp
        # 3つのプレフィックスの値を置き換える
        a_p1, a_p2, a_p3 = a_p2, a_p3, a_tmp
        a_count += 1

    # 最初に出てくる句点(。)までを取り除く
    a_sentence = re.sub('^.+?。', '', a_sentence)
    # 最後の句点(。)から先を取り除く
    if re.search('.+。', a_sentence):
        a_sentence = re.search('.+。', a_sentence).group()
    # 閉じ括弧を削除
    a_sentence = re.sub('」', '', a_sentence)
    # 開き括弧を削除
    a_sentence = re.sub('「', '', a_sentence)
    # 全角スペースを削除
    a_sentence = re.sub('　', '', a_sentence)

    return a_sentence

#マルコフ文章から重複を取り除く
def Scrap_Janome_Markov_Overlap(h_sentence):
    """ 重複した文章を取り除く
    """
    a_sentence = h_sentence.split('。')
    if '' in a_sentence:
        a_sentence.remove('')
    a_new = []
    for a_str in a_sentence:
        a_str = a_str + '。'
        if a_str=='。':
            break
        a_new.append(a_str)
    a_new = set(a_new)
    a_sentence=''.join(a_new)

    return a_sentence

###############################################################################
# 演算
###############################################################################
def Scrap_Cosine_Similarity(h_v1, h_v2):
    """
    ベクトルv1, v2のcos類似度の算出
    cos類似度はベクトルの内積をベクトル間の類似度の指標に用いる手法で、0~1の値を取ります。
    値は1に近づくほどベクトル同士が類似しており、0に近づくほど類似していないです。
    """
    return sum([a*b for a, b in zip(h_v1, h_v2)])/(sum(map(lambda x: x*x, h_v1))**0.5 * sum(map(lambda x: x*x, h_v2))**0.5)

def Scrap_Tf(h_terms, h_document):
    """
    TF値の計算。単語リストと文章を渡す
    TFはTerm Frequency、単語の出現頻度
    :param h_terms:
    :param h_document:
    :return:
    """
    a_tf_values = [h_document.count(a_term) for a_term in h_terms]
    return list(map(lambda x: x/sum(a_tf_values), a_tf_values))

def Scrap_Idf(h_terms, h_documents):
    """
    IDF値の計算。単語リストと全文章を渡す
    IIDF は Inverse Document Frequency、逆文書頻度（これが希少性）
    :param h_terms:
    :param h_documents:
    :return:
    """
    import math
    return [math.log10(len(h_documents)/sum([bool(a_term in a_document) for a_document in h_documents])) for a_term in h_terms]

def Scrap_Tf_Idf(h_terms, h_documents):
    """
    TF-IDF値を計算。文章毎にTF-IDF値を計算
    http://ailaby.com/tfidf/
    :param h_terms:
    :param h_documents:
    :return:
    """
    return [[_tf*_idf for _tf, _idf in zip(Scrap_Tf(h_terms, a_document), Scrap_Idf(h_terms, h_documents))] for a_document in h_documents]
