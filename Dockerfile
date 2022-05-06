FROM python:3.9.12-bullseye
ENV PATH /root/.local/bin:$PATH

RUN mkdir project
COPY requirements.txt project/
WORKDIR ./project

RUN pip install -r requirements.txt

COPY . .
RUN echo "hello" > text.txt

EXPOSE 8000
