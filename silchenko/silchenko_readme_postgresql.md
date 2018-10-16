# de3-team1-silchenko PostgreSQL
### 1. Установка PostgreSQL:
#### 1.1. Импортируем PostgreSQL public GPG key:
       wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
     1.2. Выполняем команду и запоминаем результат:
       lsb_release -cs
     1.3. Создаём файл /etc/apt/sources.list.d/pgdg.list:
       sudo vi /etc/apt/sources.list.d/pgdg.list
     1.4. Помещаем туда строчку, подставив результат команды из шага 1.2.:
       deb http://apt.postgresql.org/pub/repos/apt/  **результат команды **-pgdg main
      Пример:
       deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main
     1.5. Обновляем репозиторий:
       sudo apt-get update
#### 1.6. Устанавливаем PostgreSQL:
       sudo apt-get install postgresql-10 pgadmin4
