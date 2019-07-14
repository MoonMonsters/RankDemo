from rest_framework import serializers
from rank.models import Username


class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Username
        fields = ['name']
