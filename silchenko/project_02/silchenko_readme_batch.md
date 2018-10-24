# de3-team1-silchenko Batch Pipeline
### 1. Установка Java 8:
#### 1.1. Проверяем, установлена Java 8 или нет:
       java -version
#### 1.2. Добавляем репозиторий:
       sudo add-apt-repository -y ppa:webupd8team/java
#### 1.3. Обновляем репозиторий:
       sudo apt-get update
#### 1.4. Устанавливаем Java 8:
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

### 3. Установка Nginx:
#### 3.1. Устанавливаем Nginx:
       sudo apt-get install nginx
#### 3.2. Правим конфиги:
       sudo vi /etc/nginx/sites-available/default
#### 3.3. Прописываем (подставляем свои доменные имена и IP адреса):
```bash
server {

    # ssl configuration
    listen 443 ssl ;

    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;
    server_name de3-00-divolte.loveflorida88.online www.de3-00-divolte.loveflorida88.online;

    location / {
        proxy_pass http://104.199.38.155:8290/;
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
    server_name de3-00-ambari.loveflorida88.online www.de3-00-ambari.loveflorida88.online;

    location / {
        proxy_pass http://104.199.38.155:8080/;
        proxy_http_version 1.1;
        proxy_set_header upgrade $http_upgrade;
        proxy_set_header connection 'upgrade';
        proxy_set_header host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```
#### 3.4. Привязываем домен и сертификат (меняем на свои доменные имена):
       sudo certbot --nginx -d de3-00-ambari.loveflorida88.online -d www.de3-00-ambari.loveflorida88.online
       sudo certbot --nginx -d de3-00-divolte.loveflorida88.online -d www.de3-00-divolte.loveflorida88.online
#### 3.5. Проверяем и рестартуем сервис:
       sudo nginx -t
       sudo nginx -s reload
       sudo service nginx restart
#### 3.6. Заходим и проверяем (подставляем свои доменные имена):
       https://de3-00-ambari.loveflorida88.online

### 4. Установка Divolte:
#### 4.1. Качаем дистрибутив:
       https://divolte.io/
#### 4.2. Распаковываем в /opt/divolte/:
       tar -xzf divolte-collector-*.tar.gz
#### 4.3. Создаём файл divolte-collector.conf
       touch /opt/divolte/conf/divolte-collector.conf
#### 4.4. Создаём файл divolte-env.sh:
       cp /opt/divolte/conf/divolte-env.sh.example /opt/divolte/conf/divolte-env.sh
#### 4.5. Правим файл divolte-env.sh, добавляем:
       HADOOP_CONF_DIR=/etc/hadoop/conf
#### 4.6. Правим файл divolte-collector.conf, добавляем:
```bash
divolte {
  global {
    server {
      host = 0.0.0.0
      port = 8290
    }
    hdfs {
      client {
        fs.defaultFS = "hdfs://instance-1.europe-west1-b.c.pro-signal-218407.internal:8020/"
      }
      // Enable HDFS sinks.
      enabled = true

      // Use multiple threads to write to HDFS.
      threads = 2
    }
    kafka {
      // If true, flushing to Kafka is enabled.
      enabled = true

      // Number of threads to use for flushing events to Kafka
      threads = 2

      // The maximum queue of mapped events to buffer before
      // starting to drop new ones. Note that when this buffer is full,
      // events are dropped and a warning is logged. No errors are reported
      // to the source of the events. A single buffer is shared between all
      // threads, and its size will be rounded up to the nearest power of 2.
      buffer_size = 1048576

      // All settings in here are used as-is to configure
      // the Kafka producer.
      // See: http://kafka.apache.org/082/documentation.html#newproducerconfigs
      producer = {
        bootstrap.servers = ["instance-1.europe-west1-b.c.pro-signal-218407.internal:6667"]
        client.id = divolte.collector

        acks = 1
        retries = 0
        // compression.type = lz4
        max.in.flight.requests.per.connection = 1
      }
    }
  }
  
  sinks {
    // The name of the sink. (It's referred to by the mapping.)
    hdfs {
      type = hdfs

      // For HDFS sinks we can control how the files are created.
      file_strategy {
        // Create a new file every hour
        roll_every = 1 hour

        // Perform a hsync call on the HDFS files after every 1000 records are written
        // or every 5 seconds, whichever happens first.

        // Performing a hsync call periodically can prevent data loss in the case of
        // some failure scenarios.
        sync_file_after_records = 1000
        sync_file_after_duration = 5 seconds

        // Files that are being written will be created in a working directory.
        // Once a file is closed, Divolte Collector will move the file to the
        // publish directory. The working and publish directories are allowed
        // to be the same, but this is not recommended.
        working_dir = "/divolte/inflight"
        publish_dir = "/divolte/published"
      }

      // Set the replication factor for created files.
      replication = 3
    }
  
  kafka {
      type = kafka

      // This is the name of the topic that data will be produced on
      topic = egor.silchenko
    }
  }
  
  mappings {
    my_mapping = {
      schema_file = "/opt/divolte/conf/CheckoutEvent.avsc"
      mapping_script_file = "/opt/divolte/conf/mapping.groovy"
      sources = [browser]
      sinks = [kafka, hdfs]
    }
  }
  
  sources {
    browser {
      type = browser
    }
  }
}
```
#### 4.7. Создаём файл CheckoutEvent.avsc:
       touch /opt/divolte/conf/CheckoutEvent.avsc
#### 4.8. Добавляем туда:
```bash
{
    "namespace": "io.divolte.record",
    "type": "record",
    "name": "CheckoutEventRecord",
    "fields": [
        { "name": "detectedDuplicate",       "type": "boolean" },
        { "name": "detectedCorruption",      "type": "boolean" },
        { "name": "firstInSession",          "type": "boolean" },
        { "name": "timestamp",               "type": "long" },
        { "name": "remoteHost",              "type": "string" },
        { "name": "referer",                 "type": ["null", "string"], "default": null },
        { "name": "location",                "type": ["null", "string"], "default": null },
        { "name": "viewportPixelWidth",      "type": ["null", "int"],    "default": null },
        { "name": "viewportPixelHeight",     "type": ["null", "int"],    "default": null },
        { "name": "screenPixelWidth",        "type": ["null", "int"],    "default": null },
        { "name": "screenPixelHeight",       "type": ["null", "int"],    "default": null },
        { "name": "partyId",                 "type": ["null", "string"], "default": null },
        { "name": "sessionId",               "type": ["null", "string"], "default": null },
        { "name": "pageViewId",              "type": ["null", "string"], "default": null },
        { "name": "eventType",               "type": "string",           "default": "unknown" },
        { "name": "userAgentString",         "type": ["null", "string"], "default": null },
        { "name": "userAgentName",           "type": ["null", "string"], "default": null },
        { "name": "userAgentFamily",         "type": ["null", "string"], "default": null },
        { "name": "userAgentVendor",         "type": ["null", "string"], "default": null },
        { "name": "userAgentType",           "type": ["null", "string"], "default": null },
        { "name": "userAgentVersion",        "type": ["null", "string"], "default": null },
        { "name": "userAgentDeviceCategory", "type": ["null", "string"], "default": null },
        { "name": "userAgentOsFamily",       "type": ["null", "string"], "default": null },
        { "name": "userAgentOsVersion",      "type": ["null", "string"], "default": null },
        { "name": "userAgentOsVendor",       "type": ["null", "string"], "default": null },
        { "name": "price",                   "type": ["null", "string"], "default": null }
    ]
}
```
#### 4.9. Создаём файл mapping.groovy:
       touch /opt/divolte/conf/mapping.groovy
#### 4.10. Добавляем туда:
```bash
mapping {
    map duplicate() onto 'detectedDuplicate'
    map corrupt() onto 'detectedCorruption'
    map firstInSession() onto 'firstInSession'
    map timestamp() onto 'timestamp'
    map remoteHost() onto 'remoteHost'
    map referer() onto 'referer'
    map location() onto 'location'
    map viewportPixelWidth() onto 'viewportPixelWidth'
    map viewportPixelHeight() onto 'viewportPixelHeight'
    map screenPixelWidth() onto 'screenPixelWidth'
    map screenPixelHeight() onto 'screenPixelHeight'
    map partyId() onto 'partyId'
    map sessionId() onto 'sessionId'
    map pageViewId() onto 'pageViewId'
    map eventType() onto 'eventType'

    map userAgentString() onto 'userAgentString'
    def ua = userAgent()
    map ua.name() onto 'userAgentName'
    map ua.family() onto 'userAgentFamily'
    map ua.vendor() onto 'userAgentVendor'
    map ua.type() onto 'userAgentType'
    map ua.version() onto 'userAgentVersion'
    map ua.deviceCategory() onto 'userAgentDeviceCategory'
    map ua.osFamily() onto 'userAgentOsFamily'
    map ua.osVersion() onto 'userAgentOsVersion'
    map ua.osVendor() onto 'userAgentOsVendor'

    map eventParameter('price') onto 'price'
}
```
#### 4.11. Создаём рабочие директории в HDFS:
       sudo su hdfs
       hdfs dfs -mkdir /divolte
       hdfs dfs -mkdir /divolte/inflight
       hdfs dfs -mkdir /divolte/published
       hdfs dfs -chmod -R 0777 /divolte
#### 4.12. Добавляем скрипт на сайт:
```bash
<script src="https://de3-00-divolte.loveflorida88.online/divolte.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script>
    $(document).ready(function() {
      $('.basket-btn-checkout').click(function() {
        var price_text = $('.basket-coupon-block-total-price-current').first().text().match(/\d+/g).map(Number).join('');
        // console.log(price_text);
        divolte.signal('checkoutEvent', { price: price_text });
      });
    });
</script>
```
#### 4.13. Запускаем Divolte
       /opt/divolte/bin/divolte-collector
#### 4.14. Проверяем Divolte
       https://de3-00-divolte.loveflorida88.online/divolte.js
       /usr/hdp/3.0.0.0-1634/kafka/bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic egor.silchenko

### 1. Установка PostgreSQL:
#### 1.1. Импортируем PostgreSQL public GPG key:
       wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
#### 1.2. Выполняем команду и запоминаем результат:
       lsb_release -cs
#### 1.3. Создаём файл /etc/apt/sources.list.d/pgdg.list:
       sudo vi /etc/apt/sources.list.d/pgdg.list
#### 1.4. Помещаем туда строчку, подставив результат команды из шага 1.2.:
       deb http://apt.postgresql.org/pub/repos/apt/  результат команды-pgdg main
      Пример:
       deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main
#### 1.5. Обновляем репозиторий:
       sudo apt-get update
#### 1.6. Устанавливаем PostgreSQL:
       sudo apt-get install postgresql-10 pgadmin4

### 2. Создание пользователя, базы данных и таблицы:
#### 2.1. Создание пользователя:
       sudo -u postgres createuser --interactive
#### 2.2. Создание базы данных (меняем на свою):
       sudo -u postgres createdb loveflorida88
#### 2.3. Задаём пароль позователю (меняем на своего пользователя и на свой пароль):
       alter user loveflorida88 with password 'пароль';
#### 2.4. Создание таблицы (меняем на свою):
```sql
create table silchenko (
    id int generated by default as identity primary key,
    ingested_at timestamp default current_timestamp,
    annotation text,
    name text,
    author text,
    itemid text,
    parent_id text,
    rating text,
    catalogid text,
    catalogpath text
);
```
#### 2.5. Создание и загрузка таблицы рейтингов (меняем на свою):
```sql
create table ratings (
    id int generated by default as identity primary key,
    ingested_at timestamp default current_timestamp,
    data jsonb not null
);
create index ratings_gin_idx on ratings using gin(data);
```
      Загрузка:
       cat ratings_original.json | psql -h localhost -p 5432 loveflorida88 -c "COPY ratings (data) FROM STDIN;"
