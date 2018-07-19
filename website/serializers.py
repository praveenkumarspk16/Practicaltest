from rest_framework import serializers
from website.models import Rest_framework


class RestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rest_framework
        fields = ('id', 'username', 'email')

