# Punctuated Audio Transcription

This repository is an experiment to use Recurrent Neural Network to punctuate the output of IBM's speech-to-text API.

## Run a Transcription

The `options.json` file is assumed to contain all the options you want, including a path to the audio file. Example below:

```
{
	"title": "Transcription",
	"audio_file": "obama_speech.wav",
	"output": "output.docx",
	"punctuate_model": "../models/model.3000dictsize.h5",
	"wordlist": "../models/wordlist.3000.pickle",
	"watson_model": "en-US",
	"watson_credentials": "../credentials.json",
	"start": 0,
	"finish": 15
}
```


You'll also need a `credentials.json` file with your Watson Text-To-Speech username and password. It should look like this:
```
{
  "url": "https://stream.watsonplatform.net/speech-to-text/api",
  "username": "[YOUR USERNAME]",
  "password": "[YOUR PASSWORD]"
}

```

Once you have created your options file, you can run the model:

```
python3 src/run.py [path-to-options-file]
```

## Training the model from scratch

### Installation

Run 
```
./install.sh && sudo pip3 install -r requirements.txt
```

If you don't already have Tensorflow installed, go make yourself coffee or two, as it may take a while.

If you don't get any errors, at the end you should be able to run `import tensorflow` in a Python 3 interpreter.

### Creating a Corpus

There are scrapers in the `scrapers` folder. You'll need Scrapy to run them, so install it with 
```
pip3 install -r scrapers/requirements.txt
```

Once you have finished that installation, use `scrapers/make-corpus.sh` to scrape sources and create the corpus. After that has run, you should have a `corpus` folder populated with plain text files.

### Creating a Training Set from a Corpus
Assuming you have a corpus, place each plain text file in a folder called `training-files` (in this directory), and run `segmenter/top_n_corpus.sh`, followed by `segmenter/create-trainingset.sh`.

You should now have a `data` folder populated with tokenized and tagged documents and a `wordlist.pickle` file.

### Training a model

Run `model/train.sh`. If the training set is too large to fit in memory, you may get an error, in that case, try:

```
find data/*.txt | sort -R | tail -250 | xargs python3 model/model.py train
```

### Testing a model on a given input file

To test the model with an input file not containing any punctuation, run
```
python3 model/model.py predict [path-to-file.txt]
```

There is a sample input file at `segmenter/test.txt`, and you can try the model on this file by running `model.py predict test.txt` from that directory.