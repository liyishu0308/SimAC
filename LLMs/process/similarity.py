import spacy
import torch
from sklearn.metrics.pairwise import cosine_similarity

def checkSimilarity(sen1,sen2):
    nlp = spacy.load("en_core_web_lg")

    doc1 = nlp(sen1)
    doc2 = nlp(sen2)
    score = doc1.similarity(doc2)

    return score