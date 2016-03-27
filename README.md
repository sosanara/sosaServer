# sosaServer
Senior Project in Hansung Univ.

## Worked by Team Sosanara

---

## Server Settings.

참고 ```http://uwsgi-docs.readthedocs.org/en/latest/tutorials/Django_and_nginx.html#using-unix-sockets-instead-of-ports```

#### 1. 가상환경 virtualenv
virtualenv로 가상환경 venv를 만들고 requirements.txt에 있는 목록을 ```pip install``` 로 설치

#### 2. 가상환경 테스트 (localhost:8000)
```uwsgi --http :8000 --wsgi-file helloWorld.py```

#### 3. 서버 설치
```brew install nginx```

#### 4. symlink로 nginx 경로 변경
```ln -s /usr/local/Cellar/nginx/Your_Version /usr/local/ngnix```

#### 5. LaunchDaemons로 plist를 옮겨줌으로써 부팅시 자동 실행
```sudo ln -s /usr/local/opt/nginx/homebrew.mxcl.nginx.plist /Library/LaunchDaemons/homebrew.mxcl.nginx.plist```

#### 6. nginx 실행 or 중지 테스트 (localhost:8080 - port는 자동 매핑)
```sudo /usr/local/ngnix/bin/nginx``` or ```sudo /usr/local/ngnix/bin/nginx -s stop```

#### 7. nginx 전체 설정 파일인 nginx.conf 설정

```/usr/local/etc/nginx/nginx.conf``` 아래 코드처럼 설정 (sites-enabled 폴더가 없으면 생성)
~~~
http {
  include /usr/local/etc/nginx/sites-enabled/*;
  include       mime.types;
  default_type  application/octet-stream;
  ....
~~~

#### 8. 프로젝트 코드의 conf/ 폴더에 Project_Name.conf 파일을 만들고 아래 설정을 적용

~~~
# sosaServer.conf

# nginx가 요청을 전달할 django 서버의 정보를 적어준다.
upstream django {
    # 이 예제에서는 unix 파일 소켓을 사용한다. 아래의 Http 보다 좀더 가볍게 동작한다고 한다.
    # 윈도우즈 서버에서 돌리는 경우라면 아래 주석 처리되어 있는 HttpSocket 으로 설정한다.
    server unix:///Path/sosaServer/sosaServer.sock;
    #server 127.0.0.1:8001; # for a web port socket
}

# Virtual Host 설정 시작
server {
    # the port your site will be served on
    listen      8000;
    # the domain name it will serve for
    server_name localhost; # substitute your machine's IP address or FQDN
    charset     utf-8;

    # max upload size
    client_max_body_size 75M;   # adjust to taste

    # Django 에서 static 한 resource 를 서빙해야 한다면 alias를 통해 서빙 할 수 있다.
    location /static  {
        alias /Path/sosaServer/static;
    }

    # /static 를 제외한 모든 요청은 이제 아래 설정된 django 로 보내게 된다.
    location / {
        uwsgi_pass  django;
        # uwsgi를 사용하려면 uwsgi_params 파일이 필요하다.
        # 최근 버전의 nginx 를 설치하면 /usr/local/etc/nginx/uwsgi_params 파일이 존재한다.
        # 이 파일이 없다면 https://github.com/nginx/nginx/blob/master/conf/uwsgi_params 파일을 내려받아 사용하도록 한다.
        include     /usr/local/etc/nginx/uwsgi_params;
    }
}
~~~

#### 9. 설정한 conf 파일을 symlink로 site-enabled로 옮김 & 실행 테스트 (django + uwsgi)
(7번의 설정으로 nginx가 실행할 때 마다 sites-enabled를 스캔 & 실행함.)
```ln -s /Path/sosaServer/conf/sosaServer.conf /usr/local/etc/nginx/sites-enabled/```

```uwsgi --socket /Path/sosaServer/sosaServer.sock --module sosaServer.wsgi --chmod-socket=664```

#### 10. conf 폴더 안에 실행파일 생성
~~~
# sosaServer_uwsgi.ini file
[uwsgi]

# Django-related settings
# the base directory (full path)
chdir           = /Path/sosaServer
# Django's wsgi file
module          = sosaServer.wsgi
# the virtualenv (full path)
home            = /Path/sosaServer/venv

# process-related settings
# master
master          = true
# maximum number of worker processes
processes       = 10
# the socket (use the full path to be safe
socket          = /Path/sosaServer/sosaServer.sock
# ... with appropriate permissions - may be needed
# chmod-socket    = 664
# clear environment on exit
vacuum          = true
~~~

#### 11. 설정 완료.
```uwsgi --ini conf/sosaServer_uwsgi.ini```로 실행하면 된다.
