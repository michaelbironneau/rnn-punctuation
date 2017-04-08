import logging

class FixSpacing(object):
	"""
	Remove superfluous spacing characters.
	"""
	def __call__(self, transcription):
		logging.info('Fixing spacing...')
		
		for i in range(len(transcription['paragraphs'])):
			transcription['paragraphs'][i]['content'] = self._fix_spacing(transcription['paragraphs'][i]['content'])
		
		return transcription
		
	def _fix_spacing(self, paragraph):
		"""Fix spacing in paragraph"""
		paragraph = paragraph.replace(" 's", "'s")
		paragraph = paragraph.replace(" , ", ", ")
		paragraph = paragraph.replace(" . ", ". ")
		return paragraph