FROM python:3.10-slim-buster

#install requeriments
RUN pip install flask
RUN pip install psycopg2-binary
RUN pip install flask_cors

 
COPY ./ /app
WORKDIR  /app
CMD [ "chmod","775","/app" ]
ENTRYPOINT ["python3", "main.py"]
#RUN python3 main.py
