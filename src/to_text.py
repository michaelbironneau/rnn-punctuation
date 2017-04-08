from pydub.utils import mediainfo
from watson_developer_cloud import SpeechToTextV1
import json
import logging

class ToText(object):
	"""Convert the given audio file to test. Only WAV files are supported.
	Use the ToWAV class to convert to WAV if required.

	Options:

	watson_model = 'Name of watson model, not including NarrowbandModel or BroadbandModel' # e.g. 'en-US'
	"""

	_options = {}
	_creds = None

	def __init__(self, credentials, **kwargs):
		# Do this in the constructor so we don't start the pipeline for nothing if we're missing the file or it isn't well formatted
		with open(credentials) as creds_file:    
			self._creds = json.load(creds_file)
		self._options.update(kwargs)


	def _get_model(self, transcription):
		"""Validate the file and return the model"""
		model = 'en-US'
		if 'model' in self._options:
			model = self._options['model']
		info = mediainfo(transcription['file'])
		sample_rate = int(info['sample_rate'])
		if 'NarrowbandModel' in model or 'BroadbandModel' in model:
			raise Exception('Please do not include NarrowbandModel or BroadbandModel in `model` option')

		if sample_rate < 8000:
			raise Exception('Insufficient sampling rate')
		elif sample_rate < 16000:
			model += '_NarrowbandModel'
		else:
			model = '_BroadbandModel'

	def __call__(self, transcription):
		"""Convert the audio file to text"""
		logging.info('Converting WAV to text...')
		speech_to_text = SpeechToTextV1(
			username=self._creds['username'],
			password=self._creds['password'],
			x_watson_learning_opt_out=False
		)
		with open(transcription['file'], 'rb') as audio_file:
			watson_doc = speech_to_text.recognize(audio_file, content_type='audio/wav', continuous=True)
		paras = []
		for result in watson_doc['results']:
			paras.append(result['alternatives'][0]['transcript'])
		transcription['paragraphs'] = [{'content': ' '.join(paras)}] #TODO: Pass these in differently if we want to identify speakers or something...
		return transcription