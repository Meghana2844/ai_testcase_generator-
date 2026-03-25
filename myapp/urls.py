from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SourceCodeViewSet, GenerateTestCasesView, ContactMessageViewSet

router = DefaultRouter()
router.register(r'source-code', SourceCodeViewSet, basename='sourcecode')
router.register(r'contact-messages', ContactMessageViewSet, basename='contactmessage')

urlpatterns = [
    path('', include(router.urls)),
    path('generate-testcases/', GenerateTestCasesView.as_view(), name='generate-testcases'),
] 