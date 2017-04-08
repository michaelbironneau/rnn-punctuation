import json 

def new_transcription(audio_file, **kwargs):
	"""Start a new transcription"""
	transcription = {
		'file': audio_file,
		'title': 'Transcript'
	}
	transcription.update(kwargs)
	return transcription


def read_options(fpath):
	"""Read from options file and produce options object"""
	with open(fpath) as f:
		return json.load(f)
