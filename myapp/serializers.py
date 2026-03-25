from rest_framework import serializers
from .models import ContactMessage, SourceCode, TestCase

class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = [
            "id",
            "test_title",
            "test_description",
            "test_input",
            "expected_output",
            "severity_level",
        ]

class SourceCodeSerializer(serializers.ModelSerializer):
    test_cases = TestCaseSerializer(many=True, read_only=True)

    class Meta:
        model = SourceCode
        fields = ['id', 'language', 'code_text', 'test_cases','created_at','test_cases']
        read_only_fields= ['user']


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"