import pandas as pd
import czech_stemmer
import pyterrier as pt


def save_results_to_file(res: pd.DataFrame, run_no: str, file_name: str):
    print("results saving...")
    res_to_save = res.copy()
    res_to_save.rename(columns={'docid': 'iter', 'query': 'runid'}, inplace=True)
    res_to_save['iter'] = 0
    res_to_save['runid'] = run_no
    res_to_save.to_csv(file_name, sep=' ', index=False, header=False)


def cz_stemmer(docs: dict):
    print("apply stemmer...")
    lenght = len(docs)
    for k, docno in enumerate(docs):
        if k % 10000 == 0:
            print(k, "of", lenght, "docs")
        for i, term in enumerate(docs[docno]):
            docs[docno][i] = czech_stemmer.cz_stem_word(term)
    return docs


def evaluate(res, path_to_qrels):
    qrels = pd.read_csv(path_to_qrels, sep=" ", header=None, dtype={2: str})
    qrels.columns = ['qid', 'iter', 'docno', 'label']
    qrels.drop('iter', axis=1, inplace=True)

    eval = pt.Evaluate(res, qrels, metrics=["map", "P_10"], perquery=True)
    print("eval per query:", eval)
    eval = pt.Evaluate(res, qrels, metrics=["map", "P_10"])
    print("eval total:", eval)