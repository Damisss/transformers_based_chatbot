FROM python:3.7
RUN apt-get update
RUN pip install --upgrade pip
ENV HOME /app
WORKDIR /app
ENV PYTHONPATH='app/.local/bin:${PYTHONPATH}'
ADD ./requirements.txt ./requirements.txt
COPY . /app
RUN pip3 install --no-cache -r requirements.txt
RUN addgroup --system user && adduser --system --group user
RUN chown -R user:user /app && chmod -R 755 /app
USER user