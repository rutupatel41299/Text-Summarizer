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