from __future__ import print_function
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation
from keras.layers import LSTM, Bidirectional
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import keras
import numpy as np
import random
import traceback
import sys
from maketokens import maketokens, get_words
import pickle

tokens = pickle.load(open('wordlist.pickle', 'rb'))

tokens = tokens + ["``", "''", ","  ,"--", ".", "!", "?", ":", "CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR",
"JJS", "LS", "MD", "NN", "NNP", "NNPS", "NNS", "PDT", "POS", "PRP", "PRP$", "RB", "RBR", "RBS", "RP", "SYM",
"TO", "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "WDT", "WP", "WP$", "WRB", "(", ")"]

output_tokens = [",", "--", ".", "!", "?", ":", "OTHER"]

token_indices = dict((c,i) for i,c in enumerate(tokens))
indices_tokens = dict((i,c) for i,c in enumerate(tokens))

output_token_indices = dict((c,i) for i,c in enumerate(output_tokens))

IGNORED_TOKEN = output_token_indices["OTHER"]
END_TOKENS = set([output_token_indices["."], output_token_indices["!"], output_token_indices["?"]])  # tokens that end a sentence


output_indices_tokens = dict((i,c) for i,c in enumerate(output_tokens))

MAX_LENGTH= 10  # maximum length of token memory used for training (+- this number of words)

def map_output_index(ix):
    """Returns an output token from an input token index, e.g. 'NNPS' -> 'OTHER' and '.' -> '.'"""
    token = indices_tokens[ix]
    if token in output_token_indices:
        return output_token_indices[token]
    else:
        return output_token_indices['OTHER']

def build_model(activation='softmax', loss='categorical_crossentropy', learning_rate=0.001):
    """Build new model and return the model object"""
    m = Sequential()
    m.add(LSTM(64, input_shape=(MAX_LENGTH*2, len(tokens))))  # MAX_LENGTH tokens forward, MAX_LENGTH backward
    m.add(Dense(len(output_tokens), input_shape=(len(tokens),)))
    m.add(Activation(activation))
    optimizer = RMSprop(lr=learning_rate)
    m.compile(loss=loss, optimizer=optimizer)
    return m

def load_sample_indices(input_path):
    """ Read the file and get indices out of tokens"""
    sample_tokens = []
    with open(input_path, 'r') as f:
        text = f.read()
        sample_tokens = text.split(' ')
    return [token_indices[token] for token in sample_tokens if token in token_indices]
    
def balance_samples(x_samples, y_samples):
    """Balances samples between OTHER output token and the rest. As it turns out,
    most samples don't have punctuation in the middle, so we need to weigh training more
    heavily towards punctuation-rich samples so the model learns that."""
    pass

def make_samples(sample_indices, step_size=1):
    """ 
    Make semi-redundant length MAX_LENGTH*2 samples from the given indices.
    Returns a tuple (X, Y).
    Get the indices by calling `load_sample_indices()`.
    """
    # slice samples
    x_samples = []
    y_samples = []
    for i in range(0, len(sample_indices), step_size):
        # read next ten chars that aren't punctuation
        j = i
        x_sample = []
        y_sample = None
        while j < len(sample_indices) and len(x_sample) < MAX_LENGTH:
            # forward tokens
            if map_output_index(sample_indices[j]) == IGNORED_TOKEN:
                # ignore punctuation characters
                x_sample.append(sample_indices[j])
            j = j + 1
        if j < len(sample_indices) and len(x_sample) == MAX_LENGTH:
            y_sample = map_output_index(sample_indices[j])
        else:
            continue
        while j < len(sample_indices) and len(x_sample) < MAX_LENGTH*2:
            # backward tokens
            if map_output_index(sample_indices[j]) == IGNORED_TOKEN:
                # ignore punctuation characters
                x_sample.append(sample_indices[j])
            j = j + 1
        if len(x_sample) == MAX_LENGTH*2 and y_sample is not None:
            x_samples.append(x_sample)
            y_samples.append(y_sample)
    # vectorize
    X = np.zeros((len(x_samples), 2*MAX_LENGTH, len(tokens)), dtype=np.bool)
    Y = np.zeros((len(x_samples), len(output_tokens)), dtype=np.bool)
    for i, sample in enumerate(x_samples):
        for t, tok in enumerate(sample):
            X[i, t, tok] = 1
        Y[i, y_samples[i]] = 1
    return (X, Y)

def apply_prediction(words, ix, pred):
    """Returns sample with prediction applied"""
    real_ix = MAX_LENGTH + ix
    char = ''
    if pred != IGNORED_TOKEN:
        char = output_tokens[pred]
    return words[:real_ix] + [char] + words[real_ix:]
    
    
model = None

# Load model, if it already exists

if len(sys.argv) < 3:
    sys.exit('Usage: [train|predict] train.py input.txt')
    
try:
    model = load_model('model.h5')
except:
    traceback.print_exc(file=sys.stdout)
    print('Could not open model file. Creating new model.')
    model = build_model()

command = sys.argv[1]

if command != 'train' and command != 'predict':
    sys.exit('Command should be "train" or "predict"')

if command == 'train':
    indices = []
    for fpath in sys.argv[2:]:
        f_indices = load_sample_indices(fpath)
        indices = indices + f_indices
    X, Y = make_samples(indices)
    if len(X) == 0 or len(Y) == 0:
        sys.exit('No data')
    for iteration in range(1,100):
        print()
        print('-'*10)
        print('Iteration', iteration)
        model.fit(X, Y, batch_size=128, nb_epoch=1, validation_split=0.1)
        model.save('model.h5')
else:
    words = get_words(sys.argv[2])
    preds = 0
    indices = [token_indices[token] for token in maketokens(sys.argv[2]) if token in token_indices]
    print('Word length: ', len(words))
    print('Index length: ', len(indices))
    i = 0
    while i < len(indices) - 2*MAX_LENGTH:
        sample = indices[i: i + 2*MAX_LENGTH]
        x = np.zeros((1, 2*MAX_LENGTH, len(tokens)))
        for j, ix in enumerate(sample):
            x[0, j, ix] = 1
        pred = np.argmax(model.predict(x, verbose=0)[0])
        if pred != IGNORED_TOKEN:
            words = apply_prediction(words, i+preds, pred)
            preds = preds + 1
        if pred in END_TOKENS:
                # split sentence off and work on next one
            i += MAX_LENGTH
        else:
            i += 1
    print(' '.join(words))