# de3-team1-silchenko Stream Pipeline
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
    server_name de3-03-divolte.loveflorida88.online www.de3-03-divolte.loveflorida88.online;

    location / {
        proxy_pass http://35.204.41.3:8290/;
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
    server_name de3-03-kafka.loveflorida88.online www.de3-03-kafka.loveflorida88.online;

    location / {
        proxy_pass http://35.204.41.3:9092/;
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
    server_name de3-03-spark.loveflorida88.online www.de3-03-spark.loveflorida88.online;

    location / {
        proxy_pass http://35.204.41.3:8080/;
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
    server_name de3-03-superset.loveflorida88.online www.de3-03-superset.loveflorida88.online;

    location / {
        proxy_pass http://35.204.41.3:8088/;
        proxy_http_version 1.1;
        proxy_set_header upgrade $http_upgrade;
        proxy_set_header connection 'upgrade';
        proxy_set_header host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```
#### 3.4. Привязываем домен и сертификат (меняем на свои доменные имена):
       sudo certbot --nginx -d de3-03-spark.loveflorida88.online -d www.de3-03-spark.loveflorida88.online
       sudo certbot --nginx -d de3-03-divolte.loveflorida88.online -d www.de3-03-divolte.loveflorida88.online
       sudo certbot --nginx -d de3-03-kafka.loveflorida88.online -d www.de3-03-kafka.loveflorida88.online
       sudo certbot --nginx -d de3-03-superset.loveflorida88.online -d www.de3-03-superset.loveflorida88.online
#### 3.5. Проверяем и рестартуем сервис:
       sudo nginx -t
       sudo nginx -s reload
       sudo service nginx restart

### 4. Установка Divolte:
#### 4.1. Качаем дистрибутив:
       https://divolte.io/
#### 4.2. Распаковываем в /opt/divolte/:
       tar -xzf divolte-collector-*.tar.gz
#### 4.3. Создаём файл divolte-collector.conf
       touch /opt/divolte-collector-0.9.0/conf/divolte-collector.conf
#### 4.4. Создаём файл divolte-env.sh:
       cp /opt/divolte-collector-0.9.0/conf/divolte-env.sh.example /opt/divolte-collector-0.9.0/conf/divolte-env.sh
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
        bootstrap.servers = ["instance-5.europe-west4-a.c.pro-signal-218407.internal:9092"]
        client.id = divolte.collector

        acks = 1
        retries = 0
        compression.type = none
        max.in.flight.requests.per.connection = 1
      }
    }
  }
  
  sinks {
    // The name of the sink. (It's referred to by the mapping.)
    kafka {
      type = kafka

      // This is the name of the topic that data will be produced on
      topic = user_event
    }
  }
  
  mappings {
    my_mapping = {
      schema_file = "/opt/divolte-collector-0.9.0/conf/user_event.avsc"
      mapping_script_file = "/opt/divolte-collector-0.9.0/conf/mapping_user_event.groovy"
      sources = [browser]
      sinks = [kafka]
    }
  }
  
  sources {
    browser {
      type = browser
    }
  }
}
```
#### 4.7. Создаём файл user_event.avsc:
       touch /opt/divolte-collector-0.9.0/conf/user_event.avsc
#### 4.8. Добавляем туда:
```bash
{
    "doc": "user_event",
    "type" : "record",
    "name" : "user_event",
    "namespace" : "user_event",
    "fields" : [
        {"name" : "detectedDuplicate",  "type" : "boolean"},
        {"name" : "detectedCorruption", "type" : "boolean"},
        {"name" : "firstInSession",     "type" : "boolean"},
        {"name" : "timestamp",          "type" : "long"},
        {"name" : "clientTimestamp",    "type" : "long"},
        {"name" : "remoteHost",         "type" : "string"},
        {"name" : "referer",            "type" : ["null", "string"], "default": null },
        {"name" : "location",           "type" : ["null", "string"], "default": null },
        {"name" : "partyId",            "type" : ["null", "string"], "default": null },
        {"name" : "sessionId",          "type" : ["null", "string"], "default": null },
        {"name" : "pageViewId",         "type" : ["null", "string"], "default": null },
        {"name" : "eventType",          "type" : "string",           "default": "unknown"},
        {"name" : "basket_price",       "type" : ["null", "string"], "default": null },
        {"name" : "item_id",            "type" : ["null", "string"], "default": null },
        {"name" : "item_price",         "type" : ["null", "string"], "default": null },
        {"name" : "item_url",           "type" : ["null", "string"], "default": null }
    ]
}
```
#### 4.9. Создаём файл mapping_user_event.groovy:
       touch /opt/divolte-collector-0.9.0/conf/mapping_user_event.groovy
#### 4.10. Добавляем туда:
```bash
mapping {
    map duplicate() onto 'detectedDuplicate'
    map corrupt() onto 'detectedCorruption'
    map firstInSession() onto 'firstInSession'
    map timestamp() onto 'timestamp'
    map clientTimestamp() onto 'clientTimestamp'
    map remoteHost() onto 'remoteHost'
    map referer() onto 'referer'
    map location() onto 'location'
    map partyId() onto 'partyId'
    map sessionId() onto 'sessionId'
    map pageViewId() onto 'pageViewId'
    map eventType() onto 'eventType'
    map eventParameter('basket_price') onto 'basket_price'
    map eventParameter('item_id') onto 'item_id'
    map eventParameter('item_price') onto 'item_price'
    map eventParameter('item_url') onto 'item_url'
}
```
#### 4.11. Добавляем скрипт на сайт:
```bash
<script src="https://de3-03-divolte.loveflorida88.online/divolte.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script>
      $(document).ready(function() {
        $('.basket-btn-checkout').click(function() {
          var basket_price = $('.basket-coupon-block-total-price-current').first().text().match(/\d+/g).join('');
          divolte.signal('checkoutEvent', { basket_price: basket_price });
        });

      $('.product-item-image-wrapper').click(function() {
        var item_container = $(this).closest('.product-item-container');
        var item_id = item_container.attr("id");
        var item_price = $('.product-item-price-current', item_container).first().text().match(/\d+/g).join('');
        var item_url = $(this).attr("href");
        divolte.signal('itemViewEvent', {
            item_id: item_id,
            item_price: item_price,
            item_url: item_url
          }
        );
      });

      $('.product-item-title a').click(function() {
        var item_container = $(this).closest('.product-item-container');
        var item_id = item_container.attr("id");
        var item_price = $('.product-item-price-current', item_container).first().text().match(/\d+/g).join('');
        var item_url = $(this).attr("href");
        divolte.signal('itemViewEvent', {
            item_id: item_id,
            item_price: item_price,
            item_url: item_url
          }
        );
      });

      $('.product-item-button-container').click(function() {
        var item_container = $(this).closest('.product-item-container');
        var item_id = item_container.attr("id");
        var item_price = $('.product-item-price-current', item_container).first().text().match(/\d+/g).join('');
        var item_url = $('.product-item-image-wrapper', item_container).attr("href");
        divolte.signal('itemBuyEvent', {
            item_id: item_id,
            item_price: item_price,
            item_url: item_url
          }
        );
      });

      $('.btn.btn-primary.product-item-detail-buy-button').click(function() {
        var item_id = $('.bx-catalog-element.bx-vendor').attr("id");
        var item_price = $('.product-item-detail-price-current').first().text().match(/\d+/g).join('');
        var item_url = $(location).attr("href");
        divolte.signal('itemBuyEvent', {
            item_id: item_id,
            item_price: item_price,
            item_url: item_url
          }
        );
      });

    });
</script>
```
#### 4.12. Запускаем Divolte
       /opt/divolte-collector-0.9.0/bin/divolte-collector
#### 4.13. Проверяем Divolte
       https://de3-03-divolte.loveflorida88.online/divolte.js
       /home/kafka/kafka/bin/kafka-console-consumer.sh --bootstrap-server instance-5.europe-west4-a.c.pro-signal-218407.internal:9092 --topic user_event --from-beginning

### 5. Установка Spark:
#### 5.1. Скачиваем Spark:
       wget "http://mirror.linux-ia64.org/apache/spark/spark-2.2.2/spark-2.2.2-bin-hadoop2.7.tgz"
#### 5.2. Устанавливаем Spark:
       tar -xvf spark-2.2.2-bin-hadoop2.7.tgz
       sudo mv spark-2.2.2-bin-hadoop2.7 /opt/
       cd /opt/spark-2.2.2-bin-hadoop2.7
#### 5.3. Добавляем переменные в .bash_profile:
       export SPARK_HOME=/usr/local/spark
#### 5.4. Запускаем Spark:
       $SPARK_HOME/sbin/start-master.sh
       $SPARK_HOME/sbin/start-slave.sh spark://ethane:7077
#### 5.5. Проверяем web:
       https://de3-03-spark.loveflorida88.online/
#### 5.6. Запуск spark-shell:
       $SPARK_HOME/bin/spark-shell
       $SPARK_HOME/bin/pyspark
#### 5.7. Остановка Spark:
       $SPARK_HOME/sbin/stop-slave.sh
       $SPARK_HOME/sbin/stop-master.sh

### 6. Установка PostgreSQL:
#### 6.1. Импортируем PostgreSQL public GPG key:
       wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
#### 6.2. Выполняем команду и запоминаем результат:
       lsb_release -cs
#### 6.3. Создаём файл /etc/apt/sources.list.d/pgdg.list:
       sudo vi /etc/apt/sources.list.d/pgdg.list
#### 6.4. Помещаем туда строчку, подставив результат команды из шага 1.2.:
       deb http://apt.postgresql.org/pub/repos/apt/  результат команды-pgdg main
      Пример:
       deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main
#### 6.5. Обновляем репозиторий:
       sudo apt-get update
#### 6.6. Устанавливаем PostgreSQL:
       sudo apt-get install postgresql-10 pgadmin4
#### 6.7. Добавляем в автозагрузку PostgreSQL и проверяем статус:
       sudo systemctl enable postgresql@10-main.service
       sudo systemctl status postgresql@10-main.service

### 7. Установка Superset:
#### 7.1. Ставим Python 3.6:
       sudo apt-get install python3.6
#### 7.2. Ставим все зависимые пакеты для Python 3.6:
       sudo apt install python3-pip
       sudo apt-get install build-essential libssl-dev libffi-dev libsasl2-dev libldap2-dev python3.6-dev
       python3.6 -m pip install cryptography psycopg2
#### 7.3. Ставим Superset:
       python3.6 -m pip install superset
#### 7.4. Создаём админа для Superset:
       ~/.local/bin/fabmanager create-admin --app superset
#### 7.5. Инициализируем базу данных:
       ~/.local/bin/superset db upgrade
#### 7.6. Подгружаем тестовые данные:
       ~/.local/bin/superset load_examples
#### 7.7. Создаём стандартные роли и права:
       ~/.local/bin/superset init
#### 7.8. Стартуем веб-сервер:
       ~/.local/bin/superset runserver -d
#### 7.9. Проверяем веб-сервер:
       http://35.204.41.3:8088
#### 7.10. Добавляем нашу базу:
       postgresql+psycopg2://loveflorida88:XXXXXXXXXX@localhost/loveflorida88

----------------------------------------------------------------------------------------------------
### 6. Создание пользователя, базы данных и таблицы:
#### 6.1. Создание пользователя:
       sudo -u postgres createuser --interactive
#### 6.2. Создание базы данных (меняем на свою):
       sudo -u postgres createdb loveflorida88
#### 6.3. Задаём пароль позователю (меняем на своего пользователя и на свой пароль):
       alter user loveflorida88 with password 'пароль';
#### 6.4. Создание таблиц user_event (меняем на свою):
```sql
create table stg_user_event_json (
    data_id int generated by default as identity primary key,
    load_data_timestamp timestamp default current_timestamp,
    data jsonb not null
);

create table stg_user_event (
    detected_duplicate text,
    detected_corruption text,
    first_in_session text,
    timestamp bigint,
    client_timestamp text,
    remote_host text,
    referer text,
    location text,
    party_id text,
    session_id text,
    page_view_id text,
    event_type text,
    basket_price text,
    item_id text,
    item_price text,
    item_url text
);
create index stg_user_event_idx on stg_user_event (timestamp desc);

```
#### 6.5. Загрузка таблиц user_event (меняем на свою):
      Загрузка stg_user_event_json:
       python3 user_event_consumer.py | psql "user=loveflorida88 password=пароль host=localhost port=5432 sslmode=require" -c "COPY stg_user_event_json (data) FROM STDIN;"
Загрузка stg_user_event:
```sql
insert into stg_user_event
select
  data->>'detectedCorruption' as detected_corruption,
  data->>'detectedDuplicate' as detected_duplicate,
  data->>'firstInSession' as first_in_session,
  (data->>'timestamp') ::bigint as timestamp,
  data->>'clientTimestamp' as client_timestamp,
  data->>'remoteHost' as remote_host,
  data->>'referer' as referer,
  data->>'location' as location,
  data->>'partyId' as party_id,
  data->>'sessionId' as session_id,
  data->>'pageViewId' as page_view_id,
  data->>'eventType' as event_type,
  data->>'basket_price' as basket_price,
  data->>'item_id' as item_id,
  data->>'item_price' as item_price,
  data->>'item_url' as item_url
from stg_user_event_json;

delete from stg_user_event_json;
```
#### 6.5. Делаем функцию для orders, которую будем вызывать через Postgrest:
```sql
create or replace function orders(in_timestamp bigint)
  returns table (item_url text, item_id text, item_cnt bigint, item_sum bigint)
as
$body$
  select
      item_url
    , regexp_replace(regexp_replace(item_url, 'https://b24-z2eha2.bitrix24.shop/katalog/item/', ''), '/', '') as item_id
    , count(*) as item_cnt
    , sum(item_price ::int) as item_sum
    from stg_user_event
  where event_type = 'itemBuyEvent'
    and timestamp >= $1
  group by item_url;
$body$
language sql;
```
#### 6.6. Делаем функцию для users, которую будем вызывать через Postgrest:
```sql
create or replace function users(in_timestamp bigint)
  returns table (item_url text, item_id text, view_item_count bigint, view_item_deep numeric)
as
$body$
  select
      x.item_url
    , x.item_id
    , count (*) as view_item_count
    , avg(sess_item_view_deep) as view_item_deep
    from (
      select
          timestamp
        , session_id
        , item_url
        , event_type
        , regexp_replace(regexp_replace(item_url, 'https://b24-z2eha2.bitrix24.shop/katalog/item/', ''), '/', '') as item_id
        , row_number() over (partition by session_id, item_url, event_type order by timestamp ) sess_item_view_cnt
        , row_number() over (partition by session_id order by timestamp) as sess_item_view_deep
        from stg_user_event
       where 1 = 1
         and timestamp >= $1
      order by timestamp) as x
   where x.event_type = 'itemViewEvent'
  group by x.item_url, x.item_id
  order by x.item_url;
$body$
language sql;
```

### 7. Установка PostgREST:
#### 7.1. Качаем последнюю версию PostgREST:
       wget "https://github.com/PostgREST/postgrest/releases/download/v5.1.0/postgrest-v5.1.0-ubuntu.tar.xz"
#### 7.2. Устанавливаем в /opt/postgrest:
       tar Jxf postgrest-v5.1.0-ubuntu.tar.xz
#### 7.3. Создаём файлик api.conf:
       db-uri = "postgres://юзер:пароль@localhost/база"
       db-schema = "public"
       db-anon-role = "роль"
#### 7.4. Создаём файлик run_postgrest.sh и добавляем:
       /opt/postgrest/postgrest /opt/postgrest/api.conf
#### 7.5. Создаём файлик postgrest.service в директории /lib/systemd/system/ и добавляем:
```bash
[Unit]
Description=PostgREST

[Service]
ExecStart=/bin/bash /opt/postgrest/run_postgrest.sh

[Install]
WantedBy=multi-user.target
```
#### 7.5. Ставим на автозагрузку:
       sudo systemctl enable postgrest.service
       sudo systemctl status postgrest.service

### 8. Установка Flask:
#### 8.1. Ставим Flask:
       pip3 install flask
#### 8.2. Создаём скрипт для flask (меняем на свои ссылки и параметры) api.py:
```python
import requests
import json
import time
import datetime
from flask import Flask, abort, jsonify


app = Flask(__name__)
app.config["POSTGREST_API_URL"] = "http://localhost:3000/rpc/"


@app.route("/")
def hello():
    return "Это API для чекера!"


@app.route("/api/v1.0/orders/<int:timestamp>", methods=["GET"])
def get_orders(timestamp):
    if timestamp < 940312918:
        abort(404)
    json_data = {"in_timestamp":str(timestamp)}
    headers = {"Content-Type": "application/json"}
    url = app.config["POSTGREST_API_URL"]+"orders"
    res = requests.post(
        url=url,
        data=json.dumps(json_data),
        headers=headers,
    )
    data = {
        "timestamp": timestamp,
        "contents": json.loads(res.text),
        "check": True,
    }
    return jsonify(data)


@app.route("/api/v1.0/orders/", methods=["GET"])
def get_orders_hour_ago():
    hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
    timestamp = int(
        time.mktime(hour_ago.timetuple()) * 1e3 + hour_ago.microsecond / 1e3
    )
    json_data = {"in_timestamp":str(timestamp)}
    headers = {"Content-Type": "application/json"}
    url = app.config["POSTGREST_API_URL"]+"orders"
    res = requests.post(
        url=url,
        data=json.dumps(json_data),
        headers=headers,
    )
    data = {
        "timestamp": timestamp,
        "contents": json.loads(res.text),
        "check": True,
    }
    return jsonify(data)


@app.route("/api/v1.0/users/<int:timestamp>", methods=["GET"])
def get_users(timestamp):
    if timestamp < 940312918:
        abort(404)
    json_data = {"in_timestamp":str(timestamp)}
    headers = {"Content-Type": "application/json"}
    url = app.config["POSTGREST_API_URL"]+"users"
    res = requests.post(
        url=url,
        data=json.dumps(json_data),
        headers=headers,
    )
    data = {
        "timestamp": timestamp,
        "contents": json.loads(res.text),
        "check": True,
    }
    return jsonify(data)


@app.route("/api/v1.0/users/", methods=["GET"])
def get_users_hour_ago():
    hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
    timestamp = int(
        time.mktime(hour_ago.timetuple()) * 1e3 + hour_ago.microsecond / 1e3
    )
    json_data = {"in_timestamp":str(timestamp)}
    headers = {"Content-Type": "application/json"}
    url = app.config["POSTGREST_API_URL"]+"users"
    res = requests.post(
        url=url,
        data=json.dumps(json_data),
        headers=headers,
    )
    data = {
        "timestamp": timestamp,
        "contents": json.loads(res.text),
        "check": True,
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run()
```
#### 8.3. Запускаем flask:
       export FLASK_APP=api.py
       flask run -h 0.0.0.0 -p 5001
#### 8.4. Проверяем свой flask api (подставляем свой IP):
       http://35.242.187.228:5001/api/v1.0/users/
       http://35.242.187.228:5001/api/v1.0/users/1540905227894
       http://35.242.187.228:5001/api/v1.0/orders/
       http://35.242.187.228:5001/api/v1.0/orders/1540905227894

### 9. Установка Airflow:
#### 9.1. Ставим Airflow. Если возникают ошибки по зависимым пакетам, так же ставим их.
       pip3 install "apache-airflow[postgres, celery, devel, devel_hadoop, gcp_api, hdfs, hive, password, slack, ssh]"
#### 9.2. Создаём пользователя airflow с паролем в postgres и настраиваем airflow на postgres в файле airflow.cfg:
       sql_alchemy_conn = postgres://airflow:airflow@localhost:5432/airflow
#### 9.3. Делаем инициализацию Airflow:
       airflow initdb
#### 9.4. Создаём в директории $AIRFLOW_HOME директорию dags.
#### 9.5. Команды запуска Airflow:
     Start Web Server:
       nohup airflow webserver $* >> ~/airflow/logs/webserver.logs &
     Start Scheduler:
       nohup airflow scheduler >> ~/airflow/logs/scheduler.logs &
     Stopping Services:
       ps -eaf | grep airflow
       kill -9 {PID}
#### 9.5. Проверяем, что консоль поднялась (меняем на свой IP):
       http://35.242.187.228:8080/admin/
#### 9.6. Ставим на автозагрузку:
