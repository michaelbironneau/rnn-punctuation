import logging

class Capitalize(object):
	"""
	Make the first letter of each paragraph and every letter after a full stop and space a capital letter.
	"""
	def __call__(self, transcription):
		logging.info('Capitalizing...')
		
		for i in range(len(transcription['paragraphs'])):
			transcription['paragraphs'][i]['content'] = self._capitalize(transcription['paragraphs'][i]['content'])
		
		return transcription
		
	def _capitalize(self, paragraph):
		"""Capitalize paragraph"""
		paragraph = paragraph[0].upper() + paragraph[1:]
		capitalize_next = False
		for i in range(len(paragraph)):
			if paragraph[i] == '.':
				capitalize_next = True
			elif capitalize_next:
				if paragraph[i].isalpha():
					paragraph = paragraph[:i] + paragraph[i].upper() + paragraph[(i+1):]
					capitalize_next = False
				elif paragraph[i] != ' ':
					capitalize_next = False  # don't capitalize after numbers or symbols
		return paragraph