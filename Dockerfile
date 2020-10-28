FROM python:3
ADD splot-crawl.py /
ADD requirements.txt /
RUN pip install -r requirements.txt
CMD [ "python", "./splot-crawl.py" ]