## Установка ELK
### Установка Java 8
```
sudo add-apt-repository -y ppa:webupd8team/java
sudo apt-get update
sudo apt-get -y install oracle-java8-installer
```
### Установка Elastic search
```
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.4.2.tar.gz
tar -xvf elasticsearch-6.4.2.tar.gz
```
Запускаем
```
cd elasticsearch-6.4.2
./bin/elasticsearch
```

Проверяем работу сервиса
```
curl localhost:9200/_cat/health?pretty
curl localhost:9200/_cluster/health?pretty
curl localhost:9200/_cat/indices?v
```

## Установка Kibana
```
cd ~ls
wget https://artifacts.elastic.co/downloads/kibana/kibana-6.4.2-linux-x86_64.tar.gz
tar -xvf kibana-6.4.2-linux-x86_64.tar.gz
cd kibana-6.4.2-linux-x86_64
./bin/kibana
```

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

ssh -i ~/.ssh/okarin_private okarin@35.204.80.159
