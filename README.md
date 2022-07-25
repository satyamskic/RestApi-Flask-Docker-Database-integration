# RestApi-Flask-Docker-Database-integration

## Backend
1. First creating Dockerfile which creates the python image for deploy backend application.
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

2. Deploying backend application using `docker-compose.yml` file. 

Few points needs to be noted........
- Here backend code are located inside app folder. 
- It's uses the similar network as databse have. 
- Exposing backend at port no 5000.

```
    flask-app:
        container_name: flask-app
        build: ./
        restart: always
        links:
            - mysql-db
        ports:
            - '5000:5000'
        volumes:
            - ./app:/app
        networks:
            - backend
        depends_on:
            - mysql-db
```


## Database
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
Haproxy are used as a API Gateway(loadbalancer). When any users from internet hit loadbalancer IP address then it's redirect traffic to the frontend application. 

Few points needs to be note........

- Configuration file of haproxy is located at `haproxy/haproxy.cfg file`.
- There is three frontend server name are (weba, webb, webc) which is creating directly from the `docker-compose.yml` file and adding it's links to haproxy links section. 
- After that exposing haproxy to port no 8888 and 70. 
```
haproxy:
        image: haproxy:1.6
        volumes:
            - ./haproxy:/haproxy-override
            - ./haproxy/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro
        links:
            - weba
            - webb
            - webc
        ports:
            - "8888:80"
            - "70:70" 
    weba:
        build: ./frontend
        expose:
            - 80

    webb:
        build: ./frontend
        expose:
            - 80
  
    webc:
        build: ./frontend
        expose:
            - 80
```

# ansible playbook
- There is three task which is creating with the help of Ansible playbook. It's basically doing three things

a) Installing docker

b) Installing docker-compose to run docker-compose.yml file

c) Triggers the `docker-compose.yml` file


- It's using inventory file.
```
- name: Run with inline v2 compose
  hosts: localhost
  gather_facts: no
  tasks:
    - name: install docker
      apt:
        name: docker.io
        state: present
    - name: install docker compose
      pip:
        name: docker-compose
        state: present
    - name: deploy app with docker compose
      shell: |
        docker-compose up -d
```

## Note
First clean docker environment before deploying your application using the Jenkins. Use below command to cleanup the environment at same path where your `docker-compose.yml` file located.
```
docker-compose kill
docker rm -f $(docker ps -a -q)
docker rmi -f $(docker images -a -q)

```
# Jenkins Integration
After cleanup your environment trigger the Jenkins job eighter manually or using any triggers depending on your requirnment. It will deploy entire infrastructure.




