from django.db import models
from django.conf import settings

class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    project_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name

class SourceCode(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='source_codes')
    file_name = models.CharField(max_length=255)
    language = models.CharField(max_length=50)
    code_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name} ({self.language})"

class TestCase(models.Model):
    source_code = models.ForeignKey(SourceCode, on_delete=models.CASCADE, related_name='test_cases')
    test_title = models.CharField(max_length=255)
    test_description = models.TextField()
    test_input = models.TextField()
    expected_output = models.TextField()
    severity_level = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class GenerationHistory(models.Model):
    source_code = models.ForeignKey(SourceCode, on_delete=models.CASCADE, related_name='history')
    model_used = models.CharField(max_length=100)
    generation_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

