from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django_dubplates.models import Track
from django_dubplates.serializers import TrackSerializer

@csrf_exempt
def track_list(request):
    """
    List all tracks, or add (create) a new track.
    """
    if request.method == 'GET':
        tracks = Track.objects.all()
        serializer = TrackSerializer(tracks, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TrackSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def track_detail(request, pk):
    """
    Retrieve, update or delete a track.
    """
    try:
        track = Track.objects.get(pk=pk)
    except Track.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TrackSerializer(track)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TrackSerializer(track, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        track.delete()
        return HttpResponse(status=204)