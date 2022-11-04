from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from user.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated()]

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        else:
            return self.permission_classes
