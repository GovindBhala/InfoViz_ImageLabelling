# InfoViz_ImageLabelling

Image search has traditionally been matching multiple labels tagged to an image which although is very fast and accurate way of searching images but sometimes, keyword based search loses context and deeper meaning provided in a search query. This project aims for a better labelling technique with a corresponding search mechanism to get accurate search results.
For labelling technique, we generated descriptions of the images using Neural Network. The image is encoded using VGG-16 which is a Convolution neural net architecture which was used to win Imagenet competition in 2014. It has 16 weighted layers and the interesting thing about the model is that instead of having large number of hyper para meter it has convolution layers of 3*3 filter with stride 1 and max pool layer of 2*2 filter of stride 2 consistently throughout the architecture. At the end it has 2 dense layers followed by a SoftMax for the classification results. 

![Image of vgg16](https://github.com/GovindBhala/InfoViz_ImageLabelling/blob/master/vgg16.png)

Since we want the encoded features of the image and not the classification results, the last softmax layer is not used. Instead, we take the output of the last Max pool layer that is before flattening the image, to generate the feature vectors of the images. This encoded image vector is stored as a NumPy file which is considered the output of the encoder.
VGG16 application is used to preprocess the image and since, it accepts images with certain dimensions, all the images are resized to 224 by 224 with 3 channels.
This encoded image along with the text for training is passed on to Lstm based RNN decoder which trains the model to generate the text describing the image. The following architecture is from the *add research paper called show and tell link*

![Image of showandtell](https://github.com/GovindBhala/InfoViz_ImageLabelling/blob/master/show%20and%20tell%20architecture.png)


*** LSTM/GRU ***

For the search mechanism, Natural Language Processing is used to calculate the text similarity between the user query and the stored label texts and map the corresponding images for search engine results.
Universal Sentence Encoder (USE) is used to encode the image descriptions and the search query. 
USE encodes text into high-dimensional vectors that can be used for text classification, semantic similarity, clustering and other natural language tasks.
It is a pre-trained model that is optimized for greater-than-word length text, such as sentences, phrases or short paragraphs. It is trained on a variety of data sources and a variety of tasks with the aim of dynamically accommodating a wide variety of natural language understanding tasks. The input is variable length English text and it returns 512-dimensional vector as an output.
The encoded image descriptions are stored as a pickle file which is updated with every new image added to data. To measure the text similarity between the query and image labels, Word Mover’s distance is used; which measures the dissimilarity between two text documents as the minimum amount of distance that the embedded words of one document need to “travel” to reach the embedded words of another document.
Taking 50 most similar image labels based on WMD, we apply TFIDF and Document to Bag of Words to find the image descriptions most similar to the query. This is done because WMD mainly gives results based on the semantic similarity; So, once we get the most semantically similar results, we use Doc2BOW and TFIDF which will fetch syntactically similar results.


