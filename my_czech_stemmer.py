def manual_stemmer(docs_collection: dict):
    print("manual stemmer...")
    for docno in docs_collection:
        for i, term in enumerate(docs_collection[docno]):
            tl = len(term)
            # stop_words_set = set(CZ_LOW_IDF_500)
            # if term not in stop_words_set:
            if tl == 4:
                rt = term[:-1]
            if tl == 5:
                rt = term[:-1]
            elif tl == 6:
                rt = term[:-1]
            elif tl == 7:
                rt = term[:-2]
            elif tl == 8:
                rt = term[:-2]
            elif tl == 9:
                rt = term[:-2]
            elif tl == 10:
                rt = term[:-2]
            elif tl == 11:
                rt = term[:-3]
            elif tl > 11:
                rt = term[:-3]
            else:
                rt = term
            docs_collection[docno][i] = rt
    return docs_collection
