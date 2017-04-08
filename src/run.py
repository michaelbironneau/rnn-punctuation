from punctuate import Punctuate 
from to_docx import ToDocX 
from to_text import ToText 
from to_wav import ToWav 
from capitalize import Capitalize
from fix_spacing import FixSpacing
from transcription import new_transcription, read_options
import sys
import logging

logging.basicConfig(format='%(asctime)s %(message)s')

if len(sys.argv) < 2:
	print("Usage python3 run.py /path/to/options/file")
	sys.exit(1)

options = read_options(sys.argv[1])
transcription = new_transcription(options['audio_file'], title=options['title'])
toWav = ToWav(**options)
toText = ToText(options['watson_credentials'], **options)
toDocx = ToDocX(**options)
punc = Punctuate(options['punctuate_model'], options['wordlist'], **options)
caps = Capitalize()
space = FixSpacing()

toDocx(space(caps(punc(toText(toWav(transcription))))))

logging.info('Done!')
