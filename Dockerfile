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
ENV DJANGO_SUPERUSER_USERNAME adminuser
ENV DJANGO_SUPERUSER_EMAIL adminuser@test.com
ENV DJANGO_SUPERUSER_PASSWORD 111111
RUN python manage.py createsuperuser --noinput
RUN echo "from django.contrib.auth import get_user_model; User=get_user_model(); from rest_framework.authtoken.models import Token; Token.objects.create(key='visitor', user=User.objects.create(username='visitor')); Token.objects.create(key='adminuser', user=User.objects.get(username='adminuser')); " | python manage.py shell

EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000

