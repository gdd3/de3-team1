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
       echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-6.x.list
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
#### 3.8. Добавляем в автозагрузку Elasticsearch и проверяем статус:
       sudo systemctl enable elasticsearch.service
       sudo systemctl status elasticsearch.service
#### 3.9. Проверка elasticsearch
       curl localhost:9200/_cat/health?pretty
       curl localhost:9200/_cluster/health?pretty
       curl localhost:9200/_cat/indices?v

### 4. Установка Kibana:
#### 4.1. Импортируем Kibana public GPG key:
       wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
#### 4.2. Создаём Kibana source list:
       echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-6.x.list
#### 4.3. Обновляем репозиторий:
       sudo apt-get update
#### 4.4. Устанавливаем Kibana:
       sudo apt-get -y install kibana
#### 4.5. Правим конфиги Kibana:
       sudo vi /etc/kibana/kibana.yml
      Вместо:
       server.host: "0.0.0.0"
      Прописываем:
       server.host: "localhost"
#### 4.6. Рестартуем сервис:
       sudo service kibana restart
#### 4.7. Добавляем в автозагрузку Kibana и проверяем статус:
       sudo systemctl enable kibana.service
       sudo systemctl status kibana.service


### 5. Установка Apache Utilities:
#### 5.1. Обновляем репозиторий:
       sudo apt-get update
#### 5.2. Устанавливаем Apache Utilities:
       sudo apt-get install apache2-utils

### 6. Создание странички-прототипа:
#### 6.1. Создание директории /var/www/search:
       sudo mkdir /var/www/search
#### 6.2. Создание файла index.html в директории /var/www/search:
       sudo vi /var/www/search/index.html
#### 6.3. Заполняем файл index.html (подставляем своё доменное имя и название индекса):
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
    var searchHost = 'https://de3-01-elasticsearch.loveflorida88.online/silchenko/_search';
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
            'fields': [ 'name^2', 'annotation']
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
      output += '<h3>' + response.hits.hits[i]._source.name + '</h3>';
      output += response.hits.hits[i]._source.annotation + '</br>';
    }
    document.getElementById('total').innerHTML = '<h2>Showing ' + response.hits.hits.length + ' results</h2>';
    document.getElementById('hits').innerHTML = output;
  }
  doSearch('');
</script>
</body>
</html>
```

### 7. Установка Nginx:
#### 7.1. Устанавливаем Nginx:
       sudo apt-get install nginx
#### 7.2. Создаём kibanaadmin:
       sudo htpasswd -c /etc/nginx/htpasswd.users kibanaadmin
#### 7.3. Создаём папку и ключи:
          sudo mkdir /etc/nginx/ssl
          sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt
#### 7.4. Правим конфиги:
       sudo vi /etc/nginx/sites-available/default
#### 7.5. Прописываем (подставляем свои доменные имена):
```bash
server {

    root /var/www/search;
    server_name de3-01-search.loveflorida88.online www.de3-01-search.loveflorida88.online; 

    location / {
            index index.html;
            alias /var/www/search/;
            default_type text/html;
    }
}

server {

    # ssl configuration
    listen 443 ssl ;

    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;
    server_name de3-01-kibana.loveflorida88.online www.de3-01-kibana.loveflorida88.online;

    location / {
        proxy_pass http://localhost:5601;
        proxy_http_version 1.1;
        proxy_set_header upgrade $http_upgrade;
        proxy_set_header connection 'upgrade';
        proxy_set_header host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

server {

    # ssl configuration
    listen 443 ssl ;

    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;
    server_name de3-01-elasticsearch.loveflorida88.online www.de3-01-elasticsearch.loveflorida88.online;

    location / {
        proxy_pass http://localhost:9200;
        proxy_http_version 1.1;
        proxy_set_header upgrade $http_upgrade;
        proxy_set_header connection 'upgrade';
        proxy_set_header host $host;
        proxy_cache_bypass $http_upgrade;
        
        add_header 'Access-Control-Allow-Origin' "$http_origin";
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, DELETE, PUT';
        add_header 'Access-Control-Allow-Credentials' 'true';
        add_header 'Access-Control-Allow-Headers' 'User-Agent,Keep-Alive,Content-Type';
    }
}
```
#### 7.6. Привязываем домен и сертификат (меняем на свои доменные имена):
       sudo certbot --nginx -d de3-01-kibana.loveflorida88.online -d www.de3-01-kibana.loveflorida88.online
       sudo certbot --nginx -d de3-01-elasticsearch.loveflorida88.online -d www.de3-01-elasticsearch.loveflorida88.online
       sudo certbot --nginx -d de3-01-search.loveflorida88.online -d www.de3-01-search.loveflorida88.online
#### 7.7. Проверяем и рестартуем сервис:
       sudo nginx -t
       sudo nginx -s reload
       sudo service nginx restart
#### 7.8. Заходим и проверяем (подставляем свои доменные имена):
       https://de3-01-kibana.loveflorida88.online
       https://de3-01-elasticsearch.loveflorida88.online/silchenko/_search
       https://de3-01-search.loveflorida88.online

### 8. Установка Logstash
#### 8.1. Создаём Logstash source list:
       echo 'deb http://packages.elastic.co/logstash/2.2/debian stable main' | sudo tee /etc/apt/sources.list.d/logstash-2.2.x.list
#### 8.2. Обновляем репозиторий:
       sudo apt-get update
#### 8.3. Устанавливаем Logstash:
       sudo apt-get -y install kibana

### 9. Скачивание исходных данных:
#### 9.1. Создаём директорию для исходных данных:
       sudo mkdir /home/loveflorida88/input_data
#### 9.2. Скачивание item_details_full:
       wget "http://data.cluster-lab.com/data-newprolab-com/project02/item_details_full?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=HI36GTQZKTLEH30CJ443%2F20181013%2F%2Fs3%2Faws4_request&X-Amz-Date=20181013T103635Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=eb8d824e55bd0c50c4ea5adcc5a034f19a6bd1d51a0ada17f8ff3e92885e305f"
#### 9.3. Скачивание catalogs:
       wget "http://data.cluster-lab.com/data-newprolab-com/project02/catalogs?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=HI36GTQZKTLEH30CJ443%2F20181013%2F%2Fs3%2Faws4_request&X-Amz-Date=20181013T103619Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=a71f86444926896adcb545c9eb18a1417452db9a9587a3aa45d508c43b35ae77"
#### 9.4. Скачивание catalog_path:
       wget "http://data.cluster-lab.com/data-newprolab-com/project02/catalog_path?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=HI36GTQZKTLEH30CJ443%2F20181013%2F%2Fs3%2Faws4_request&X-Amz-Date=20181013T103555Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=1614d2c58972e0e4dcc459be3a548d6f31b21a049c7a72175d01d8208c74a24c"
#### 9.5. Скачивание ratings:
       wget "http://data.cluster-lab.com/data-newprolab-com/project02/ratings?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=HI36GTQZKTLEH30CJ443%2F20181013%2F%2Fs3%2Faws4_request&X-Amz-Date=20181013T103652Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=bfa043b8850d639c00764e49d6cd24ed4d0892054ade97552a6061396efe4a35"

### 10. Установка JQ и ESBULK:
#### 10.1. Устанавливаем JQ:
       sudo apt install jq
#### 10.2. Устанавливаем ESBULK:
       wget "https://github.com/miku/esbulk/releases/download/v0.5.1/esbulk_0.5.1_amd64.deb"
       sudo apt install ./esbulk_0.5.1_amd64.deb

### 11. Загрузка данных:
#### 11.1. Создаём индекс silchenko (меняем на своё название):
PUT silchenko
{
    "settings" : {
        "number_of_shards" : 1,
        "number_of_replicas": 0
    }
}
#### 11.2. Создаём маппинг silchenko_mapping.json (меняем на своё название):
{
    "properties" : {
        "annotation": {"type": "text"},
        "name": {"type": "keyword"},
        "author": {"type": "keyword"},
        "itemid": {"type": "integer"},
        "parent_id": {"type": "integer"},
        "rating": {"type": "double"},
        "catalogid": {"type": "integer"},
        "catalogpath": {"type": "text"}
        }
    }
}
#### 11.3. Загружаем рейтинги (меняем на свои названия файлов):
       cat ratings_original.json | esbulk -verbose -index silchenko -mapping silchenko_mapping.json
#### 11.4. Загружаем каталоги (меняем на свои названия файлов):
       cat catalog_original.json | esbulk -verbose -index silchenko -mapping silchenko_mapping.json
#### 11.5. Загружаем пути каталогов (меняем на свои названия файлов):
       cat catalog_path_original.json | \
       jq -c '.["catalogpath"] = (.catalogpath|tostring)' | \
       esbulk -verbose -index silchenko -mapping silchenko_mapping.json
#### 11.6. Загружаем предметы (меняем на свои названия файлов):
       cat item_details_full_original.json | \
       jq  -c '.["annotation"] = .attr0 | .["name"] = .attr1 | .["author"] = .attr2 | {annotation, name, author, itemid, parent_id}' | \
       esbulk -verbose -index item -mapping silchenko_mapping.json
