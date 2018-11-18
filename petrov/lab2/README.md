# Лабораторная работа №2
Основных задач три:
- собрать кликстрим с сайта
- рассчитывать статистики по расписанию
- отдавать значения метрик через API

Необходимые статистики по каждому товару: количество просмотров страницы с товаром; средняя глубина просмотра страницы с товаром; количество и суммарная стоимость товара, отправленного в корзину нажатием на кнопку "купить" на странице с товаром.

## Сбор данных
С помощью Divolte кликстрим с сайта собирается и сохраняется в kafka. Kafka управляется через Ambari. 

Для расчета необходимых статистик достаточно собирать информацию о переходах пользователя по страницам и о нажатиях на кнопку "купить" на странице с товарами. Глубину просмотра можно вычислять за сессию (сессия заканчивается, если за 30 минут пользователь не совершил ни одного действия).

Divolte по-умолчанию собирает информацию о переходах по страницам 
```
javascript.auto_page_view_event = true
```
Для того, чтобы собирать информацию о нажатиях на кнопку "купить", повесим на элементы с классом `.product-item-detail-buy-button` следующий обработчик события `click`
```javascript
function() {
	divolte.signal(
		"buy_button_click", 
		{
			"price": document.getElementsByClassName('product-item-detail-price-current')[0].innerText,
			"amount": document.getElementsByClassName('product-item-amount-field')[0].value
		}
	);
}
```
Таким образом, будет фиксироваться событие `buy_button_click`, в котором дополнительно определены атрибуты `price` (цена товара) и `amount` (выбранное количество товара).

Divolte складывает в Kafka данные в формате `avro`. Соответствующий маппинг с минимально необходимыми полями
```
mapping {
  map timestamp() onto 'timestamp'
  map eventType() onto 'eventType'
  map location() onto 'location'
  map sessionId() onto 'sessionId'
  map eventParameter('price') onto 'price'
  map eventParameter('amount') onto 'amount'
}
```
и avro-схема
```
{
  "namespace": "io.divolte.examples.record",
  "type": "record",
  "name": "lab2_event",
  "fields": [
    { "name": "timestamp",  "type": "long" },
    { "name": "eventType",  "type": ["null", "string"], "default": null },
    { "name": "location",   "type": ["null", "string"], "default": null },
    { "name": "sessionId",   "type": ["null", "string"], "default": null },
    { "name": "price",   "type": ["null", "string"], "default": null },
    { "name": "amount",   "type": ["null", "string"], "default": null }
  ]
}
```

Далее создаем топик в kafka
```bash
/usr/hdp/3.0.0.0-1634/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic online_store
```

Запускаем Divolte
```bash
divolte-collector-0.9.0/bin/divolte-collector
```
и проверяем, что клики собираются. Для этого можно запустить консольный консьюмер kafka командой
```bash
/usr/hdp/3.0.0.0-1634/kafka/bin/kafka-console-consumer.sh --bootstrap-server PLAINTEXT://instance-1.europe-west1-b.c.terrain-screens-1506419009646.internal:6667 --topic online_store --from-beginning
```

Чтобы не запускать Divolte вручную каждый раз, можно создать системную службу, которая будет автоматически запускаться при перезагрузке сервера или падении процесса.
Для этого нужно создать файл `/etc/systemd/system/divolte.service` со следующим содержимым
```
[Unit]
Description=Divolte
[Install]
WantedBy=multi-user.target
[Service]
ExecStart=/home/obsurder/divolte-collector-0.9.0/bin/divolte-collector
TimeoutSec=600
RuntimeDirectoryMode=755
Restart=always
User=obsurder
Environment="JAVA_HOME=/usr/lib/jvm/java-8-oracle"
```
Подгрузить сервис командой 
```
sudo systemctl daemon-reload
``` 
и активировать его командой 
```
sudo systemctl enable divolte
```
Теперь сервис можно включить командой
```
sudo systemctl start divolte
```

## Конфигурация БД
Статистическую информацию можно хранить в реляционной БД. Рассмотрим пример с использованием PostgreSQL.
Создаем БД `online_shop`
```bash
sudo -u postgres createdb online_shop
```
Затем создаем системного пользователя `online_shop`
```bash
sudo useradd online_shop
sudo passwd online_shop
```
Заходим в БД 
```bash
sudo -u postgres psql
```
и создаем пользователя `online_shop`, которому отдаем все права на БД `online_shop`
```sql
CREATE ROLE online_shop;
ALTER ROLE online_shop WITH PASSWORD 'password';
GRANT ALL ON DATABASE online_shop TO online_shop;
ALTER ROLE online_shop WITH LOGIN;
\q
```
Дальше перезаходим под пользователем `online_shop`
```bash
sudo -u online_shop psql
```
и создаем таблицы для хранения метрик
```sql
CREATE TABLE users (
	"ts" int NOT NULL,
    "url" text NOT NULL,
	"item_id" text NOT NULL,
	"count" int NOT NULL,
	"deep" float8 NOT NULL,
    PRIMARY KEY ("ts","item_id")
);

CREATE TABLE orders (
	"ts" int NOT NULL,
    "url" text NOT NULL,
	"item_id" text NOT NULL,
	"count" int NOT NULL,
	"sum" float8 NOT NULL,
    PRIMARY KEY ("ts","item_id")
);
```
Здесь `url` -- адрес магазина вида `b24-*.bitrix24.shop`; `item_id` -- идентификатор товара, например, `dress-nightlife`; `count`, `deep` и `sum` -- статистики; `ts` -- время снятия метрик, это поле необходимо для агрегации данных по временным периодам.

Запись в `pg_hba.conf` добавлять не нужно, так как локальные подключения там разрешены по умолчанию с использованием `md5`.

## Скрипт для расчета статистик
Скрипт должен делать следующее: при каждом новом запуске, он забирает из топика данные, которые он еще не видел, подсчитывает по этим данным статистики и складывает их в БД.

Сначала устанавливаем `pip`, с помощью которого устанавливаем пакет `virtualenv`
```bash
sudo apt install python3-pip
sudo pip3 install virtualenv
```
Затем создаем папку `lab2_calc_metrics`, где будет размещено приложение для расчета статистик и создаем в ней виртуальное окружение `lab2_metrics`
```bash
mkdir lab2_calc_metrics
cd lab2_calc_metrics
virtualenv lab2_metrics
```
Для работы скрипта необходимо установить пакеты, названия которых запишем в файл `requirements.txt`
```
kafka-python
avro-python3
psycopg2
lz4
```
и установим их командой
```bash
lab2_metrics/bin/pip install -r requirements.txt
```
Создадим скрипт `calc_metrics.py`. Основная часть скрипта выглядит следующим образом
```python
messages = get_messages()
items = calc_metrics(messages)
ts = math.floor(time.time())
users_records = [
	[ts,'b24-khpv25.bitrix24.shop',x,items[x]['page_views_count'],items[x]['deep']]
	for x in items
]
orders_records = [
	[ts,'b24-khpv25.bitrix24.shop',x,items[x]['orders_count'],items[x]['orders_sum']] 
	for x in items if items[x]['orders_count'] != 0
]
con,cur = dbc()
psycopg2.extras.execute_values(cur, "INSERT INTO users VALUES %s", users_records, page_size=100)
psycopg2.extras.execute_values(cur, "INSERT INTO orders VALUES %s", orders_records, page_size=100)
con.commit()
con.close()
```
Функция `get_messages` забирает новые сообщения из топика.
```python
def get_messages():
    # делаем ридер для авро-схема
    schema = avro.schema.Parse(open(SCHEMA_PATH,'r').read())
    reader = DatumReader(schema)
    
    # создаем консьюмера
    consumer = KafkaConsumer(
        TOPIC_NAME,
        group_id=GROUP_ID,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        api_version=(0, 10),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        consumer_timeout_ms=15000
    )
    
    # читаем последние сообщения
    messages = []
    for message in consumer:
        messages.append(avro_deserializer(message.value,reader))
    consumer.close()
    
    # сортируем по времени
    messages = sorted(messages, key=lambda k: k['timestamp'])
    
    return messages
```
В ней используется функция `avro_deserializer` которая с помощью созданного `reader` читает сообщения в формате `avro` в питоновские структуры данных
```python
def avro_deserializer(data,reader):
    bytes_reader = io.BytesIO(data)
    decoder = BinaryDecoder(bytes_reader)
    result = reader.read(decoder)
    return result
```
После того, как новые сообщения прочитаны, функция `calc_metrics` рассчитывает статистики на новых сообщениях
```python
def calc_metrics(messages):
    items = {}
    sessions = {}
    for message in messages:
        location = message['location']
        session_id = message['sessionId']
        event_type = message['eventType']
        sessions.setdefault(session_id,{'page_views_count':0})
        if event_type == 'pageView':
            sessions[session_id]['page_views_count'] += 1
        if is_item(location):
            item_id = get_item_id(location)
            items.setdefault(item_id,{'page_views_count':0,'deep':0.0,'orders_count':0,'orders_sum':0.0})
            if event_type == 'pageView':
                items[item_id]['page_views_count'] += 1
                t = items[item_id]['page_views_count']
                items[item_id]['deep'] = (t - 1) / t * items[item_id]['deep'] + 1 / t * sessions[session_id]['page_views_count']
            if event_type == 'buy_button_click':
                items[item_id]['orders_count'] += int(message['amount'])
                items[item_id]['orders_sum'] += float(re.sub("\D","",message['price'])) * int(message['amount'])
    return items
```
Эта функция проходится по каждому сообщению. Во время прохода подсчитывается глубина просмотра сайта для каждой сессии (по количеству событий типа `pageView` в рамках сессии `sessionId`). Также эта функция определяет, является ли страница, на которую зашел пользователь, страницей с информацией о товаре (по `location`). За счет этого подсчитывается количество просмотров страниц каждого товара и глубина просмотра этих страниц (как среднее от всех глубин). Кроме этого проверяются события типа `buy_button_click`, из которых вытаскиваются значения полей `price` и `amount` и по которым подсчитываются количество заказов (равно `amount`) и общая стоимость заказов (`price` x `amount`) каждого товара.

Стоит отметить, что в таком подходе все сессии в новом наборе сообщений считаются новыми (то есть для всех них счетчик просмотров страниц по-умолчанию выставляется 0). Понятно, что это не совсем верно, так как некоторые сессии могли продолжаться еще с предыдущего расчета статистик. Чтобы избежать этой проблемы, можно дополнительно записывать в БД последнее значение глубины просмотра сайта для каждой сессии и при следующем расчете метрик инициализировать не нулем, и именно этим значением.

Дальше формируются записи для вставку в таблицы БД и вставляются.

В функции `dbc` происходит получение объектов подключения к БД и курсора согласно Python DB API 2.0. В случае использования библиотека `psycopg2` для работы с БД PostgreSQL эта функция имеет следующий вид
```python
def dbc():
    db_name = 'online_shop'
    db_user = 'online_shop'
    db_pass = 'password'
    db_host = 'localhost'
    db_port = '5432'
    con = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host, port=db_port)
    cur = con.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    return con,cur
```
С параметром инициализации курсора `cursor_factory = psycopg2.extras.RealDictCursor` данные из БД будут в виде списка словарей, при этом ключи словарей - это названия столбцов в таблице.

## Настройка API
Создаем директорию, в которой будет размещено приложение на Flask
```bash
mkdir lab2_api
cd lab2_api
```
Прикидываем, какие понадобятся пакеты и создаем файл `requirements.txt` с содержимым
```
flask
psycopg2
```
Создаем виртуальное окружение и ставим необходимые пакеты
```bash
virtualenv lab2_env
lab2_env/bin/pip install -r requirements.txt
```
Создаем приложение веб-сервер `lab2_api.py`.
Определим четыре метода нашего API
```python
@app.route('/api/v1.0/users', methods=['GET'])
def api_get_users():
    timestamp = math.floor(time.time()) - 60*60
    users = get_info('users',timestamp)
    return jsonify(users)

@app.route('/api/v1.0/users/<int:timestamp>', methods=['GET'])
def api_get_users_by_timestamp(timestamp):
    users = get_info('users',timestamp)
    return jsonify(users)

@app.route('/api/v1.0/orders', methods=['GET'])
def api_get_orders():
    timestamp = math.floor(time.time()) - 60*60
    orders = get_info('orders',timestamp)
    return jsonify(orders)

@app.route('/api/v1.0/orders/<int:timestamp>', methods=['GET'])
def api_get_orders_by_timestamp(timestamp):
    orders = get_info('orders',timestamp)
    return jsonify(orders)
```
Методы `/api/v1.0/users` и `/api/v1.0/orders` возращают информацию из таблиц `users` и `orders` за последний час.
Методы `/api/v1.0/users/<int:timestamp>` и `/api/v1.0/orders/<int:timestamp>` возвращают информацию из таблиц `users` и `orders` за промежуток времени, прошедший от переданного `timestamp` до текущего момента.

Функция `get_info` забирает информацию из БД
```python
def get_info(query_type,timestamp):
    timestamp = int(timestamp)

    con,cur = dbc()
    cur.execute(SQL_QUERIES[query_type].format(timestamp))
    
    result = {
        'timestamp': timestamp,
        'contents': [],
        'check': True
    }
    records = cur.fetchall()
    for record in records:
        result['contents'].append(record)
    con.close()
        
    return result
```

Шаблоны SQL-запросов хранятся в словаре `SQL_QUERIES`
```python
SQL_QUERIES = {
    'users': """SELECT url,item_id AS "id_item",SUM(count) AS count, AVG(deep) AS deep FROM users WHERE ts >= {} GROUP BY item_id,url;""",
    'orders': """SELECT url,item_id AS "id_item",SUM(count) AS count, SUM(sum) AS sum FROM orders WHERE ts >= {} GROUP BY item_id,url;"""
}
```

Запуск приложения осуществляется кодом
```python
app = Flask(__name__)

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port=5001)
```

Необходимые импорты
```python
from flask import Flask
from flask.json import jsonify
import psycopg2
import psycopg2.extras
import math
import time
```

Запустить скрипт для проверки можно командой
```bash
lab2_env/bin/python lab2_api.py
```
После запуска этого скрипта, на порту `5001` будет доступно API. Проверить работоспособность можно командой
```bash
curl localhost:5001/api/v1.0/users
```

Чтобы не обращаться к этому порту напрямую, в конфигурации nginx можно добавить
```
location /api/v1.0/ {
    proxy_pass http://localhost:5001/api/v1.0/;
}
```

Настроим системный сервис, который будет перезапускать веб-сервер при старте системы и в других случаях. Создаем файл `/etc/systemd/system/lab2_api.service` с содержимым
```
[Unit]
Description=Lab 2 API flask web server
[Install]
WantedBy=multi-user.target
[Service]
ExecStart=/home/obsurder/lab2_api/lab2_env/bin/python /home/obsurder/lab2_api/lab2_api.py
TimeoutSec=600
RuntimeDirectoryMode=755
Restart=always
User=obsurder
```
Затем выполняем команды
```bash
sudo systemctl daemon-reload
sudo systemctl enable lab2_api
sudo systemctl start lab2_api
```

## Настройка расписания
Для запуска скрипта каждые пол часа по крону в файл `/etc/crontab` следует добавить строку
```
*/30 *    * * *   obsurder /home/obsurder/lab2_calc_metrics/lab2_metrics/bin/python /home/obsurder/lab2_calc_metrics/calc_metrics.py >> /home/obsurder/lab2_calc_metrics/output.txt 2>&1
```
В файл `output.txt` будет записывать все, что печатается во время выполнения программы.
Перезапускать ничего не надо, crontab сам подтянет все изменения. 
В конце файла `/etc/crontab` обязательно должна быть пустая строка.

## Полезные ссылки
[Автозапуск сервиса через systemd](https://linuxoid.pro/autostart-using-systemd/)
[Проектирование RESTful API с помощью Python и Flask](https://habr.com/post/246699/)

## Описание файлов
- [calc_metrics.py](calc_metrics.py) -- скрипт для расчета статистик на данных из kafka
- [default](default) -- конфиг nginx
- [divolte-collector.conf](divolte-collector.conf) -- конфиг divolte
- [divolte.html](divolte.html) -- кусок html, который необходимо вставить на страницу для сбора кликстрим
- [lab2.avsc](lab2.avsc) -- avro-схема для событий divolte
- [lab2_api.py](lab2_api.py) -- веб-приложение на flask, реализующее API для запросов метрик
- [lab2_mapping.groovy](lab2_mapping.groovy) -- маппинг в поля avro-схемы

