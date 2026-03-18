from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .services import AIService
from .models import ContactMessage, SourceCode
from .serializers import ContactMessageSerializer, SourceCodeSerializer


class SourceCodeViewSet(viewsets.ModelViewSet):
    serializer_class = SourceCodeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SourceCode.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        source_code = serializer.save()
        source_code.refresh_from_db()

        try:
            AIService.generate_and_store(source_code)
        except Exception as e:
            print(f"AI Error: {e}")




class GenerateTestCasesView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        code = request.data.get("code")
        language = request.data.get("language", "unknown") 
        if not code:
            return Response(
                {"error": "Code is required"},
                status=400
            )

        try:
            result = AIService.generate_from_code(code, language)

            return Response(result)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=500
            )
        



class ContactMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']

    def get_queryset(self):
        return ContactMessage.objects.none()