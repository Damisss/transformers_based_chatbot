FROM python:3.7

RUN apt-get update
ENV HOME /app
WORKDIR /app
ENV PYTHONPATH="/app/.local/bin:${PYTHONPATH}"
ADD ./requirements.txt ./requirements.txt 
RUN pip3 install --no-cache-dir -r ./requirements.txt
COPY .   /app
EXPOSE 3001


