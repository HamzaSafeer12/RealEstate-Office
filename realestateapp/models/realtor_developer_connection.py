from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserConnection(models.Model):
    realtor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('realtor', 'receiver')  # Prevent duplicate requests