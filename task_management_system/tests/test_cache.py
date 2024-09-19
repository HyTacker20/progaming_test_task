from django.core.cache import cache
from django.urls import reverse
from rest_framework.test import APITestCase

from task_management_system.models import Task


class CacheResponseMixinTest(APITestCase):
    def setUp(self):
        cache.clear()
        Task.objects.all().delete()
        self.list_url = reverse('task-list')
        self.task = Task.objects.create(
            title="Cached Task",
            description="Testing cache",
        )

    def test_cache_list_response(self):
        response1 = self.client.get(self.list_url)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(len(response1.data['results']), 1)

        Task.objects.create(
            title="Another Task",
            description="Another task description",
        )

        response2 = self.client.get(self.list_url)
        self.assertEqual(len(response2.data['results']), 1)

    def test_cache_invalidation_on_create(self):
        self.client.get(self.list_url, {'page': 1})

        response = self.client.post(self.list_url, {
            'title': 'New Task',
            'description': 'New task description',
        }, format='json')
        self.assertEqual(response.status_code, 201)

        response = self.client.get(self.list_url, {'page': 1})
        print(f"Response Data after creation: {response.data}")
        self.assertEqual(len(response.data['results']), 2)
