# HOW TO IMPLEMENT AN API GATEWAY IN NGINX

### First we need to know what API Gateway is.
when we talking about microservices one of the most important points are the comunication between them, it is crucial for good comunication between services.
With an API gateway it is possible to create a single entry point for requests for different services by centralizing them.
this allows for multiple benefits such as separation in the application layers a single, extra layer of protection among others. More information can be seen in this <a href="https://blog.engdb.com.br/api-gateway/?utm_source=google&utm_medium=cpc&utm_campaign=Campanha+Smart+Tax+Platform+-+Leads&gclid=CjwKCAjwpqCZBhAbEiwAa7pXeZYIHDXreFEq3kMWd4FBNeRTBn0_P7GD-Olt1x6muBwm437WG0HZzRoCJLMQAvD_BwE">post</a>.

# PROJECT 
This project consists in a implementation of an API gateway using NGINX, for example, two contentiary services were used, a simple implementation of api prototype using Flask and a Djago server.
services can be accessed by endpoints that will be directed to the correct services by nginx


# CONFIGURATION API GATEWAY

## nginx.conf
    user nginx;
    worker_processes 1;

    error_log /var/log/nginx/error.log warn;
    pid /var/run/nginx.pid;

    events {
        worker_connections 1024;
    }

    http {
        include /etc/nginx/conf.d/proxy.conf;
        include /etc/nginx/mime.types;
        include /etc/nginx/fastcgi_params;
        include /etc/nginx/scgi_params;
        include /etc/nginx/uwsgi_params;
        
        index index.html index.htm;
        
        default_type application/octet-stream;

        log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                        '$status $body_bytes_sent "$http_referer" '
                        '"$http_user_agent" "$http_x_forwarded_for"';
    
        access_log off;
        server_tokens off;
        sendfile on;
        tcp_nopush on;
        tcp_nodelay on;
        keepalive_timeout 65;

        server {

            listen 80 default_server;
            listen [::]:80 default_server;
            
            server_name _;
            root /usr/share/nginx/html;

            location /flask {
                proxy_pass http://flask-api:5000/;
            }

            location  /django {
                proxy_pass http://django-project:8000/;
            }
            

            location /images {
            access_log off;
            return 204;
            }
        }
    }


## proxy.conf
    proxy_redirect off;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Host $server_name;

# DOCKER FILES
## SERVICE 01

        FROM python:3

        WORKDIR /usr/src/app

        COPY requirements.txt ./
        RUN pip install --no-cache-dir -r requirements.txt


        ENTRYPOINT [ "python3" ]
        COPY api.py ./

        CMD ["api.py" ]

## SERVICE 02
    FROM python:3

    WORKDIR /usr/src/app

    COPY requirements.txt ./
    RUN pip install --no-cache-dir -r requirements.txt
    COPY . .



# DOCKER COMPOSE
    version: '3'
    networks:
    proxy:
    services:
        internal: true

    services:
    proxy-api:
        image: nginx
        container_name: proxy-api
        restart: unless-stopped
        volumes:
            - ./nginx/nginx.conf:/etc/nginx/nginx.conf
            - ./nginx/proxy.conf:/etc/nginx/conf.d/proxy.conf
        ports:
            - 80:80
        networks:
            - services
            - proxy
    service01:
        build: ./service01
        container_name: flask-api
        volumes:
        - ./service01/api.py

        ports:
        - 5000:5000
        networks:
        - services

        depends_on:
        - proxy-api
    
    service02:
        build: ./service02/
        container_name: django-project
        command: python manage.py runserver 0.0.0.0:8000
        volumes:
        - ./service02/
        ports:
        - 8000:8000
        networks:
        - services
        depends_on:
        - proxy-api

in the services declaration we have three services one that is the api gateway, it is responsible for  forwarding requisitions and the others two are the services that can be access by the clients.



# RUN THE PROJECT

        docker-compose up -d 


you can access the project with django by the URL: ```http://localhost/django/``` and the flask project by the URL:```http://localhost/django/```