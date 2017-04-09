from src.split_paragraphs import SplitParagraphs
import unittest 

class TestSplitParagraphs(unittest.TestCase):

	def test_output(self):
		c = SplitParagraphs('./models/paragraph.splitter.pickle')
		input_text = """Motorola (which has been known as Lenovo Moto, but is now back to Motorola again) is the only brand left embracing a modular design. Need more battery? Snap on a Moto Mod battery pack. Want to up your entertainment game? Try on the speaker or projector Mod. With Google's Project Ara folded and LG's G5 experiment failed, the modular Moto Z could help decide Motorola's fate as a brand. The Moto Z family currently consists of the Moto Z, Moto Z Play, and Moto Z Force. In addition to the phones, Motorola has pledged to keep releasing Moto Mods at a rate of at least 12 a year. A next-gen Moto Z2 would help keep the Mods alive. Besides the rumored name, we haven't heard much else about the Moto Z2. The original Moto Z debuted last July, so we could be learn more about the phone in the next few months if the Moto Z follows an annual release schedule. In the meantime, there are plenty of new Moto Mods to keep your current Moto Z feeling fresh."""
		
		output = c({'paragraphs': [{'content': input_text}]})
		self.assertTrue(len(output['paragraphs'])>1 and len(output['paragraphs']) < 5)  # acceptable range of paragraphs

if __name__ == '__main__':
	unittest.main()
