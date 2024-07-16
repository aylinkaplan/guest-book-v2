from rest_framework import serializers
from .models import User, Entry


class UserSerializer(serializers.ModelSerializer):
    total_messages = serializers.IntegerField()
    last_entry = serializers.CharField()

    class Meta:
        model = User
        fields = ['name', 'total_messages', 'last_entry']


class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name']


class EntrySerializer(serializers.ModelSerializer):
    user = UserNestedSerializer()

    class Meta:
        model = Entry
        fields = ['user', 'subject', 'message']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_name = user_data['name']
        user, created = User.objects.get_or_create(name=user_name)
        validated_data['user'] = user
        entry = Entry.objects.create(**validated_data)
        return entry
