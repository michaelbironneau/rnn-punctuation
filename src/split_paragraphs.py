import logging
import copy
from nltk import word_tokenize
from nltk import sent_tokenize
import pickle
from sklearn.ensemble import RandomForestClassifier

fin_pun = {'.': 0, '!': 1, '?': 3, 'OTHER': 4}

def _get_vec(paragraph):
    """Get training vector for a single paragraph"""
    sentences = sent_tokenize(paragraph)
    ret = []
    cumm_Ds = 0
    cumm_Dw = 0
    Fin_Pun = 0
    for sentence in sentences:
        delta_s = 1
        delta_w = len(word_tokenize(sentence))
        fp = sentence.strip()[-1]
        if fp in fin_pun:
            fp = fin_pun[fp]
        else:
            fp = fin_pun['OTHER']
        ret.append({
            'D_s': cumm_Ds + delta_s,
            'D_w': cumm_Dw + delta_w,
            'Length': delta_w,
            'EndOfP': 0,
            'FinPun': fp
        })
        cumm_Ds += delta_s
        cumm_Dw += delta_w
    ret[-1]['EndOfP'] = 1
    return ret

def make_training_vectors(paras):
    """
    Convert a list of paragraphs to a training vector
    
    The features come from http://homepages.inf.ed.ac.uk/mlap/Papers/emnlp04.pdf.
    """
    #total_length = sum([len(sent_tokenize(para)) for para in paras])
    X = []
    Y = []
    for para in paras:
        vecs = _get_vec(para)
        for vec in vecs:
            X.append([vec['D_s'], vec['D_w'], vec['Length'], vec['FinPun']])
            Y.append([vec['EndOfP']])
    return (X, Y)

class SplitParagraphs(object):
    """
    Add paragraph breaks.
    """
    _model = None
    _options = {'max_paragraphs': 100}
    
    def __init__(self, model, **kwargs):
    	with open(model, 'rb') as f:
    		self._model = pickle.load(f)
    	self._options.update(kwargs)
    
    def __call__(self, transcription):
    	logging.info('Splitting text into paragraphs...')
    	
    	new_t = copy.deepcopy(transcription)
    	new_t['paragraphs'] = []
    	for para in transcription['paragraphs']:
    		new_p = self._segment_text(self._model, [para['content']], max_splits=self._options['max_paragraphs'])
    		for p in new_p:
    			pc = copy.deepcopy(para)  # so we get other attributes, like the speaker, that this class may not be aware of
    			pc['content'] = p
    			new_t['paragraphs'].append(pc)		
    	return new_t
    
    def _segment_text(self, model, paras, max_splits=4):
        """Recursively segment the text into paragraphs."""
        if max_splits == 0:
            return paras
        for i in range(len(paras)):
            x_pred, _ = make_training_vectors([paras[i]])
            splits = model.predict(x_pred)
            # Only retain first split
            if 1 in splits[:-1]:
                # Not terminating
                sentences = sent_tokenize(paras[i])
                split_ix = list(splits).index(1)
                new_p = [' '.join(sentences[:split_ix]), ' '.join(sentences[split_ix:])]
                new_ps = [p for p in paras[:i]] + new_p + [p for p in paras[i+1:]]
                return self._segment_text(model, new_ps, max_splits-1)
        return paras
    	
