import nltk
from nltk import word_tokenize
import sys
import os
import operator
import codecs
import pickle 

common_words = {}

tokens = ["``", "''", ","  ,"--", ".", "!", "?", ":", "CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR",
"JJS", "LS", "MD", "NN", "NNP", "NNPS", "NNS", "PDT", "POS", "PRP", "PRP$", "RB", "RBR", "RBS", "RP", "SYM",
"TO", "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "WDT", "WP", "WP$", "WRB", "(", ")"]

token_set = set(tokens)
MAX_WORDS = 3000

def update_dict(new_words):
	for word in new_words:
		if word in common_words:
			common_words[word] = common_words[word] + 1
		else:
			common_words[word] = 1

def is_numeric(word):
	try:
		int(word.replace(',','').replace('.', ''))
		return True
	except ValueError:
		return False

def update(path):
	with codecs.open(path, "r",encoding='utf-8', errors='ignore') as f:
	#with open(path, 'r') as f:
		words = word_tokenize(f.read())
		update_dict(words)

if __name__ == "__main__":
	for path in sys.argv[1:]:
		update(path)
	sorted_words = sorted(common_words.items(), key=operator.itemgetter(1), reverse=True)
	sorted_words = [word.lower() for word, _ in sorted_words if (word not in tokens and not is_numeric(word))]
	sorted_words = sorted_words[:MAX_WORDS]
	#sorted_words = sorted_words + tokens
	print(sorted_words)
	pickle.dump(sorted_words, open('wordlist.pickle', 'wb'))
	
