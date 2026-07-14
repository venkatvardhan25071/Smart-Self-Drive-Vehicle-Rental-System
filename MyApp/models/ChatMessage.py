from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    # Null=True allows anonymous users to chat
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Chat with {self.user or 'Guest'} at {self.created_at}"