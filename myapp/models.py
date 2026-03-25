from django.db import models
from django.conf import settings



class SourceCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='source_codes')
    language = models.CharField(max_length=50)
    code_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} ({self.language})"

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



class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
 