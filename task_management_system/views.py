from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.response import Response

from task_management_system.mixins import CacheResponseMixin
from task_management_system.models import Task
from task_management_system.serializers import TaskSerializer


class TaskViewSet(CacheResponseMixin, viewsets.ModelViewSet):
    cache_timeout = 60 * 10

    queryset = Task.objects.order_by("pk").all()
    serializer_class = TaskSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "priority", "created_at"]

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False)
        instance = self.get_object()
        old_status = instance.status

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        new_status = serializer.instance.status

        if old_status != new_status:
            self.send_status_update_notification(serializer.instance)

        return Response(serializer.data)

    @staticmethod
    def send_status_update_notification(task):
        channel_layer = get_channel_layer()
        message = f"Task #{task.id}: status changed to {task.status}."
        async_to_sync(channel_layer.group_send)(
            'task_status_updates',
            {
                'type': 'task_status_update',
                'message': message,
            }
        )
