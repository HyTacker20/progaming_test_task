from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from task_management_system.models import Task, TaskStatus, TaskPriority
from task_management_system.serializers import TaskSerializer


class TaskAPITest(APITestCase):
    def setUp(self):
        self.list_url = reverse('task-list')
        self.task = Task.objects.create(
            title="Initial Task",
            description="Initial task description",
            status=TaskStatus.NEW,
            priority=TaskPriority.LOW
        )
        self.detail_url = reverse('task-detail', args=[self.task.id])

    def test_get_task_list(self):
        response = self.client.get(self.list_url)
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_create_task(self):
        data = {
            'title': 'New Task',
            'description': 'New task description',
            'status': TaskStatus.IN_PROGRESS,
            'priority': TaskPriority.HIGH
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.last().title, 'New Task')

    def test_get_task_detail(self):
        response = self.client.get(self.detail_url)
        task = Task.objects.get(id=self.task.id)
        serializer = TaskSerializer(task)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_task(self):
        data = {
            'title': 'Updated Task',
            'description': 'Updated description',
            'status': TaskStatus.COMPLETED,
            'priority': TaskPriority.MEDIUM
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.status, TaskStatus.COMPLETED)

    def test_partial_update_task(self):
        data = {'status': TaskStatus.COMPLETED.value}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, TaskStatus.COMPLETED.value)

    def test_delete_task(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
