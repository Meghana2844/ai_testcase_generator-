from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


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
    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)