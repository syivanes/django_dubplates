from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.response import Response

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
	status_code = 409
	default_detail = 'Conflict: This track already has a user_owns_track relationship instance'
	default_code = 'already_has_owner'

class UserTrackRelViewSet(viewsets.ModelViewSet):
	queryset = UserTrackRelationship.objects.all()
	serializer_class = UserTrackRelSerializer

	# laundry list:
	# user_owns relationship already exists
	# if trying user_purchased and user_watching exists, then convert existing
	# if trying user_purchased or user_watching, and user_owns already exists, then reject

	def owns_instances_q(self, track_id, specific_user_id=None):
		queryset = UserTrackRelationship.objects.filter(track_id=track_id).filter(relationship_type__contains='user_owns_track')
		if specific_user_id==None:
			exists = queryset.exists()
		else:
			queryset = queryset.filter(user_id=specific_user_id)
			exists = queryset.exists()
			
		return { 'queryset': queryset, 'exists': exists }


	def update_relationship(self, instance, data):
		# print('@@@@@@@@@@@@@@@@@@@@')
		# print(serializer.__getattr__)
		# print(kwargs)
		# print('@@@@@@@@@@@@@@@@@@@@')
		serializer = UserTrackRelSerializer(instance, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(status=status.HTTP_200_OK)

	def create(self, serializer, *args, **kwargs):
		track_id = serializer.data['track']
		user_id = serializer.data['user']
		relationship_type = serializer.data['relationship_type']

		watching_instances_q = UserTrackRelationship.objects.filter(track_id=track_id).filter(user_id=user_id).filter(relationship_type__contains='user_watching_track')
		purchased_instances_q = UserTrackRelationship.objects.filter(track_id=track_id).filter(user_id=user_id).filter(relationship_type__contains='user_purchased_copy')

		watching_already_exists = watching_instances_q.exists()
		purchased_already_exists = purchased_instances_q.exists()

		if relationship_type=='user_owns_track':
			owns_instances_q = self.owns_instances_q(track_id=track_id)
			owns_already_exists = owns_instances_q['exists']
			if owns_already_exists:
				raise TrackAlreadyHasOwner
		elif relationship_type=='user_watching_track':
			if watching_already_exists:
				content = {'Conflict', 'an identical watching relationship already exists'}
				return Response(content, status=status.HTTP_409_CONFLICT)
			elif purchased_already_exists:
				content = {'Conflict', 'track has already been purchased by user, can\'t add to watchlist'}
				return Response(content, status=status.HTTP_409_CONFLICT)
			else:
				owns_instances_q = self.owns_instances_q(track_id=track_id, specific_user_id=user_id)
				owns_already_exists = owns_instances_q['exists']
				if owns_already_exists:
					content = {'Conflict', 'user owns this track, can\'t add to watchlist'}
				return Response(content, status=status.HTTP_409_CONFLICT)
		elif relationship_type=='user_purchased_copy':
			if purchased_already_exists:
				content = {'Conflict', 'user has already purchased a copy of this track'}
				return Response(content, status=status.HTTP_409_CONFLICT)
			elif watching_already_exists:
				print('watching_already_exists')
				return self.update_relationship(instance=watching_instances_q[0], data=serializer.data)
				# return Response(status=status.HTTP_200_OK)
			else:
				owns_instances_q = self.owns_instances_q(track_id=track_id, specific_user_id=user_id)
				owns_already_exists = owns_instances_q['exists']
				if owns_already_exists:
					content = {'Conflict', 'user is owner of this track, can\'t purchase a copy'}
					return Response(content, status=status.HTTP_409_CONFLICT)
		serializer.save()


@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'users': reverse('user-view-set', request=request, format=format),
		'tracks': reverse('tracks-view-set', request=request, format=format),
		'user-track': reverse('usertrackrel-view-set', request=request, format=format)
	})