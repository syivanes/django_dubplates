from rest_framework import serializers
from django_dubplates.models import Track


class TrackSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, allow_blank=False, max_length=100)
    url = serializers.CharField(required=True)


    def create(self, validated_data):
        """
        Create and return a new `Track` instance, given the validated data.
        """
        return Track.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Track` instance, given the validated data.
        """
        print(validated_data)
        instance.title = validated_data.get('title', instance.title)
        instance.url = validated_data.get('url', instance.url)
        instance.save()
        return instance