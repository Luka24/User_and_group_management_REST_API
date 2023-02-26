FROM python:3.11.2

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP=application.py

RUN python create_db.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]