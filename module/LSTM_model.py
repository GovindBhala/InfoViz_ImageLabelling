import pickle
import numpy as np
import tensorflow as tf
import tensorflow.keras as keras

vocabulary_size = 25000

with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

model_encoder = keras.applications.VGG16(include_top=False, weights='imagenet')
encoded_image_features = keras.Model(model_encoder.input, model_encoder.layers[-1].output)


def preprocess_image(image_location):
    image = tf.io.read_file(image_location)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, (224, 224))
    image = keras.applications.vgg16.preprocess_input(image)

    return image, image_location


def encode_images(train_images):
    encode_train = []
    for image_path in train_images:
        if (os.path.exists(image_path + '.npy') == False):
            encode_train.append(image_path)

    encode_train = sorted(set(encode_train))
    encoded_image = tf.data.Dataset.from_tensor_slices(encode_train)
    encoded_image = encoded_image.map(preprocess_image, num_parallel_calls=tf.data.experimental.AUTOTUNE).batch(16)

    for image, path in (encoded_image):
        batch_image_features = encoded_image_features(image)
        batch_image_features = tf.reshape(batch_image_features,
                                          (batch_image_features.shape[0], -1, batch_image_features.shape[3]))

        for bf, p in zip(batch_image_features, path):
            path_of_feature = p.numpy().decode("utf-8")
            # print(path_of_feature+'.npy')
            if (os.path.exists(path_of_feature + '.npy') == False):
                # print('2'+path_of_feature)
                np.save(path_of_feature, bf.numpy())


max_caption_length = 264


def evaluate(image):
    attention_plot = np.zeros((max_caption_length, attention_dim))

    hidden = Text_decoder.reset_state(batch_size=1)

    temp_input = tf.expand_dims(preprocess_image(image)[0], 0)
    img_tensor_val = encoded_image_features(temp_input)
    img_tensor_val = tf.reshape(img_tensor_val, (img_tensor_val.shape[0], -1, img_tensor_val.shape[3]))

    features = Image_encoder(img_tensor_val)

    dec_input = tf.expand_dims([tokenizer.word_index['<start>']], 0)
    result = []

    for i in range(max_caption_length):
        predictions, hidden, attention_weights = Text_decoder(dec_input, features, hidden)

        attention_plot[i] = tf.reshape(attention_weights, (-1,)).numpy()

        predicted_id = tf.argmax(predictions[0]).numpy()
        result.append(tokenizer.index_word[predicted_id])

        if tokenizer.index_word[predicted_id] == '<end>':
            return result, attention_plot

        dec_input = tf.expand_dims([predicted_id], 0)

    attention_plot = attention_plot[:len(result), :]
    return result, attention_plot


def load_image_features(image_name, caption):
    image_tensor = np.load(image_name.decode('utf-8') + '.npy')
    return image_tensor, caption


class BahdanauAttention(tf.keras.Model):
    def __init__(self, units):
        super(BahdanauAttention, self).__init__()
        self.W1 = tf.keras.layers.Dense(units)
        self.W2 = tf.keras.layers.Dense(units)
        self.V = tf.keras.layers.Dense(1)

    def call(self, features, hidden):
        # features(CNN_encoder output) shape == (batch_size, 64, embedding_dim)

        # hidden shape == (batch_size, hidden_size)
        # hidden_with_time_axis shape == (batch_size, 1, hidden_size)
        hidden_with_time_axis = tf.expand_dims(hidden, 1)

        # score shape == (batch_size, 64, hidden_size)
        score = tf.nn.tanh(self.W1(features) + self.W2(hidden_with_time_axis))

        # attention_weights shape == (batch_size, 64, 1)
        # you get 1 at the last axis because you are applying score to self.V
        attention_weights = tf.nn.softmax(self.V(score), axis=1)

        # context_vector shape after sum == (batch_size, hidden_size)
        context_vector = attention_weights * features
        context_vector = tf.reduce_sum(context_vector, axis=1)

        return context_vector, attention_weights


class Encoder(keras.Model):

    def __init__(self, EMBEDDING_DIM):
        super(Encoder, self).__init__()
        self.dense_fc = keras.layers.Dense(EMBEDDING_DIM)  # Shape=(batch_size, 49 , embedding_dim)

    def call(self, input_dim):
        return (tf.nn.relu(self.dense_fc(input_dim)))


class Decoder(keras.Model):

    def __init__(self, embedding_dim, units, vocab_size):
        super(Decoder, self).__init__()
        self.units = units
        self.attention = BahdanauAttention(self.units)
        self.embedding = keras.layers.Embedding(vocab_size, embedding_dim)
        self.lstm = keras.layers.LSTM(self.units, return_sequences=True, return_state=True,
                                      recurrent_initializer='glorot_uniform', recurrent_dropout=0.3)
        self.dropout1 = keras.layers.Dropout(rate=0.25)
        self.dropout2 = keras.layers.Dropout(rate=0.25)

        self.fc1 = keras.layers.Dense(self.units)
        self.fc2 = keras.layers.Dense(vocab_size)

    def call(self, input_vec, features, state_hidden):
        context_vector, attention_weights = self.attention(features, state_hidden)
        input_vec = self.embedding(input_vec)
        input_vec = tf.concat([tf.expand_dims(context_vector, 1), input_vec], axis=-1)
        input_vec = self.dropout1(input_vec)
        output, state_hidden, state_cell = self.lstm(input_vec)
        output = self.dropout2(output)
        input_vec = self.fc1(output)
        input_vec = tf.reshape(input_vec, (-1, input_vec.shape[2]))
        input_vec = self.fc2(input_vec)
        return input_vec, state_hidden, attention_weights

    def reset_state(self, batch_size):
        return tf.zeros((batch_size, self.units))


BATCH_SIZE = 64
BUFFER_SIZE = 1000
EMBEDDING_DIM = 256
units = 512
vocab_size = len(tokenizer.word_index) + 1
attention_dim = 49
channel_dim = 512

Image_encoder = Encoder(EMBEDDING_DIM)
Text_decoder = Decoder(EMBEDDING_DIM, units, vocab_size)

optimizer = tf.keras.optimizers.Adam()
loss_objective = tf.keras.losses.SparseCategoricalCrossentropy(
    from_logits=True, reduction='none')


def loss_function(real, pred):
    mask = tf.math.logical_not(tf.math.equal(real, 0))
    loss_ = loss_objective(real, pred)

    mask = tf.cast(mask, dtype=loss_.dtype)
    loss_ *= mask

    return tf.reduce_mean(loss_)


checkpoint_path = ".//512000-LSTM//512000-LSTM"#".//Full-LSTM//Full-LSTM"
ckpt = tf.train.Checkpoint(encoder=Image_encoder,
                           decoder=Text_decoder,
                           optimizer=optimizer)
ckpt_manager = tf.train.CheckpointManager(ckpt, checkpoint_path, max_to_keep=5)

ckpt.restore(ckpt_manager.latest_checkpoint)



def model(image_url):

    
    image_path = tf.keras.utils.get_file(image_url, origin=image_url)

    image_path = tf.keras.utils.get_file(image_url, origin=image_url)

    result, attention_plot = evaluate(image_path)
   
    print('Prediction Caption:', ' '.join(result))

    return result
