import os
import flask
import numpy as np
#import tensorflow as tf
#import tensorflow.keras as keras
from flask import session, url_for, jsonify, request
from flask_cors import CORS

import json
import jieba
import pickle
import tensorflow_hub as hub
from gensim import corpora, models, similarities

module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(module_url)

embeddings = pickle.load(open("embeddings", "rb"))

#sample_path = 'C:\\Users\\Govind\\SML\\Project\\app_uploaded_files\\picture.jpg'
#sample_path = "C:\\Users\\Govind\SML\\Project\\train2017\\train2017"
sample_path = "..\\000000000009.jpg"

caption_file = "annotations_trainval2017\\annotations\\captions_train2017.json"

with open(caption_file) as caption_json:
    captions_data=json.load(caption_json)

image_captions=[]
image_name_location=[]
for caption in captions_data['annotations']:
    image_caption = caption['caption'] 
    image_captions.append(image_caption)
    image_location = "http://localhost/train2017/"+ str(f"{caption['image_id']:012d}")+'.jpg'
    image_name_location.append(image_location)

documents = image_captions
image_dict = dict(zip(image_captions, image_name_location))

print ("module %s loaded" % module_url)
def embed(input):
    return model(input)

def WMD(query, embeddings):
    sen1 = embed([query])
    embd = np.repeat(sen1, len(embeddings), axis = 0)
    return np.linalg.norm(embd-embeddings, axis = 1)


def find_similar_sentences(query, embeddings, documents):
    results = {}
    wmdistance = WMD(query,embeddings)
    Z = [x for _,x in sorted(zip(wmdistance,documents))]
    print("Univ results : \n")
    results['Univ Results'] = [{'path' : sample_path, 'caption' : value} for value in Z[:10]]
    print(*Z[:10],sep='\n')
    texts = Z[:50]
    keyword = query
    texts = [jieba.lcut(text) for text in texts]
    dictionary = corpora.Dictionary(texts)
    feature_cnt = len(dictionary.token2id)
    corpus = [dictionary.doc2bow(text) for text in texts]
    tfidf = models.TfidfModel(corpus)
    kw_vector = dictionary.doc2bow(jieba.lcut(keyword))
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features = feature_cnt)
    sim = index[tfidf[kw_vector]]
    Y = [x for _,x in sorted(zip(sim,Z), reverse=True)]
    results['doc2bow'] = [{'path' : image_dict[value], 'caption' : value} for value in Y[:9]]
    print("\n\nFiltered with doc2bow\n")
    print(*Y[:10],sep='\n')
    return [{'path' : image_dict[value], 'caption' : value} for value in Y[:9]]

app = flask.Flask(__name__)
app.config["DEBUG"] = True

sample_path = "./logo192.png" ## CHANGE HERE

@app.route('/get-search-result', methods = ['GET'])
def get_images_from_query():
    search_query = request.args['query']
    #Y = ['This is a man', 'This is a man', 'This is a man', 'This is a man', 'This is a man', 'This is a man', 'This is a man', 'This is a man', 'This is a man']
    
    #results = [{'path' : sample_path, 'caption' : value} for value in Y] #find_similar_sentences(search_query,embeddings, documents)
    results = find_similar_sentences(search_query, embeddings, documents)
    response = jsonify(results)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5010)