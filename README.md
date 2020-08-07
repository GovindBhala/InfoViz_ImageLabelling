# Infomation Vizualization                             
<p align="right">Govind Bhala and Heer Sanjay Patel </p>

### <ins>Better Image Labeling using neural image captioning</ins>

* [Description](#description)
* [Dataset](#dataset)
* [Image Labelling](#image-labeling)
* [Image Searching](#image-searching)
* [Project Setup](#project-setup)
* [API Structure](#api-structure)

#### Description

Image search has traditionally been matching multiple labels tagged to an image which although is very fast but sometimes, keyword based search loses context and deeper meaning provided in a search query. This project aims for a better labelling technique with a corresponding search mechanism to get accurate contextual and symentically correct search results.


#### Dataset

The dataset is taken from [MS COCO](https://cocodataset.org/#download). 
It consists 118,292 images and 591,753 corresponding captions. The data was split into training and testing with 80% and 20% ratio. The captions associated with these images are filtered and tokenized using a vocabulary of most frequent 25,000 words.


#### Image Labeling

For labeling the images, we generated a sentence long descriptions for a given image using Deep Sequence Neural Network through an encoder - decoder architecture, where image is encoded via a CNN and the decoder which is a RNN is trained to generate sentences on the encoded image input. For encoder, we have used a pre-trained model VGG-16 which is a Convolution neural net responsible for winning Imagenet competition in 2014.<br/> It has 16 weighted layers and has convolution layers of 3\*3 filter with stride 1 and max pool layer of 2\*2 filter of stride 2 consistently throughout the architecture. At the end it has 2 dense layers followed by a SoftMax layer for generating classification results. 

![Image of vgg16](https://github.com/GovindBhala/InfoViz_ImageLabelling/blob/master/images/vgg16.png)

Since we want the encoded features of the image and not the classification results, we extract our encoded output from the last Max pool layer, that is before flattening the image. This encoded image vector is stored as a NumPy file which is considered the output of the encoder.

VGG16 application is used to preprocess the image and since, it accepts images with certain dimensions, all the images are resized to 224 by 224 with 3 channels.
This encoded image along with the text for training is passed on to RNN decoder which trains the model to generate the text describing the image. The following architecture is from [Show attend and tell](https://arxiv.org/pdf/1502.03044.pdf)

![Image of showandtell](https://github.com/GovindBhala/InfoViz_ImageLabelling/blob/master/images/show%20and%20tell%20architecture.png)


#### Image Searching

For the search mechanism, Natural Language Processing is used to calculate the text similarity between the user query and the stored label texts. Once we have the top similar results we can extract the corrosponding image associated with the label, thus forming our seach engine.<br/>
To get sentence similarity, [Universal Sentence Encoder](https://tfhub.dev/google/universal-sentence-encoder/4) (USE) is used to first vectorize the image descriptions and the search query. 
USE encodes text into high-dimensional vectors that can be used for text classification, semantic similarity, clustering and other natural language tasks.
It is a pre-trained model that is optimized for greater-than-word length text, such as sentences, phrases or short paragraphs. It is trained on a variety of data sources and a variety of tasks with the aim of dynamically accommodating a wide variety of natural language understanding tasks. The input is variable length English text and it returns 512-dimensional vector as an output.<br/>

The next step in this process is to find the most similar vectors in the image labels to the vector generated from user's input query.
To measure the text similarity between the query and image labels, Word Mover’s distance is used; which measures the dissimilarity between two text as the minimum amount of euclidean distance that the embedded words of one document need to “travel” to reach the embedded words of another document. <br/>
To speed up the process of sentence matching, image descriptions are pre-encoded and stored in a vector form as a pickle file which is updated with every new image added to data. 

Taking 50 most similar image labels based on WMD, we apply TFIDF and Document to Bag of Words using [Gensim](https://pypi.org/project/gensim/) library to find the image descriptions most similar to the query. This is done because WMD mainly gives results based on the semantic similarity; so once we get the most semantically similar results, we use Doc2BOW and TFIDF which will fetch syntactically similar results.
The most similar descriptions are mapped to it's corresponding images to return the final image results to the user.

![Image of vgg16](https://github.com/GovindBhala/InfoViz_ImageLabelling/blob/master/images/NLP%20flowchart.png)


#### Project Setup
* Notebooks : Contains notebooks used for training image caption generation model
  - GRU.ipynb : Notebook for training GRU model
  - LSTM.ipynb : Notebook for training LSTM model
* UI Components : Contains all files necessary to run the UI
* module : Contains the script version of model training notebooks, such that they can be used in the server code
  - GRU_model.py : Script for loading and predicting on GRU model
  - LSTM_model.py : Script for loading and predicting on LSTM model
  - tokenizer.pickle : pickle file which contains tokenized captions, saved while training
 * CaptionGenerationServer.py : Flask application for hosting Caption Generation server
 * SearchOnQueryServer.py : Flask application for hosting searching for images based on user query server
 
 For training the model, use the training notebooks.<br />
 For hosting the servers, exectue the flask applications <br />
 For running UI application, please follow instructions in UI Components folder's README
 All trained models along with the embeddings calculated on training captions can be found uploaded in Google Drive here
 
#### API Structure
