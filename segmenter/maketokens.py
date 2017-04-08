import nltk
from nltk import word_tokenize
import sys
import os
import pickle
import codecs

wordlist = set(pickle.load(open('wordlist.pickle', 'rb')))

def get_words(path):
	tokens = []
	with codecs.open(path, "r",encoding='utf-8', errors='ignore') as f:
		tokens = word_tokenize(f.read())
	return tokens

def maketokens(path):
	doc = None
	words = None 
	tokens = None
	ret = []
	with codecs.open(path, "r",encoding='utf-8', errors='ignore') as f:
		words = word_tokenize(f.read())
		tokens = nltk.pos_tag(words)
	for word, token in tokens:
		if word.lower() in wordlist:
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

if __name__ == "__main__":
	for path in sys.argv[1:]:
		base=os.path.basename(path)
		with open(os.path.join('./data', os.path.splitext(base)[0] + '.txt'), 'w') as f:
			f.write(' '.join(maketokens(path)))
	
