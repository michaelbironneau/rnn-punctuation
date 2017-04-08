mkdir tmp && \
scrapy debates.py -o ./tmp/debates.json && \
scrapy nato.py -o ./tmp/nato.json && \
scrapy usaspeeches.py -o ./tmp/usaspeeches.json && \
scrapy whitehouse.py -o ./tmp/whitehouse.json && \
mkdir corpus && \
find ./tmp/*.json| xargs python3 process_json.py