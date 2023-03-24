from rest_framework import generics
from django_dubplates.models import Track
from django_dubplates.serializers import TrackSerializer


class TracksAll(generics.ListCreateAPIView):
	"""
	List all tracks, or add (create) a new track.
	"""
	queryset = Track.objects.all()
	serializer_class = TrackSerializer

class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
	"""
	Retrieve, update or delete a track.
	"""
	queryset = Track.objects.all()
	serializer_class = TrackSerializer