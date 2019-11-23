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


def make_tfidf():
    vec = TfidfVectorizer()
    tfidf = vec.fit_transform(fulls)
    npidf = tfidf.toarray()
    fnames = vec.get_feature_names()
    return  npidf, fnames


def choose_by_tfidf(fnames, tfidf, word):
    try:
        index = fnames.index(word)
        idf = npidf[:, index]
        return idf[1] > 100 * idf[0]
    except:
        return False

def select_by_cos(word, sets, model):
    best = '0'
    best_res = -100
    for gword in sets[0]:
        score = model.wv.similarity(word, gword)
        if score > best_res:
            best_res = score
            best = gword
    return best, best_res


def production(string, model, texts, fulls, sets, fnames, tfidf):
    res = []
    stem = pymystem3.Mystem()
    proc = stem.lemmatize(string)
    corpus = [re.sub(r'[^\w\s]', '', el) for el in proc]
    corpus = [el for el in corpus if el.strip() != '']

    for word in corpus:
        if choose_by_tfidf(fnames, tfidf, word):
            chose, pos = select_by_cos(word, sets, model)
            res.append([word, chose, pos])
    return res