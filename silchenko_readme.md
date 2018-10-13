# de3-team1-silchenko
### 1. Установка Java 8:
#### 1.1. Добавляем репозиторий:
       sudo add-apt-repository -y ppa:webupd8team/java
#### 1.2. Обновляем репозиторий:
       sudo apt-get update
#### 1.3. Устанавливаем Java 8:
       sudo apt-get -y install oracle-java8-installer

### 2. Установка Elasticsearch:
#### 2.1. Импортируем Elasticsearch public GPG key:
       wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
#### 2.2. Создаём Elasticsearch source list:
       echo "deb http://packages.elastic.co/elasticsearch/2.x/debian stable main" | sudo tee -a /etc/apt/sources.list.d/elasticsearch-2.x.list
#### 2.3. Обновляем репозиторий:
       sudo apt-get update
#### 2.4. Устанавливаем Elasticsearch:
       sudo apt-get -y install elasticsearch
#### 2.5. Правим конфиги Elasticsearch:
       sudo vi /etc/elasticsearch/elasticsearch.yml
      Вместо:
       network.host: 192.168.0.1
      Прописываем:
       network.host: localhost
#### 2.7. Рестартуем сервис:
       sudo service elasticsearch restart
#### 2.8. Добавляем в автозагрузку Elasticsearch:
       sudo update-rc.d elasticsearch defaults 95 10

### 3. Установка Kibana:
#### 3.1. Создаём Kibana source list:
       echo "deb http://packages.elastic.co/kibana/4.5/debian stable main" | sudo tee -a /etc/apt/sources.list.d/kibana-4.5.x.list
#### 3.2. Обновляем репозиторий:
       sudo apt-get update
#### 3.3. Устанавливаем Kibana:
       sudo apt-get -y install kibana
#### 3.4. Правим конфиги Kibana:
       sudo vi /opt/kibana/config/kibana.yml
      Вместо:
       server.host: "0.0.0.0"
      Прописываем:
       server.host: "localhost"
#### 3.6. Добавляем в автозагрузку Kibana:
       sudo update-rc.d kibana defaults 96 9
#### 3.7. Рестартуем сервис:
       sudo service kibana start

### 4. Установка Apache Utilities:
#### 4.1. Обновляем репозиторий:
       sudo apt-get update
#### 4.2. Устанавливаем Apache Utilities:
       sudo apt-get install apache2-utils

### 5. Установка Nginx:
#### 5.1. Устанавливаем Nginx:
       sudo apt-get install nginx
#### 5.2. Создаём kibanaadmin:
       sudo htpasswd -c /etc/nginx/htpasswd.users kibanaadmin
#### 5.3. Правим конфиги:
       sudo vi /etc/nginx/sites-available/default
#### 5.4. Прописываем (подставляем свой IP адрес):
```
server {
    listen 80;

   # server_name https://35.204.41.3;
    server_name 35.204.41.3;

    auth_basic "Restricted Access";
    auth_basic_user_file /etc/nginx/htpasswd.users;

    location / {
       # proxy_pass http://35.204.41.3:5601;
        proxy_pass http://localhost:5601;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```
#### 5.5. Рестартуем сервис:
       sudo service nginx restart
#### 5.6. Заходим и проверяем (подставляем свой IP адрес):
       http://35.204.41.3

### 6. Установка Logstash
#### 6.1. Создаём Logstash source list:
       echo 'deb http://packages.elastic.co/logstash/2.2/debian stable main' | sudo tee /etc/apt/sources.list.d/logstash-2.2.x.list
#### 6.2. Обновляем репозиторий:
       sudo apt-get update
#### 6.3. Устанавливаем Logstash:
       sudo apt-get -y install kibana
#### 6.4. Настраиваем 

### 7. Скачивание исходных данных:
#### 7.1. Скачивание item_details_full:
       wget "http://data.cluster-lab.com/data-newprolab-com/project02/item_details_full?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=HI36GTQZKTLEH30CJ443%2F20181013%2F%2Fs3%2Faws4_request&X-Amz-Date=20181013T103635Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=eb8d824e55bd0c50c4ea5adcc5a034f19a6bd1d51a0ada17f8ff3e92885e305f"
#### 7.2. Скачивание catalogs:
       wget "http://data.cluster-lab.com/data-newprolab-com/project02/catalogs?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=HI36GTQZKTLEH30CJ443%2F20181013%2F%2Fs3%2Faws4_request&X-Amz-Date=20181013T103619Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=a71f86444926896adcb545c9eb18a1417452db9a9587a3aa45d508c43b35ae77"
#### 7.3. Скачивание catalog_path:
       wget "http://data.cluster-lab.com/data-newprolab-com/project02/catalog_path?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=HI36GTQZKTLEH30CJ443%2F20181013%2F%2Fs3%2Faws4_request&X-Amz-Date=20181013T103555Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=1614d2c58972e0e4dcc459be3a548d6f31b21a049c7a72175d01d8208c74a24c"
#### 7.4. Скачивание ratings:
       wget "http://data.cluster-lab.com/data-newprolab-com/project02/ratings?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=HI36GTQZKTLEH30CJ443%2F20181013%2F%2Fs3%2Faws4_request&X-Amz-Date=20181013T103652Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=bfa043b8850d639c00764e49d6cd24ed4d0892054ade97552a6061396efe4a35"

### 8. Создание странички-прототипа:
#### 8.1. Создание директории /var/www/search:
       sudo mkdir /var/www/search
#### 8.2. Создание файла index.html в директории /var/www/search:
       sudo vi /var/www/search/index.html
#### 8.3. Заполняем файл index.html (подставляем свой IP адрес):
```
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
    var searchHost = 'http://35.204.41.3:9200/elasticsearch_index_draco_elastic/_search';
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