import numpy as np
import pymystem3
import gensim
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import os


def prepare_group(mypath):
    files = []
    stem = pymystem3.Mystem()

    for r, d, f in os.walk(mypath):
        for file in f:
            files.append(os.path.join(r, file))

    docs = []
    full = ''
    wordset = set()

    for filepath in files:
        corpus = []
        with open(filepath) as file:
            for line in file:
                corpus.append(line)
        corpus = [el for el in corpus if el != '\n']

        corpus = [re.sub(r'[^\w\s]', '', el)[:-1] for el in corpus]

        for el in corpus:
            words = el.lower()
            proc = stem.lemmatize(words)
            proc = [w for w in proc if (w.strip() != '') and (w != '\n')]
            docs.append(proc)

            for word in proc:
                full += ' ' + word
                wordset.add(word)
        print(filepath)

    return docs, wordset, full


def make_tfidf(fulls):
    vec = TfidfVectorizer()
    tfidf = vec.fit_transform(fulls)
    npidf = tfidf.toarray()
    fnames = vec.get_feature_names()
    return  npidf, fnames


def choose_by_tfidf(fnames, tfidf, word, coef=2):
    try:
        index = fnames.index(word)
        idf = tfidf[:, index]
        return idf[1] > coef * idf[0]
    except:
        return False


def select_by_cos(word, sets, model, tfidf, fnames, coef):
    best = '0'
    best_res = -100
    for gword in sets[0]:
        try:
            score = model.wv.similarity(word, gword)
            if score > best_res:
                bad = choose_by_tfidf(fnames, tfidf, gword, coef)
                if not bad:
                    best_res = score
                    best = gword
        except:
            pass
    return best, best_res


def part_production(string, model, sets, fnames, tfidf, coef):
    start = string.split()
    res = []
    stem = pymystem3.Mystem()
    proc = stem.lemmatize(string)
    corpus = [re.sub(r'[^\w\s]', '', el) for el in proc]
    corpus = [el for el in corpus if el.strip() != '']

    for i, word in enumerate(corpus):
        if choose_by_tfidf(fnames, tfidf, word):
            chose, pos = select_by_cos(word, sets, model, tfidf, fnames, coef)
            res.append([word, chose, i])
    return res


def pipeline(wor=4):
    docs_c, wordset_c, full_c = prepare_group('./books/classic')
    docs_t, wordset_t, full_t = prepare_group('./books/trash')

    texts = docs_c + docs_t
    fulls = [full_c, full_t]
    sets = [wordset_c, wordset_t]

    model = gensim.models.Word2Vec(texts, size=100, iter=10, workers=wor, min_count=2, window=5, sg=0, hs=1,
                                   negative=2, cbow_mean=1)
    npidf, fnames = make_tfidf(fulls)
    return docs_c, wordset_c, full_c, docs_t, wordset_t, full_t, texts, fulls, sets, model, npidf, fnames


def one_word_production(word, model, sets, fnames, tfidf, coef):
    primal = word
    stem = pymystem3.Mystem()
    proc = stem.lemmatize(word)[0]
    word = proc.strip()
    if word == '':
        return 0, primal
    if choose_by_tfidf(fnames, tfidf, word):
        chose, pos = select_by_cos(word, sets, model, tfidf, fnames, coef)
        return 1, chose
    else:
        return 0, primal

def production(string, model, sets, fnames, tfidf, coef):
    final = []
    for word in string.split():
        num, choice = one_word_production(word, model, sets, fnames, tfidf, coef)
        final.append((num, choice))
    return final