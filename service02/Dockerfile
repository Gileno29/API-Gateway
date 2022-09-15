FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


#ENTRYPOINT ["python3", "manage.py", "runserver", '0:8000']
COPY . .

#CMD ["manage.py runserver 127.0.0.1:8000" ]