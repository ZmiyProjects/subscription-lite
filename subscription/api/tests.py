import json

from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Editor

ADDRESS_FOR_TEST = '/api/editors/'


class EditorTestCase(APITestCase):
    fixtures = [
        'fixtures/database/editors.json'
    ]

    def test_create_editor(self):
        data = {
            'editor_name': "Питер"
        }
        response = self.client.post(ADDRESS_FOR_TEST, json.dumps(data),
                                    content_type='application/json;charset=UTF-8')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        self.assertDictEqual(json.loads(response.content), {"id": 3}, response.content)
        self.assertEqual(Editor.objects.count(), 3, response.content)
