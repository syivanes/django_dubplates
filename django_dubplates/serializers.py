from rest_framework import serializers
from django_dubplates.models import Track
from django_dubplates.models import Watchlist
from django.contrib.auth.models import User


# class TrackSerializer(serializers.Serializer):
#   id = serializers.IntegerField(read_only=True)
#   title = serializers.CharField(required=True, allow_blank=False, max_length=100)
#   download_url = serializers.CharField(required=True)
#   owner = serializers.ReadOnlyField(source='owner.username')


#   def create(self, validated_data):
#      """
#      Create and return a new `Track` instance, given the validated data.
#      """
#      print(validated_data)
#      return Track.objects.create(**validated_data)

#   def update(self, instance, validated_data):
#      """
#      Update and return an existing `Track` instance, given the validated data.
#      """
#      print(validated_data)
#      instance.title = validated_data.get('title', instance.title)
#      instance.url = validated_data.get('url', instance.url)
#      instance.save()
#      return instance

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
#   tracks = serializers.PrimaryKeyRelatedField(many=True, queryset=Track.objects.all())

#   class Meta:
#      model = User
#      fields = ['id', 'username', 'tracks_author']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    track_author = serializers.HyperlinkedRelatedField(many=True, view_name='track-detail', read_only=True)
    watchlist_user = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'password', 'email', 'track_author', 'watchlist_user']
    def create(self, validated_data):
        print('calling create() in serializers.py')
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class WatchlistSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Watchlist
        fields = '__all__'
