from src.capitalize import Capitalize
import unittest 

class TestCapitalize(unittest.TestCase):

	def test_output(self):
		c = Capitalize()
		input_text = """this is a test. 12 partriges in a pear tree. i want the first letter capitalized."""
		expected_text = input_text = """This is a test. 12 partriges in a pear tree. I want the first letter capitalized."""
		output = c({'paragraphs': [{'content': input_text}]})['paragraphs'][0]['content']
		self.assertEqual(expected_text, output)

if __name__ == '__main__':
	unittest.main()
