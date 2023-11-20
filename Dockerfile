FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /django

COPY ./nginx/nginx.conf ./nginx/
COPY ./nginx/conf.d/default.conf ./nginx/conf.d/
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# COPY . .

EXPOSE 80


# RUN python manage.py migrate
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
