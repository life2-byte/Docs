from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    title = models.CharField(max_length=255, default="Untitled Document")
    content = models.TextField(blank=True, default="")  # HTML content from rich text editor
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_documents")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class SharedAccess(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="shares")
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shared_documents")
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('document', 'shared_with')  # avoid duplicate shares

    def __str__(self):
        return f"{self.document.title} shared with {self.shared_with.username}"