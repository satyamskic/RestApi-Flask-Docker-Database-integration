# RestApi-Flask-Docker-Database-integration

# Step-1
First create Dockerfile which creates the python image for deploy frontend application.
```
FROM python:latest
COPY ./app /app
COPY requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["main.py"]

```
