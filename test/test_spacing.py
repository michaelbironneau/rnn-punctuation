from src.fix_spacing import FixSpacing
import unittest 

class TestFixSpacing(unittest.TestCase):

	def test_output(self):
		c = FixSpacing()
		input_text = """ , who you just heard is from Lexington , Massachusetts and works for a national health care advocacy organization . she 's c"""
		expected_text = input_text = """, who you just heard is from Lexington, Massachusetts and works for a national health care advocacy organization. she's c"""
		output = c({'paragraphs': [{'content': input_text}]})['paragraphs'][0]['content']
		self.assertEqual(expected_text, output)

if __name__ == '__main__':
	unittest.main()
