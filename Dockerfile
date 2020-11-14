FROM python:3
RUN apt-get update && \
    apt-get -o Dpkg::Options::="--force-overwrite" --no-install-recommends install -y \
	chromium-driver \ 
	chromium
RUN mkdir data
ADD crawl_wp.py /
ADD requirements.txt /
RUN pip install -r requirements.txt
CMD [ "python", "./crawl_wp.py" ]
