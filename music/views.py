from django.db.transaction import atomic
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from .models import Songs, Artist, Albom
from .serializers import SongsSerializer, ArtistSerializer, AlbomSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters

class ArtistAPIView(APIView):
    def get(self, request):
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)

class AlbomAPIViewSet(ModelViewSet):
    queryset = Albom.objects.all()
    serializer_class = AlbomSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

class SongSetAPIView(ModelViewSet):
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer
    # authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated, ]
    filter_backends = (filters.SearchFilter, )
    search_fields = ['title', ]
    pagination_class = LimitOffsetPagination

    @action(detail=True, methods=["POST"])
    def listen(self, request, *args, **kwargs):
        song = self.get_object()
        with atomic():
            song.listened += 1
            song.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["GET"])
    def top(self, request, *args, **kwargs):
        songs = self.get_queryset()
        songs = songs.order_by('-listened')[:3]
        serializer = SongsSerializer(songs, many=True)
        return Response(data=serializer.data)

    @action(detail=True, methods=["POST"])
    def albom(self, request, *args, **kwargs):
        song = self.get_object()
        albom = song.albom
        serializer = AlbomSerializer(albom)
        return Response(data=serializer.data)

    @action(detail=True, methods=["POST"])
    def artist(self, request, *args, **kwargs):
        song = self.get_object()
        artist = song.albom.artist
        serializer = ArtistSerializer(artist)
        return Response(data=serializer.data)


    # def get(self, request, id):
    #     try:
    #         song = Songs.objects.get(id=id)
    #         serializer = SongsSerializer(song)
    #         return Response(data=serializer.data)
    #     except:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #
    # def patch(self, request, id):
    #     song = Songs.objects.get(id=id)
    #     serializer = SongsSerializer(instance=song, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(data=serializer.data, status=status.HTTP_200_OK)
    #
    #     return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def put(self, request, id):
    #     song = Songs.objects.get(id=id)
    #     serializer = SongsSerializer(instance=song, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(data=serializer.data, status=status.HTTP_200_OK)
    #
    #     return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self, request, id):
    #     song = Songs.objects.get(id=id)
    #     song.delete()
    #
    #     return Response(status=status.HTTP_204_NO_CONTENT)
