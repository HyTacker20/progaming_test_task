from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer
from channels.routing import URLRouter, ProtocolTypeRouter
from channels.testing import WebsocketCommunicator
from django.contrib.auth.models import User
from django.test import TransactionTestCase
from rest_framework_simplejwt.tokens import AccessToken

from task_management_system.models import Task, TaskStatus
from task_management_system.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "websocket": URLRouter(websocket_urlpatterns),
})


class TaskStatusConsumerTest(TransactionTestCase):
    async def test_websocket_receive_notification(self):
        user = await sync_to_async(User.objects.create_user)(
            username='testuser', password='testpass'
        )
        access_token = str(AccessToken.for_user(user))

        communicator = WebsocketCommunicator(
            application,
            "/ws/tasks/status/",
            headers=[
                (b'authorization', f'Bearer {access_token}'.encode())
            ]
        )

        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        task = await sync_to_async(Task.objects.create)(
            title="WebSocket Task",
            description="Testing WebSocket notification",
            status=TaskStatus.NEW
        )

        channel_layer = get_channel_layer()

        message = f"Task #{task.id}: status changed to {TaskStatus.COMPLETED}."
        await channel_layer.group_send('task_status_updates', {
            'type': 'task_status_update',
            'message': message
        })

        response = await communicator.receive_json_from()
        self.assertEqual(response['message'], message)

        await communicator.disconnect()
