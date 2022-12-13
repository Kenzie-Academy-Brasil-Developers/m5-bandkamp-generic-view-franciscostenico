from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User
from .serializers import UserSerializer
from .permissions import IsAccountOwner


class UserView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]

    serializer_class = UserSerializer
    queryset = User.objects.all()
