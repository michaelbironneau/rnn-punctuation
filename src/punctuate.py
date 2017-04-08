from keras.models import load_model
import nltk
from nltk import word_tokenize
import sys
import os
import pickle
import codecs
import numpy as np
import logging


MAX_LENGTH= 10  # maximum length of token memory used for training (+- this number of words)

class Punctuate(object):
	"""This takes a sentence with no punctuation and adds it back using a Recurrent Neural Network model.

	Necessary arguments:

	model = 'model filename.h5' # (required)
	wordlist = 'wordlist.pickle filename' # (required, must match the wordlist for the model)

	"""

	_options = {}
	_model = None
	_wordlist = None

	def __init__(self, model, wordlst, **kwargs):
		self._model = load_model(model)
		with open(wordlst, 'rb') as lst:
			self._wordlist = pickle.load(lst)
		if len(self._wordlist) < 100:
			raise Exception('Insufficient words in wordlist')
		self._wordlist = self._wordlist + ["``", "''", ","  ,"--", ".", "!", "?", ":", "CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR",
			"JJS", "LS", "MD", "NN", "NNP", "NNPS", "NNS", "PDT", "POS", "PRP", "PRP$", "RB", "RBR", "RBS", "RP", "SYM",
			"TO", "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "WDT", "WP", "WP$", "WRB", "(", ")"]
		#self._wordlist = set(self._wordlist)
		self._output_tokens = [",", "--", ".", "!", "?", ":", "OTHER"]

		self._token_indices = dict((c,i) for i,c in enumerate(self._wordlist))
		self._indices_tokens = dict((i,c) for i,c in enumerate(self._wordlist))

		self._output_token_indices = dict((c,i) for i,c in enumerate(self._output_tokens))

		self._IGNORED_TOKEN = self._output_token_indices["OTHER"]
		self._END_TOKENS = set([self._output_token_indices["."], self._output_token_indices["!"], self._output_token_indices["?"]])  # tokens that end a sentence
		self._output_indices_tokens = dict((i,c) for i,c in enumerate(self._output_tokens))
		self._options.update(kwargs)

	def _tokenize(self, text):
		"""Tokenize the text"""
		words = None 
		tokens = None
		ret = []
		tokens = nltk.pos_tag(word_tokenize(text))
		for word, token in tokens:
			if word.lower() in self._wordlist:
				# most common words
				ret.append(word.lower())
				continue
			if token == '.':
				ret.append(word)  # this way we get all possible punctuation marks - IMPORTANT!
			elif token == '$':
				ret.append('SYM')  # we don't need to process dollar signs separately from any other symbol!
			else:
				ret.append(token) 
		return ret

	def __call__(self, transcription):
		"""Punctuate each paragraph of the transcription object"""
		logging.info('Puctuating text...')
		for i in range(len(transcription['paragraphs'])):
			text = transcription['paragraphs'][i]['content']
			text = self._punctuate(text)
			transcription['paragraphs'][i]['content'] = text
		return transcription

	def _apply_prediction(self, words, ix, pred):
		"""Returns sample with prediction applied"""
		real_ix = MAX_LENGTH + ix
		char = ''
		if pred != self._IGNORED_TOKEN:
			char = self._output_tokens[pred]
		return words[:real_ix] + [char] + words[real_ix:]
		

	def _punctuate(self, text):
		"""Punctuate the given text and return it"""
		words = word_tokenize(text)
		preds = 0
		indices = [self._token_indices[token] for token in self._tokenize(text) if token in self._token_indices]
		i = 0
		while i < len(indices) - 2*MAX_LENGTH:
			sample = indices[i: i + 2*MAX_LENGTH]
			x = np.zeros((1, 2*MAX_LENGTH, len(self._wordlist)))
			for j, ix in enumerate(sample):
				x[0, j, ix] = 1
			pred = np.argmax(self._model.predict(x, verbose=0)[0])
			if pred != self._IGNORED_TOKEN:
				words = self._apply_prediction(words, i+preds, pred)
				preds = preds + 1
			if pred in self._END_TOKENS:
					# split sentence off and work on next one
				i += MAX_LENGTH
			else:
				i += 1
		output = ' '.join(words)
		if output[-1] != '.':
			output += '.'
		return output