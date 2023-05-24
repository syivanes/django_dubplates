from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from django_dubplates.models import Track
from django_dubplates.serializers import TrackSerializer
from django.contrib.auth.models import User
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
		# serializer.save(owner=self.request.user)
		serializer.save()

	# def retrieve(self, request, pk=None):
	# 	track = Track.objects.filter(track_id=pk)
	# 	if track.exists():
	# 		track_ownership_q = UserTrackRelationship.objects.filter(track_id=pk).filter(relationship_type__contains='user_owns_track')
	# 		if track_ownership_q.exists():
	# 			track_serializer = TrackSerializer(track)
	# 			user_track_ownership_instance = track_ownership_q[0]
	# 			# somehow append user_id from user_track_ownership_instance to track_serializer.data so it would define `owner` here?
	# 			return Response(track_serializer.data)



class UserViewSet(viewsets.ModelViewSet):
	"""
	This viewset automatically provides `list` and `retrieve` actions.
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer

	def perform_create(self, serializer):
		serializer.save()

class UserTrackRelViewSet(viewsets.ModelViewSet):
	queryset = UserTrackRelationship.objects.all()
	serializer_class = UserTrackRelSerializer

	def owns_instances_q(self, track_id, specific_user_id=None):
		queryset = UserTrackRelationship.objects.filter(track_id=track_id).filter(relationship_type__contains='user_owns_track')
		if specific_user_id==None:
			exists = queryset.exists()
		else:
			queryset = queryset.filter(user_id=specific_user_id)
			exists = queryset.exists()
			
		return { 'queryset': queryset, 'exists': exists }


	def update_relationship(self, instance, data):
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
				content = {'Conflict: an identical watching relationship already exists'}
				return Response(content, status=status.HTTP_409_CONFLICT)
			elif purchased_already_exists:
				content = {'Conflict: track has already been purchased by user, can\'t add to watchlist'}
				return Response(content, status=status.HTTP_409_CONFLICT)
			else:
				owns_instances_q = self.owns_instances_q(track_id=track_id, specific_user_id=user_id)
				owns_already_exists = owns_instances_q['exists']
				if owns_already_exists:
					content = {'Conflict: user owns this track, can\'t add to watchlist'}
				return Response(content, status=status.HTTP_409_CONFLICT)
		elif relationship_type=='user_purchased_copy':
			if purchased_already_exists:
				content = {'Conflict: user has already purchased a copy of this track'}
				return Response(content, status=status.HTTP_409_CONFLICT)
			elif watching_already_exists:
				print('watching_already_exists')
				return self.update_relationship(instance=watching_instances_q[0], data=serializer.data)
				# return Response(status=status.HTTP_200_OK)
			else:
				owns_instances_q = self.owns_instances_q(track_id=track_id, specific_user_id=user_id)
				owns_already_exists = owns_instances_q['exists']
				if owns_already_exists:
					content = {'Conflict: user is owner of this track, can\'t purchase a copy'}
					return Response(content, status=status.HTTP_409_CONFLICT)
		serializer.save()


@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'users': reverse('user-view-set', request=request, format=format),
		'tracks': reverse('tracks-view-set', request=request, format=format),
		'user-track': reverse('usertrackrel-view-set', request=request, format=format)
	})