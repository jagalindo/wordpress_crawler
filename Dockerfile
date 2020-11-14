FROM python:3
ADD crawl_wp.py /
ADD requirements.txt /
RUN pip install -r requirements.txt
CMD [ "python", "./crawl_wp.py" ]
