# FROM nvidia/cuda:11.5.1-cudnn8-runtime-ubuntu20.04
# CMD nvidia-smi

#environment steup
# RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y curl
# RUN apt-get install unzip
# RUN apt-get -y install python3
# RUN apt-get -y install python3-pip
FROM python:3.7
RUN apt-get update
RUN pip install --upgrade pip

ENV HOME /app
WORKDIR /app
ENV PYTHONPATH="/app/.local/bin:${PYTHONPATH}"
ENV TOKENIZERS_PARALLELISM=false


RUN mkdir -p /app/artifacts && mkdir -p /app/registered_models_checkpoints
#copy requirements.txt
ADD ./requirements.txt ./requirements.txt 
RUN pip3 install --no-cache-dir -r ./requirements.txt 
EXPOSE 6006
COPY ./ /app
CMD ["python", "intent_recognition/train_pipeline.py"]
