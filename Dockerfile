FROM python:3.9.12-bullseye
ENV PATH /root/.local/bin:$PATH

RUN mkdir project
COPY requirements.txt project/
WORKDIR ./project

RUN pip install -r requirements.txt

COPY . .
WORKDIR ./site_backend
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000

