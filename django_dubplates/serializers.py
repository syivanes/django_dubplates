from rest_framework import serializers
from django_dubplates.models import Track
from django.contrib.auth.models import User


class TrackSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, allow_blank=False, max_length=100)
    download_url = serializers.CharField(required=True)
    owner = serializers.ReadOnlyField(source='owner.username')


    def create(self, validated_data):
        """
        Create and return a new `Track` instance, given the validated data.
        """
        print(validated_data)
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

    # def save(self, *args, **kwargs):
    #     lexer = get_lexer_by_name(self.language)
    #     linenos = 'table' if self.linenos else False
    #     options = {'title': self.title} if self.title else {}
    #     formatter = HtmlFormatter(style=self.style, linenos=linenos,
    #                               full=True, **options)
    #     self.highlighted = highlight(self.code, lexer, formatter)
    #     super().save(*args, **kwargs)


class UserSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, queryset=Track.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'tracks_author']