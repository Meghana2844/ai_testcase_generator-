from django.contrib import admin

from myapp.models import ContactMessage, GenerationHistory, SourceCode, TestCase

admin.site.register(TestCase)
admin.site.register(SourceCode)
admin.site.register(GenerationHistory)
admin.site.register(ContactMessage)