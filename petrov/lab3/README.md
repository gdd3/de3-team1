# Лабораторная работа №3
Основные задачи:
- расчет метрик
- сбор метрик
- визуализация метрик
- настройка API
Необходимые метрики: число посетителей в пятиминутный интервал, число заказов в пятиминутный интервал, конверсия за час, средний чек за сутки с обновлением раз в час, сумма всех заказов за сутки с обновлением раз в полчаса.

## Расчет метрик
Для расчета всех метрик достаточно отслеживать два типа событий:
- переходы по страницам
- нажатие на кнопку "Оформить заказ" с текущей суммой покупок в корзине

Все действия по сбору данных аналогичны второй лабораторной.

Расчитывать метрики пожно налету, по мере появления новых сообщений из Kafka. При этом надо учитывать, что минимальный интервал обновления метрик: 5 минут. Соответственно, если за пять минут не появится ни одного сообщения, то метрики число посетителей и число заказов не сбросятся на ноль. Решить этот вопрос можно как минимум двумя путями:
- по таймеру засылать служебное сообщение в топик хотя бы раз в пять минут 
- параллельно запустить скрипт, который будет по таймеру поправлять метрики (скидывать на нулевые значения, если за последние пять минут не было сообщений)

Пример расчета метрик и публикация их значений в формате Prometheus Text на веб-страничке (используется пакет `prometheus_client`):
```python
for message in consumer:
    data = avro_deserializer(message.value,reader)
    current_time = data['timestamp']
    current_user = data['sessionId']
    current_event = data['eventType']

    if not is_same_interval(current_time,last_message_time,8.64e7):
        average_order_value = (0, 0)
        gauges['tov'].set(0.0)
        gauges['aov'].set(0.0)
    if not is_same_interval(current_time,last_message_time,3.6e6):
        conversion_users = set()
        conversion_users_orders = set()
        gauges['conversion'].set(0.0)
    if not is_same_interval(current_time,last_message_time,3e5):
        users = set()
        gauges['orders_count'].set(0)

    last_message_time = current_time
    gauges['last_message_time'].set(current_time)
    users.add(current_user)
    gauges['users_count'].set(len(users))
    conversion_users.add(current_user)
    if current_event == 'checkout_click':
        current_price = price_convert(data['total_price'])
        gauges['orders_count'].inc()
        conversion_users_orders.add(current_user)
        gauges['conversion'].set(round(len(conversion_users_orders) / len(conversion_users) * 100, 2))
        gauges['tov'].inc(current_price)
        average_order_value = recalc_avg(average_order_value, current_price)
        gauges['aov'].set(round(average_order_value[0], 2))
```

## Сбор метрик
После того, как убедились, что метрики собираются и публикуются, скачиваем Prometheus
```bash
wget https://github.com/prometheus/prometheus/releases/download/v2.5.0/prometheus-2.5.0.linux-amd64.tar.gz
tar xvfz prometheus-2.5.0.linux-amd64.tar.gz
```
Настраиваем конфиг `prometheus-2.5.0.linux-amd64/prometheus.yml`
```
global:
  scrape_interval: 5m
  external_labels:
    monitor: 'online_store'

scrape_configs:
  - job_name: 'test_job'

    scrape_interval: 5m

    static_configs:
      - targets: ['localhost:8013']
```
Запускаем командой
```bash
prometheus-2.5.0.linux-amd64/prometheus --config.file=prometheus-2.5.0.linux-amd64/prometheus.yml
```

## Визуализация метрик
Теперь можно подключиться к Prometheus через его API и забрать оттуда метрики для визуализации. С помощью Grafana это можно сделать автоматически, подключив Prometheus в качестве источника данных.

Ставим Grafana
```bash
wget https://s3-us-west-2.amazonaws.com/grafana-releases/release/grafana_5.3.4_amd64.deb 
sudo dpkg -i grafana_5.3.4_amd64.deb
sudo systemctl daemon-reload
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
```
В настройках можно поменять порта на `3001`, чтобы не было конфликтов с другими службами. Переходим по адресу `localhost:3001`.
Далее в веб-интерфейсе настраиваем источник данных и дэшборд.

## Настройка API
Аналогично второй лабораторной работе, только вместо подключения к БД, конверсия забирается напрямую с веб-страницы с текущими метриками. 
```python
def get_conversion():
    r = requests.get('http://localhost:'+str(METRICS_PORT))
    page = r.content.decode('utf8')
    metrics = {}
    for family in text_string_to_metric_families(page):
        for sample in family.samples:
            if sample[0] == 'conversion':
                metrics[sample[0]] = sample[2]
    return metrics['conversion']/100
```

