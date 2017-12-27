from libmct import mct_scrap

if __name__ == '__main__':
    #a_wordlist = mct_scrap.Scrap_Janome_Parse("", "text.txt", "janome_parse.txt")
    a_wordlist = mct_scrap.Scrap_Janome_Parse("", "大相撲.html", "janome_parse.txt")
    a_markov = mct_scrap.Scrap_Janome_Markov_Dict(a_wordlist, "")
    print(a_markov)
    print('\n')
    a_sentence = mct_scrap.Scrap_Janome_Markov_Chain(a_wordlist, a_markov)
    print(a_sentence)
    print('\n')
    a_sentence = mct_scrap.Scrap_Janome_Markov_Overlap(a_sentence)
    print(a_sentence)
    print('\n')
