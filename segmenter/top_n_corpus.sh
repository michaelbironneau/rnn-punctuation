rm -rf data && mkdir data
find training-files/*.txt | xargs python3 top_n_words.py
