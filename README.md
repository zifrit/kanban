### Мой Канбан
REST API лдя создание доски, колонок и размещение задач в колонках.

Для запуска проекта нужно сделать следующее:
1. Клонируйте проект себе на компьютер:
```bash
git clone https://github.com/zifrit/kanban.git
```
2. Создайте файл .env в корне проекта с переменными окружения по примеру .env_example.
В переменную CRYPTO_SECRET_KEY поместите ключ, сгенерированный командой:
```bash
openssl rand -hex 32
```

3. Запуск проекта в докере 
```bash
docker compose -f docker-compose.yaml up --build -d
```
в докере поднимается сам проект, база данных PostgreSQL 16 и Nginx.
Проект доступен по адресу 0.0.0.0

#### Документация будет доступна по адресу http://app_host/api/openapi

### Для запуска тестов

1. Клонируйте проект себе на компьютер:
```bash
git clone https://github.com/zifrit/kanban.git
```
2. Создайте файл .env в корне проекта с переменными окружения по примеру .env_example.
В переменную CRYPTO_SECRET_KEY поместите ключ, сгенерированный командой:
```bash
openssl rand -hex 32
```

3. Запуск проекта в докере 
```bash
docker compose -f docker-compose-test.yml up --build -d
```