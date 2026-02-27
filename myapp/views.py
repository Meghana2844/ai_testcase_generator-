from rest_framework import viewsets, status
from rest_framework.response import Response
from .services import AIService
from .models import Project, SourceCode
from .serializers import ProjectSerializer, SourceCodeSerializer
from rest_framework.permissions import IsAuthenticated

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SourceCodeViewSet(viewsets.ModelViewSet):
    serializer_class = SourceCodeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        
        return SourceCode.objects.filter(project__user=self.request.user)

    def perform_create(self, serializer):
        source_code = serializer.save()
        
        source_code.refresh_from_db()
        
        try:
            AIService.generate_test_cases(source_code)
        except Exception as e:
            print(f"AI Error: {e}")