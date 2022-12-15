from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination

from albums.models import Album

from .models import Song
from .serializers import SongSerializer


class SongView(ListCreateAPIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = SongSerializer
    queryset = Song.objects.all()

    def perform_create(self, serializer: SongSerializer):
        album = get_object_or_404(Album, id=self.kwargs["pk"])
        return serializer.save(album_id=album.id)
