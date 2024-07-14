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

# generation of part of speech tagging dictionary with word frequency on the basis of data from stopstem()
def pos_counting(filtered_tokens, doc_stopped):
    word_freq = dict()
    for token in filtered_tokens:
        word_freq[token] = word_freq.get(token, 0) + 1

    pos_dict = dict()
    for token in doc_stopped:
        if token.pos_ in pos_dict:
            pos_dict[token.pos_][token.text] = word_freq[token.text]
        else:
            pos_dict[token.pos_] = dict()
            pos_dict[token.pos_][token.text] = word_freq[token.text]
    print('part of speech dictionary:', pos_dict)
    return pos_dict

# processing of actual data again for generating list of sentences for generating summary
def sentence_list(data1):
    pun = '\t' + '!"#$%&' + '()*+,-/:;<=>?@[\]^_`{|}~—' + '‘’' + '\n' + '\r' + '\r\n' + '\v' + '\x0b' + '\f' + '\x0c' + '\x1c' + '\x1d' + '\x1e' + '\x85' + '\u2028' + '\u2029'
    for sym in pun:
        cnt = data1.count(sym)
        data1 = data1.replace(sym, '', cnt)

    doc1 = nlp(data1)
    sentences = list(doc1.sents)

    for s in sentences:
        print(s)
    return sentences

# fetching unique words from part of speech tagging dictionary on the basis of sentences in actual data
def unique_word_fetch(doc_length, pos_dict):
    # threshold selection
    threshold = 0
    if doc_length >= 3 and doc_length <= 7:
        threshold = 2
    elif doc_length >= 8 and doc_length <= 15:
        threshold = 4
    elif doc_length >= 16 and doc_length <= 22:
        threshold = 6
    elif doc_length >= 22 and doc_length <= 30:
        threshold = 8
    elif doc_length >= 30:
        threshold = 10

    considered_pos = ['ADV', 'CONJ', 'NOUN', 'PRON', 'PROPN', 'X']

    unique_words = list()

    if threshold == 0:
        return unique_words

    for posn in pos_dict:
        if posn in considered_pos:
            for word in pos_dict[posn]:
                if pos_dict[posn][word] >= threshold:  # how to select that threshold is a problem
                    unique_words.append(word)
    print('unique words: ', unique_words)
    return unique_words

# generating summary based on unique words from unique_word_fetch() and sentences from sentence_list()
def summary_generation(sentences, unique_words):
    summary = list()
    keyword_count = dict()
    ind = 0
    for sen in sentences:
        sent = str(sen)
        sent_lower = sent.lower()
        flag = 0
        cnt = 0
        for word in unique_words:
            if word in sent_lower:
                cnt = cnt + 1
            if word in sent_lower and flag == 0:
                flag = flag + 1
                summary.append(sent)
        if cnt != 0:
            keyword_count[ind] = cnt
            ind = ind + 1
    print(keyword_count)

    for s in summary:
        print(s)
    print('length of summary', len(summary))
    return summary, keyword_count