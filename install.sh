sudo add-apt-repository ppa:mc3man/trusty-media && \
sudo apt-get update && \
sudo apt-get install ffmpeg python3 python3-pip build-essential gfortran libatlas-base-dev libatlas3gf-base python-dev libjpeg-dev libxml2-dev libfreetype6-dev libpng-dev libffi-dev -y && \
sudo pip3 install -r requirements.txt