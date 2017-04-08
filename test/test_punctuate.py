from src.punctuate import Punctuate
import unittest 

class TestPunctuate(unittest.TestCase):
	model = './models/model.3000dictsize.h5'
	wordlist = './models/wordlist.3000.pickle'
	
	def test_output(self):
		p = Punctuate(TestPunctuate.model, TestPunctuate.wordlist)
		input_text = """Mr. Speaker Mr. President Members of the Congress It is with a heavy heart that I stand before you my friends and colleagues in the Congress of the United States Only yesterday we laid to rest the mortal remains of our beloved President Franklin Delano Roosevelt At a time like this words are inadequate The most eloquent tribute would be a reverent silence yet in this decisive hour when world events are moving so rapidly our silence might be misunderstood and might give comfort to our enemies."""
		output = p({'paragraphs': [{'content': input_text}]})['paragraphs'][0]['content']
		self.assertTrue((',' in output))
		self.assertTrue(('.' in output))
		self.assertTrue(len([word for word in input_text.split(' ') if word not in output])<10)
	
if __name__ == '__main__':
	unittest.main()
