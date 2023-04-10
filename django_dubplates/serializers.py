from rest_framework import serializers
from django_dubplates.models import Track
from django.contrib.auth.models import User


# class TrackSerializer(serializers.Serializer):
#    id = serializers.IntegerField(read_only=True)
#    title = serializers.CharField(required=True, allow_blank=False, max_length=100)
#    download_url = serializers.CharField(required=True)
#    owner = serializers.ReadOnlyField(source='owner.username')


#    def create(self, validated_data):
#       """
#       Create and return a new `Track` instance, given the validated data.
#       """
#       print(validated_data)
#       return Track.objects.create(**validated_data)

#    def update(self, instance, validated_data):
#       """
#       Update and return an existing `Track` instance, given the validated data.
#       """
#       print(validated_data)
#       instance.title = validated_data.get('title', instance.title)
#       instance.url = validated_data.get('url', instance.url)
#       instance.save()
#       return instance

class TrackSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, allow_blank=False, max_length=100)
    download_url = serializers.CharField(required=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Track
        fields = ['url', 'id', 'title', 'owner',
                  'download_url']


# class UserSerializer(serializers.ModelSerializer):
#    tracks = serializers.PrimaryKeyRelatedField(many=True, queryset=Track.objects.all())

#    class Meta:
#       model = User
#       fields = ['id', 'username', 'tracks_author']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    tracks_author = serializers.HyperlinkedRelatedField(many=True, view_name='track-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'password', 'email', 'tracks_author']
