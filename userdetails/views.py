from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from .serializers import UserSerializer, RegisterSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    
    def get_serializer_class(self):
       
        if self.action == 'create':
            return RegisterSerializer
        return UserSerializer

    def get_permissions(self):
       
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]