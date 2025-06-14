from rest_framework import serializers
from .models import UserActivityLog


class UserActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivityLog
        fields = "__all__"
        read_only_fields = ("timestamp", "user")

    def create(self, validated_data):
        # Inject request.user automatically
        request = self.context["request"]
        validated_data["user"] = request.user
        return super().create(validated_data)

    def validate_status(self, value):
        # Restrict illegal jumps (e.g., DONE → IN_PROGRESS)
        current = self.instance.status if self.instance else None
        allowed = {
            None: ["PENDING"],
            "PENDING": ["IN_PROGRESS", "DONE"],
            "IN_PROGRESS": ["DONE"],
        }
        if current not in allowed or value not in allowed[current]:
            raise serializers.ValidationError("Invalid status transition")
        return value
