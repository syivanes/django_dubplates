from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions

from django_dubplates.models import Track
from django_dubplates.serializers import TrackSerializer
from django.contrib.auth.models import User
from django_dubplates.serializers import UserSerializer
from django_dubplates.permissions import IsOwnerOrReadOnly


class TracksAll(generics.ListCreateAPIView):
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	queryset = Track.objects.all()
	serializer_class = TrackSerializer
	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)

class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
	queryset = Track.objects.all()
	serializer_class = TrackSerializer

class UserList(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer




@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format=format),
		'tracks': reverse('tracks-all', request=request, format=format)
	})