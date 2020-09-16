# Веб-сервис предоставляющий API для учета подписки на периодические печатные издания

# Основные сущности

## Editor
Издательство:

- id - уникальный идентификатор издательства
- editor_name - уникальное название издательства

## Journal
Журнал
- id - уникальный идентификатор журнала
- journal_name - уникальное название журнала
- price - стоимость подписки на 1 год
- editor - ссылка на издательство

## Customer
Подписчик

- id - уникальный идентификатор подписчика
- first_name - фамилия подписчика
- last_name - имя подписчика
- address - адрес доставки изданий
- birth_date - дата рождения (18+)
- registration_date - дата регистрации
- subscriptions_count - количество активных подписок

## Subscription
Подписка

- journal - ссылка на идентификатор журнала
- customer - ссылка на идентификатор пользователя, оформившего подписку
- start_date - дата оформления подписки
- end_date - дата окончания подписки

# Основные методы API

- POST /api/editors - добавить новое издательство

```bash
curl --header "Content-Type: application/json" --request POST --data '{"editor_name": "Дачная пресса"}' http://127.0.0.1:8080/api/editors/
```
Ответ - id нового издательства

- GET /api/editors - получить список издательств

```bash
curl --header "Content-Type: application/json" --request GET http://127.0.0.1:8080/api/editors/
```

- GET /api/editors/$id - получить конкретное издательство и список доступные подписок (журналов)

```bash
curl --header "Content-Type: application/json" --request GET http://127.0.0.1:8080/api/editors/1/
```

- POST /api/editors/$id/journals - добавить новый журнал конкретному издательству

```bash
curl --header "Content-Type: application/json" --request POST --data '{"journal_name": "Рыбалка", "price": 100}' http://127.0.0.1:8080/api/editors/1/journals/
```
Ответ - id нового журнала

- GET /api/journals/$id - получить конкретный журнал

```bash
curl --header "Content-Type: application/json" --request GET http://127.0.0.1:8080/api/journals/1/
```

- POST /api/customers - добавить нового пользователя

```bash
curl --header "Content-Type: application/json" --request POST --data '{"first_name": "Иванов", "second_name": "Иван", "address": "г. Москва, Ленинский проспект", "birth_date": "1990-10-25"}' http://127.0.0.1:8080/api/customers/
```
Ответ - id нового пользователя

- PATCH /api/customers/$id/ - обновить сведения о пользователе

```bash
curl --header "Content-Type: application/json" --request PATCH --data '{"address": "г. Москва, Ленинский проспект, дом 2к10"}' http://127.0.0.1:8080/api/customers/1/
```
Ответ - структура с новым состоянием пользователя

- POST /api/customers/$id/subscriptions - добавить пользователю новую подписку

```bash
curl --header "Content-Type: application/json" --request POST --data '{"journal": 4}' http://127.0.0.1:8080/api/customers/1/subscriptions/
```

- GET /api/customers/$id - получить конкретного пользователя и его подписки

```bash
curl --header "Content-Type: application/json" --request GET http://127.0.0.1:8080/api/customers/1/
```