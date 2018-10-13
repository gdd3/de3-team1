# de3-team1-silchenko
### 1. Установка Java 8:
#### 1.1. Добавляем репозиторий:
       sudo add-apt-repository -y ppa:webupd8team/java
#### 1.2. Обновляем репозиторий:
       sudo apt-get update
#### 1.3. Устанавливаем Java 8:
       sudo apt-get -y install oracle-java8-installer

### 2. Устанавливаем Certbot
#### 2.1. Обновляем репозиторий:
           sudo apt-get update
#### 2.2. Добавляем репозиторий Certbot:
           sudo apt-get install software-properties-common
           sudo add-apt-repository ppa:certbot/certbot
#### 2.3. Обновляем репозиторий и устанавливаем Certbot
           sudo apt-get update
           sudo apt-get install python-certbot-nginx 

### 3. Установка Elasticsearch:
#### 3.1. Импортируем Elasticsearch public GPG key:
       wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
#### 3.2. Создаём Elasticsearch source list:
       echo "deb http://packages.elastic.co/elasticsearch/2.x/debian stable main" | sudo tee -a /etc/apt/sources.list.d/elasticsearch-2.x.list
#### 3.3. Обновляем репозиторий:
       sudo apt-get update
#### 3.4. Устанавливаем Elasticsearch:
       sudo apt-get -y install elasticsearch
#### 3.5. Правим конфиги Elasticsearch:
       sudo vi /etc/elasticsearch/elasticsearch.yml
      Вместо:
       network.host: 192.168.0.1
      Прописываем:
       network.host: localhost
#### 3.7. Рестартуем сервис:
       sudo service elasticsearch restart
#### 3.8. Добавляем в автозагрузку Elasticsearch:
       sudo update-rc.d elasticsearch defaults 95 10
#### 3.9. Проверка elasticsearch
           curl localhost:9200/_cat/health?pretty
           curl localhost:9200/_cluster/health?pretty
           curl localhost:9200/_cat/indices?v

### 4. Установка Kibana:
#### 4.1. Создаём Kibana source list:
       echo "deb http://packages.elastic.co/kibana/4.5/debian stable main" | sudo tee -a /etc/apt/sources.list.d/kibana-4.5.x.list
#### 4.2. Обновляем репозиторий:
       sudo apt-get update
#### 4.3. Устанавливаем Kibana:
       sudo apt-get -y install kibana
#### 4.4. Правим конфиги Kibana:
       sudo vi /opt/kibana/config/kibana.yml
      Вместо:
       server.host: "0.0.0.0"
      Прописываем:
       server.host: "localhost"
#### 4.6. Добавляем в автозагрузку Kibana:
       sudo update-rc.d kibana defaults 96 9
#### 4.7. Рестартуем сервис:
       sudo service kibana start

### 5. Установка Apache Utilities:
#### 5.1. Обновляем репозиторий:
       sudo apt-get update
#### 5.2. Устанавливаем Apache Utilities:
       sudo apt-get install apache2-utils

### 6. Установка Nginx:
#### 6.1. Устанавливаем Nginx:
       sudo apt-get install nginx
#### 6.2. Создаём kibanaadmin:
       sudo htpasswd -c /etc/nginx/htpasswd.users kibanaadmin
#### 6.3. Создаём папку и ключи:
          sudo mkdir /etc/nginx/ssl
          sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt
#### 6.4. Правим конфиги:
       sudo vi /etc/nginx/sites-available/default
#### 6.5. Прописываем (подставляем свой IP адрес):
```bash
server {
    listen       80 default_server;
    listen [::]:80 default_server;

    server_name https://35.204.41.3;
    ssl_certificate      /etc/nginx/ssl/nginx.crt;
    ssl_certificate_key  /etc/nginx/ssl/nginx.key;

    auth_basic "Restricted Access";
    auth_basic_user_file /etc/nginx/htpasswd.users;

    location / {
        proxy_pass http://localhost:5601;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```
#### 6.6. Привязываем домен и сертификат (меняем на свой купленный домен):
           sudo certbot --nginx -d de3-01.loveflorida88.online -d www.de3-01.loveflorida88.online
#### 6.7. Проверяем и рестартуем сервис:
       sudo nginx -t
       sudo nginx -s reload
       sudo service nginx restart
#### 6.8. Заходим и проверяем (подставляем свой купленный домен):
       https://de3-01.loveflorida88.online

### 7. Установка Logstash
#### 7.1. Создаём Logstash source list:
       echo 'deb http://packages.elastic.co/logstash/2.2/debian stable main' | sudo tee /etc/apt/sources.list.d/logstash-2.2.x.list
#### 7.2. Обновляем репозиторий:
       sudo apt-get update
#### 7.3. Устанавливаем Logstash:
       sudo apt-get -y install kibana

### 8. Скачивание исходных данных:
#### 8.1. Создаём директорию для исходных данных:
       sudo mkdir /home/loveflorida88/input_data
#### 8.2. Скачивание item_details_full:
       wget "http://data.cluster-lab.com/data-newprolab-com/project02/item_details_full?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=HI36GTQZKTLEH30CJ443%2F20181013%2F%2Fs3%2Faws4_request&X-Amz-Date=20181013T103635Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=eb8d824e55bd0c50c4ea5adcc5a034f19a6bd1d51a0ada17f8ff3e92885e305f"
#### 8.3. Скачивание catalogs:
       wget "http://data.cluster-lab.com/data-newprolab-com/project02/catalogs?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=HI36GTQZKTLEH30CJ443%2F20181013%2F%2Fs3%2Faws4_request&X-Amz-Date=20181013T103619Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=a71f86444926896adcb545c9eb18a1417452db9a9587a3aa45d508c43b35ae77"
#### 8.4. Скачивание catalog_path:
       wget "http://data.cluster-lab.com/data-newprolab-com/project02/catalog_path?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=HI36GTQZKTLEH30CJ443%2F20181013%2F%2Fs3%2Faws4_request&X-Amz-Date=20181013T103555Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=1614d2c58972e0e4dcc459be3a548d6f31b21a049c7a72175d01d8208c74a24c"
#### 8.5. Скачивание ratings:
       wget "http://data.cluster-lab.com/data-newprolab-com/project02/ratings?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=HI36GTQZKTLEH30CJ443%2F20181013%2F%2Fs3%2Faws4_request&X-Amz-Date=20181013T103652Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=bfa043b8850d639c00764e49d6cd24ed4d0892054ade97552a6061396efe4a35"

### 9. Создание странички-прототипа:
#### 9.1. Создание директории /var/www/search:
       sudo mkdir /var/www/search
#### 9.2. Создание файла index.html в директории /var/www/search:
       sudo vi /var/www/search/index.html
#### 9.3. Заполняем файл index.html (подставляем свой IP адрес и название индекса):
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Search demo site</title>
</head>
<body>
<h1>Elasticsearch client side demo</h1>
<div id="search_container">
    <label for"search">Search</label>
    <input type="text" id="search"/>
    <input type="submit" onclick="doSearch(document.getElementById('search').value);"/>
</div>
<div id="total"></div>
<div id="hits"></div>
<script type="application/javascript">
  function doSearch (needle) {
    var searchHost = 'http://35.204.41.3:9200/elasticsearch_index_silchenko_elastic/_search';
    var body = {
      'size': 10
    };
    if (needle.length !== 0) {
      var query = {
        'bool': {}
      };
      if (needle.length !== 0) {
        query.bool.must = {
          'multi_match': {
            'query': needle,
            'fields': [ 'title^2', 'summary_processed' ]
          }
        };
      }
      body.query = query;
    }

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open('POST', searchHost, false);
    xmlHttp.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    xmlHttp.send(JSON.stringify(body));
    var response = JSON.parse(xmlHttp.responseText);

    // Print results on screen.
    var output = '';
    for (var i = 0; i < response.hits.hits.length; i++) {
      output += '<h3>' + response.hits.hits[i]._source.title + '</h3>';
      output += response.hits.hits[i]._source.summary_processed[0] + '</br>';
    }
    document.getElementById('total').innerHTML = '<h2>Showing ' + response.hits.hits.length + ' results</h2>';
    document.getElementById('hits').innerHTML = output;
  }
  doSearch('');
</script>
</body>
</html>
```
#### 9.4. Правим конфиги:
       sudo vi /etc/nginx/sites-enabled/default
#### 9.5. Прописываем (подставляем свой IP адрес):
```bash
server {
     listen 80 default_server;
     listen [::]:80;
     server_name _;
     root /var/www/search;
          location / {
                  index index.html;
                  alias /var/www/search/;
                  default_type text/html;
          }
}
```
#### 9.6. Рестартуем сервис:
       sudo nginx -t
       sudo nginx -s reload
       sudo service nginx restart
#### 9.7. Заходим и проверяем (подставляем свой IP адрес):
       http://35.204.41.3
