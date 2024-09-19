from rest_framework import serializers

from task_management_system.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        # if it's a partial update, make fields optional
        if kwargs.get('partial', False):
            for field in self.fields.values():
                field.required = False
        super().__init__(*args, **kwargs)
