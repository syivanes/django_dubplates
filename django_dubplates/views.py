from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.exceptions import APIException

from django_dubplates.models import Track
from django_dubplates.serializers import TrackSerializer
from django.contrib.auth.models import User
# from django_dubplates.models import User
from django_dubplates.serializers import UserSerializer
from django_dubplates.models import UserTrackRelationship
from django_dubplates.serializers import UserTrackRelSerializer
from django_dubplates.permissions import IsOwnerOrReadOnly


class TrackViewSet(viewsets.ModelViewSet):
	"""
	This viewset automatically provides `list`, `create`, `retrieve`,
	`update` and `destroy` actions.
	"""

	queryset = Track.objects.all()
	serializer_class = TrackSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly,
						  IsOwnerOrReadOnly]

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)

class UserViewSet(viewsets.ModelViewSet):
	"""
	This viewset automatically provides `list` and `retrieve` actions.
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer

	def perform_create(self, serializer):
		# print('*************')
		# print(serializer.validated_data.get('password'))
		# print('*************')
		# serializer.set_password(serializer.validated_data.get('password'))
		print('calling perform_create() in views.py')
		serializer.save()

class TrackAlreadyHasOwner(APIException):
	status_code = 404
	default_detail = 'this track already has a user_owns_track relationship instance'
	default_code = 'already_has_owner'

class UserTrackRelViewSet(viewsets.ModelViewSet):
	queryset = UserTrackRelationship.objects.all()
	serializer_class = UserTrackRelSerializer

	def perform_create(self, serializer):
		track_id = serializer.data['track']
		user_id = serializer.data['user']
		relationship_type = serializer.data['relationship_type']
		if relationship_type=='user_owns_track':
			owns_instances = UserTrackRelationship.objects.filter(track_id=track_id).filter(relationship_type__contains='user_owns_track')
			already_exists = len(owns_instances) > 0
			if already_exists:
				raise TrackAlreadyHasOwner
		serializer.save()


@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'users': reverse('user-view-set', request=request, format=format),
		'tracks': reverse('tracks-view-set', request=request, format=format),
		'user-track': reverse('usertrackrel-view-set', request=request, format=format)
	})