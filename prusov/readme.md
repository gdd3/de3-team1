## Настройка прокси сервера
У нас есть static ip и свое доменное имя [доменное имя]. Чтобы не перенастраивать под каждую лабу статический ip на разные VM-ы, настроим отдельный прокси-сервер.

### Создаем новый инстанс на GCP
Заходим в раздел `Compute Engine`, далее в `VM Instances` и создаем VM f1-micro.
Заходим в раздел `VPC network`, далее в `External ip addresses` и назначаем новому экземпляру static ip.
Заходим в раздел `Network services`,  далее в `Cloud DNS` и добавляем записи для сервера:
- project-1.de30pro.com
- www.project-1.de30pro.com

### Настройка и проверка nginx на прокси-сервере
Установим Certbot
    sudo apt-get update
    sudo apt-get install software-properties-common
    sudo add-apt-repository ppa:certbot/certbot
    sudo apt-get update
    sudo apt-get install python-certbot-nginx

Установим Apache utils
    sudo apt-get install apache2-utils

Установим и настроим Nginx
    sudo apt-get install nginx

Создадим директорию и ключи
    sudo mkdir /etc/nginx/ssl
    sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt
