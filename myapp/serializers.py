from rest_framework import serializers
from .models import ContactMessage, Project, SourceCode, TestCase

class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = '__all__'

class SourceCodeSerializer(serializers.ModelSerializer):
    test_cases = TestCaseSerializer(many=True, read_only=True)

    class Meta:
        model = SourceCode
        fields = ['id', 'project', 'file_name', 'language', 'code_text', 'test_cases']

class ProjectSerializer(serializers.ModelSerializer):
    source_codes = SourceCodeSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'description', 'created_at', 'source_codes']

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"