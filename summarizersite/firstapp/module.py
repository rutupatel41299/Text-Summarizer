import spacy
import string
from collections import Counter
from spacy.lang.en.stop_words import STOP_WORDS
nlp = spacy.load("en_core_web_lg")

# handeling uploaded PDF file for the summary generation
def handle_uploaded_file(f):
    with open('C:/Users/rutup/PycharmProjects/final_summarizer_project/summarizersite/files/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return 'C:/Users/rutup/PycharmProjects/final_summarizer_project/summarizersite/files/name.txt'

# processed data for fetching unique words
def natural_language_processing(data):
    # removing punctuations and new lines and tabs
    pun = string.punctuation + '\t' + '—' + '‘’' + '\n' + '\r' + '\r\n' + '\v' + '\x0b' + '\f' + '\x0c' + '\x1c' + '\x1d' + '\x1e' + '\x85' + '\u2028' + '\u2029'
    for sym in pun:
        cnt = data.count(sym)
        data = data.replace(sym, '', cnt)

    # lower the data
    data = data.lower()

    doc = nlp(data)
    print('processed data: ', doc)
    return doc

# stopping and stemming of data which came from natural_language_processing()
def stopstem(doc):
    # stopping and stemming
    filtered_tokens = []
    for token in doc:
        if not token.is_stop:
            filtered_tokens.append(token.lemma_)

    res = []
    for ele in filtered_tokens:
        if ele.strip():
            res.append(ele)

    filtered_tokens = res

    print('list of tokens after stopping and stemming: ', filtered_tokens)
    print()

    text_stopped = ' '.join(filtered_tokens)
    doc_stopped = nlp(text_stopped)
    print('stemmed and stopped document: ', doc_stopped)
    print()
    return filtered_tokens, doc_stopped