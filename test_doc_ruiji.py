import mct_scrap
from sklearn.feature_extraction.text import TfidfVectorizer

def _cosine_(h_tf_idfs, h_index, h_max):
    for a_i in range(h_index, h_max - 1):
        print(mct_scrap.Scrap_Cosine_Similarity(h_tf_idfs[h_index], h_tf_idfs[a_i + 1]))
        _cosine_(h_tf_idfs, a_i + 1, h_max)

if __name__ == '__main__':
    # 単語リスト
    _terms = ["リンゴ", "ゴリラ", "ラッパ"]
    # 文章リスト
    _documents = ["リンゴ、リンゴ", "リンゴとゴリラ", "ゴリラとラッパ"]

    tf_idfs = mct_scrap.Scrap_Tf_Idf(_terms, _documents)
    #print(len(tf_idfs))
    #print(tf_idfs[0])
    #print(tf_idfs[1])
    #print(tf_idfs[2])

    # 文章0と文章1の類似度
    _cosine_(tf_idfs, 0, len(tf_idfs))

    """
    # 文章0と文章1の類似度
    print(mct_scrap.Scrap_Cosine_Similarity(tf_idfs[0], tf_idfs[1]))
    # 文章0と文章2の類似度
    print(mct_scrap.Scrap_Cosine_Similarity(tf_idfs[0], tf_idfs[2]))
    # 文章1と文章2の類似度
    print(mct_scrap.Scrap_Cosine_Similarity(tf_idfs[1], tf_idfs[2]))
    """

    """
    #
    # ベクトル化
    #
    vectorizer = TfidfVectorizer(use_idf=True, token_pattern=u'(?u)\\b\\w+\\b')
    vecs_terms = vectorizer.fit_transform(_terms)
    print(vecs_terms.toarray())
    vecs_documents = vectorizer.fit_transform(_documents)
    print(vecs_documents.toarray())

    print(mct_scrap.Scrap_Cosine_Similarity(vecs_terms, vecs_documents))
    """
