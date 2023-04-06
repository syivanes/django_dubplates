from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions
from rest_framework import viewsets

from django_dubplates.models import Track
from django_dubplates.serializers import TrackSerializer
from django.contrib.auth.models import User
from django_dubplates.serializers import UserSerializer
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

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'users': reverse('user-view-set', request=request, format=format),
		'tracks': reverse('tracks-view-set', request=request, format=format)
	})