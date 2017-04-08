import ffmpy
import tempfile
import os
import time
import logging

class ToWav(object):
    """Convert the given audio file to WAV. Options:

    start = point in time to start at, in ss
    finish = point in time to finish at, in ss 
    """

    _options = {}

    def __init__(self, **kwargs):
        self._options.update(kwargs)

    def _convert(self, transcription):
        """Convert the audio file to WAV, possibly with truncation"""
        tmp_file = os.path.join(tempfile.mkdtemp(), 'output.wav')
        start = 0
        finish = 0
        if 'start' in self._options:
            start = self._options['start']
        if 'finish' in self._options:
            finish = self._options['finish']

        if start >= finish:
            raise Exception("`finish` should be > `start`")
        
        ff = ffmpy.FFmpeg(
            inputs={transcription['file']: '-t {0} -ss {0}'.format(finish-start, self.format_seconds_to_hhmmss(start))},
            outputs={tmp_file: None})
        ff.run()
        transcription['file'] = tmp_file  # set the new file name to the converted audio file

    def format_seconds_to_hhmmss(self, seconds):
        hours = seconds // (60*60)
        seconds %= (60*60)
        minutes = seconds // 60
        seconds %= 60
        return "%02i:%02i:%02i" % (hours, minutes, seconds)

    def __call__(self, transcription):
        """Convert the audio file to WAV"""
        logging.info('Converting to WAV...')
        self._convert(transcription)
        return transcription