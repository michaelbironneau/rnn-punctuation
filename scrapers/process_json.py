import sys 
import codecs
import json
import re
import os
    

if len(sys.argv) < 2:
    print("Usage: python process_json.py file1.json [file2.json [file3.json...]]")

for fpath in sys.argv[1:]:
    with open(fpath) as f:
        samples = json.load(f)
        for d in samples:
            out_file_name = re.sub(r'\W+', '', d['title']) + '.txt'
            with open(os.path.join('./corpus', out_file_name), 'w') as f_out:
                f_out.write(d['content'])