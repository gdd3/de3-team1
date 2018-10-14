## Настройка прокси сервера
У нас есть static ip и свое доменное имя www.de30pro.com. Чтобы не перенастраивать под каждую лабу статический ip на разные VM-ы, настроим отдельный прокси-сервер.

### Создаем новый инстанс на GCP
Заходим в раздел `Compute Engine`, далее в `VM Instances` и создаем VM f1-micro.
Заходим в раздел `VPC network`, далее в `External ip addresses` и назначаем новому экземпляру static ip.
Заходим в раздел `Network services`,  далее в `Cloud DNS` и добавляем записи для проксирования на 1ю лабу:
- project-1.de30pro.com
- www.project-1.de30pro.com

### Настройка и проверка прокси-сервера
Установим Certbot
```
    sudo apt-get update
    sudo apt-get install software-properties-common
    sudo add-apt-repository ppa:certbot/certbot
    sudo apt-get update
    sudo apt-get install python-certbot-nginx
```

Установим и настроим Nginx
```    sudo apt-get install nginx```

Создадим директорию, ключи, привяжем сертификат
```
    sudo mkdir /etc/nginx/ssl
    sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt
    sudo certbot --nginx -d project-1.de30pro.com -d www.project-1.de30pro.com
```

Проверим доступ к web-серверу извне
В браузере зайдем на страничку project-1.de30pro.com, прописанную в GCP Cloud DSN и убедимся что запрос приходит на nginx нашего нового прокси-сервера.

### ЧЕРНОВИК

Установим Apache utils
```    sudo apt-get install apache2-utils```

Правим конфиги
```
server {
    listen       80 default_server;
    listen [::]:80 default_server;

    server_name https://project-1.de30pro.com;
    ssl_certificate      /etc/nginx/ssl/nginx.crt;
    ssl_certificate_key  /etc/nginx/ssl/nginx.key;

    auth_basic "Restricted Access";
    auth_basic_user_file /etc/nginx/htpasswd.users;

    location / {
        proxy_pass http://localhost:5601; #добавить DNS-имя сервака с kibana
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```
