# RestApi-Flask-Docker-Database-integration

## Frontend
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
## Backend
In above project, MySQL database contaier deployed directly from docker-compose.yml file.  
```
  mysql-db:
        container_name: mysql-db
        image: mysql:5.7
        restart: always
        environment:
            MYSQL_ROOT_PASSWORD: root
            MYSQL_DATABASE: users
        ports:
            - '3308:3306'
        command: --init-file /data/application/init.sql
        volumes:
            - ./init.sql:/data/application/init.sql
            - ./database:/var/lib/mysql
        networks:
            - backend
```
## API Gateway
Haproxy are used as a API Gateway(loadbalancer). When any users from internet hit loadbalancer IP address then it's redirect traffic to the frontend application. Configuration file of haproxy is located at `haproxy/haproxy.cfg file`.

```
```



