# de3-team1-silchenko
1. Установка Java 8:
 1.1. Добавляем репозиторий:
       sudo add-apt-repository -y ppa:webupd8team/java
 1.2. Обновляем репозиторий:
       sudo apt-get update
 1.3. Устанавливаем Java 8:
       sudo apt-get -y install oracle-java8-installer

2. Установка Elasticsearch:
 2.1. Импортируем Elasticsearch public GPG key:
       wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
 2.2. Создаём Elasticsearch source list:
       echo "deb http://packages.elastic.co/elasticsearch/2.x/debian stable main" | sudo tee -a /etc/apt/sources.list.d/elasticsearch-2.x.list
 2.3. Обновляем репозиторий:
       sudo apt-get update
 2.4. Устанавливаем Elasticsearch:
       sudo apt-get -y install elasticsearch
 2.5. Правим конфиги Elasticsearch:
       sudo vi /etc/elasticsearch/elasticsearch.yml
 2.6. Вместо:
       network.host: 192.168.0.1
      прописываем:
      network.host: localhost
      # network.host: 35.204.41.3
 2.7. Рестартуем сервис:
       sudo service elasticsearch restart
 2.8. Добавляем в автозагрузку Elasticsearch:
       sudo update-rc.d elasticsearch defaults 95 10

3. Установка Kibana:
 3.1. Создаём Kibana source list:
       echo "deb http://packages.elastic.co/kibana/4.5/debian stable main" | sudo tee -a /etc/apt/sources.list.d/kibana-4.5.x.list
 3.2. Обновляем репозиторий:
       sudo apt-get update
 3.3. Устанавливаем Kibana:
       sudo apt-get -y install kibana
 3.4. Правим конфиги Kibana:
       sudo vi /opt/kibana/config/kibana.yml
 3.5. Вместо:
       server.host: "0.0.0.0"
      Прописываем:
      server.host: "localhost"
      # server.host: 35.204.41.3
 3.6. Добавляем в автозагрузку Kibana:
       sudo update-rc.d kibana defaults 96 9
 3.7. Рестартуем сервис:
       sudo service kibana start

4. Установка Apache Utilities:
 4.1. Обновляем репозиторий:
       sudo apt-get update
 4.2. Устанавливаем Apache Utilities:
       sudo apt-get install apache2-utils

5. Установка Nginx:
 5.1. Устанавливаем Nginx:
       sudo apt-get install nginx
 5.2. Создаём kibanaadmin:
       sudo htpasswd -c /etc/nginx/htpasswd.users kibanaadmin
 5.3. Правим конфиги:
       sudo vi /etc/nginx/sites-available/default
 5.4. Прописываем:
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
 5.5. Рестартуем сервис:
       sudo service nginx restart
 5.6. Заходим и проверяем:
       http://35.204.41.3

6. Установка Logstash
 6.1. Создаём Logstash source list:
       echo 'deb http://packages.elastic.co/logstash/2.2/debian stable main' | sudo tee /etc/apt/sources.list.d/logstash-2.2.x.list
 6.2. Обновляем репозиторий:
       sudo apt-get update
 6.3. Устанавливаем Logstash:
       sudo apt-get -y install kibana
 6.4. Настраиваем 