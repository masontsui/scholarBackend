FROM python:3.8-alpine

WORKDIR /app

RUN python3 -m venv /app
RUN . /app/bin/activate
RUN pip install Flask requests

COPY . /app

EXPOSE 5000

#CMD [ "python", "-m", "flask", "--app", "router", "run" ]
CMD [ "python", "router.py" ]

#CMD ["python3 -m flask --app /app/router.py run"]

#ENTRYPOINT ["python"]
