from rest_framework.routers import DefaultRouter

from task_management_system.views import TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = router.urls
