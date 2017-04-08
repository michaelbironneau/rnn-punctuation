from src.to_docx import ToDocX
import unittest 
import os.path
import os 

class TestToDocX(unittest.TestCase):
	output_file = 'test.docx'

	def test_output(self):
		transcription = {'title': 'Test', 'paragraphs': [{'content': 'The cat sat on the mat.'}]}
		dx = ToDocX(output_file=TestToDocX.output_file)
		dx(transcription)
		self.assertTrue(os.path.isfile(TestToDocX.output_file))
		os.remove(TestToDocX.output_file)
		
if __name__ == '__main__':
	unittest.main()
