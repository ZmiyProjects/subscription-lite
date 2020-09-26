import json
from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Editor, Journal, Customer


class EditorTestCase(APITestCase):
    fixtures = [
        'fixtures/database/editors.json',
        'fixtures/database/journals.json'
    ]

    def test_create_editor(self):
        data = {
            'editor_name': "Питер"
        }
        response = self.client.post('/api/editors/', json.dumps(data),
                                    content_type='application/json;charset=UTF-8')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        self.assertDictEqual(json.loads(response.content), {"id": 3}, response.content)
        self.assertEqual(Editor.objects.count(), 3, response.content)

    def test_get_editor(self):
        result = {
            "id": 1,
            "editor_name": "Тайная пресса",
            "journals_count": 2
        }

        response = self.client.get('/api/editors/1/', content_type='application/json;charset=UTF-8')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertDictEqual(json.loads(response.content), result, response.content)

    def test_get_all_editors(self):
        result = [
            {
                "id": 1,
                "editor_name": "Тайная пресса",
                "journals_count": 2
            },
            {
                "id": 2,
                "editor_name": "Альфа",
                "journals_count": 1
            }
        ]

        response = self.client.get('/api/editors/', content_type='application/json;charset=UTF-8')
        self.assertListEqual(json.loads(response.content), result, response.content)


class JournalTestCase(APITestCase):
    fixtures = [
        'fixtures/database/editors.json',
        'fixtures/database/journals.json'
    ]

    def test_create_journal(self):
        data = {
            'journal_name': "Новый",
            'price': 200
        }

        response = self.client.post('/api/editors/1/journals/', json.dumps(data),
                                    content_type='application/json;charset=UTF-8')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        self.assertDictEqual(json.loads(response.content), {"id": 4}, response.content)

        response = self.client.get('/api/editors/1/', content_type='application/json;charset=UTF-8')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

        # После добавления нового журнала, количество журналов у издателя должно увеличиться на 1
        self.assertEqual(json.loads(response.content)["journals_count"], 3, response.content)

    def test_incorrect_price(self):
        data = {
            'journal_name': "Отрицательно оцененный",
            'price': -1
        }

        response = self.client.post('/api/editors/1/journals/', json.dumps(data),
                                    content_type='application/json;charset=UTF-8')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)

    def test_get_journal(self):
        result = {
            "id": 2,
            "editor": {
                "id": 1,
                "editor_name": "Тайная пресса"
            },
            "journal_name": "Наука",
            "price": 400
        }
        response = self.client.get('/api/journals/2/', content_type='application/json;charset=UTF-8')

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertDictEqual(json.loads(response.content), result, response.content)


class CustomerTestCase(APITestCase):
    fixtures = [
        'fixtures/database/customers.json'
    ]

    def test_create_customer(self):
        data = {
            "first_name": "Иванов",
            "second_name": "Алексей",
            "address": "г. Москва, Пролетарская улица",
            "birth_date": "2000-09-10"
        }

        response = self.client.post('/api/customers/', json.dumps(data), content_type='application/json;charset=UTF-8')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        self.assertDictEqual(json.loads(response.content), {"id": 3}, response.content)

    def test_incorrect_age(self):
        """попытка регистрации пользователя младше 18 лет"""
        data = {
            "first_name": "Иванов",
            "second_name": "Алексей",
            "address": "г. Москва, Пролетарская улица",
            "birth_date": "2010-09-10"
        }

        response = self.client.post('/api/customers/', json.dumps(data), content_type='application/json;charset=UTF-8')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)

    def test_update_customer(self):
        data = {
            "address": "г. Москва, Ленинский проспект, дом 2к10"
        }

        result = {
            "id": 2,
            "first_name": "Петр",
            "second_name": "Петров",
            "address": "г. Москва, Ленинский проспект, дом 2к10",
            "birth_date": "1974-03-20",
            "registration_date": "2020-05-29"
        }

        response = self.client.patch('/api/customers/2/', json.dumps(data),
                                     content_type='application/json;charset=UTF-8')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertDictEqual(json.loads(response.content), result)

    def test_get_customer(self):
        result = {
            "id": 1,
            "first_name": "Иванов",
            "second_name": "Иван",
            "address": "г. Москва, Ленинский проспект",
            "birth_date": "1990-10-25",
            "registration_date": "2020-01-01",
            "subscription_count": 2
        }

        response = self.client.get('/api/customers/1/', content_type='application/json;charset=UTF-8')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertDictEqual(json.loads(response.content), result, response.content)


class SubscriptionTestCase(APITestCase):
    fixtures = [
        'fixtures/database/editors.json',
        'fixtures/database/subscriptions.json',
        'fixtures/database/customers.json',
        'fixtures/database/journals.json'
    ]

    def test_create_subscription(self):
        data = {
            "journal": 2
        }

        result = {
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
            "journal_id": 2,
            "customer_id": 2
        }

        response = self.client.post('/api/customers/2/subscriptions/', json.dumps(data),
                                    content_type='application/json;charset=UTF-8')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        self.assertDictEqual(json.loads(response.content), result, response.content)

        response = self.client.get('/api/customers/2/', content_type='application/json;charset=UTF-8')
        self.assertEqual(json.loads(response.content)["subscription_count"], 3, response.content)

    def test_delete_subscription(self):
        # TODO /api/customers/2/subscriptions/subscription_id/
        data = {
            "journal": 2
        }

        after_delete = {
            "id": 1,
            "subscriptions": [
                {
                    "start_date": "2020-09-01",
                    "end_date": "2021-09-01",
                    "journal": {
                        "id": 1,
                        "editor": {
                            "id": 1,
                            "editor_name": "Тайная пресса"
                        },
                        "journal_name": "Рыбалка",
                        "price": 100
                    }
                }
            ]
        }

        response = self.client.delete('/api/customers/1/subscriptions/', json.dumps(data),
                                      content_type='application/json;charset=UTF-8')

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

        response = self.client.get('/api/customers/1/subscriptions/', content_type='application/json;charset=UTF-8')
        self.assertDictEqual(json.loads(response.content), after_delete, response.content)

    def test_get_customer_subscriptions(self):
        result = {
            "id": 1,
            "subscriptions": [
                {
                    "start_date": "2020-09-01",
                    "end_date": "2021-09-01",
                    "journal": {
                        "id": 1,
                        "editor": {
                            "id": 1,
                            "editor_name": "Тайная пресса"
                        },
                        "journal_name": "Рыбалка",
                        "price": 100
                    }
                },
                {
                    "start_date": "2020-09-01",
                    "end_date": "2021-09-01",
                    "journal": {
                        "id": 2,
                        "editor": {
                            "id": 1,
                            "editor_name": "Тайная пресса"
                        },
                        "journal_name": "Наука",
                        "price": 400
                    }
                }
            ]
        }

        response = self.client.get('/api/customers/1/subscriptions/', content_type='application/json;charset=UTF-8')

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertDictEqual(json.loads(response.content), result, response.content)
