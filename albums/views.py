from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Album
from .serializers import AlbumSerializer


class AlbumView(ListCreateAPIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = AlbumSerializer
    queryset = Album.objects.all()

    def perform_create(self, serializer: AlbumSerializer):
        return serializer.save(user_id=self.request.user.id)
