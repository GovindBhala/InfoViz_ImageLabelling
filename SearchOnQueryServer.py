import os
import flask
import numpy as np
from flask import session, url_for, jsonify, request
from flask_cors import CORS
import json
import jieba
import pickle
import tensorflow_hub as hub
from gensim import corpora, models, similarities

## Download Universal-sentence-encoder model
module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(module_url)

## Load pre-calculated sentece embeddings from cache
## This file can be downloaded from Google Drive link shared in read me
embeddings = pickle.load(open("embeddings", "rb"))

## Location of the captions file downloaded from MS COCO dataset
caption_file = "annotations_trainval2017\\annotations\\captions_train2017.json"

with open(caption_file) as caption_json:
    captions_data=json.load(caption_json)

image_captions=[]
image_name_location=[]
for caption in captions_data['annotations']:
    image_caption = caption['caption'] 
    image_captions.append(image_caption)
    image_location = "http://localhost/train2017/"+ str(f"{caption['image_id']:012d}")+'.jpg'  ## All images in the train set are hosted on 80 port for it to be accessible for UI
    image_name_location.append(image_location)

documents = image_captions
image_dict = dict(zip(image_captions, image_name_location))

print ("module %s loaded" % module_url)
def embed(input):
    return model(input)

def WMD(query, embeddings):
    """
    Calculate WMD of input user query against pre-calculated embeddings"
    """
    sen1 = embed([query])
    embd = np.repeat(sen1, len(embeddings), axis = 0)
    return np.linalg.norm(embd-embeddings, axis = 1)


def find_similar_sentences(query, embeddings, documents):
    wmdistance = WMD(query,embeddings)
    ## Get WMD results over all captions
    Z = [x for _,x in sorted(zip(wmdistance,documents))]

    print("Univ results : \n")
    print(*Z[:10],sep='\n') # Print top 10 results
    
    ## Take top 50 results and calculate doc2bag of words similarity over it
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
    print("\n\nFiltered with doc2bow\n")
    print(*Y[:10],sep='\n')
    ## return top 9 results as the API response
    return [{'path' : image_dict[value], 'caption' : value} for value in Y[:9]]

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/get-search-result', methods = ['GET'])
def get_images_from_query():
    """
    This function recieves GET request with user query as input.
    It fetches results from find_similar_sentences function and returns that as response
    Sample request API : http://localhost:5010/get-search-result
    """
    
    search_query = request.args['query']
    results = find_similar_sentences(search_query, embeddings, documents)
    response = jsonify(results)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5010)