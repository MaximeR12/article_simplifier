from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Analysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    input_text = models.TextField()
    output_text = models.TextField(blank=True)
    output_language = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"Analysis by {self.user.username} on {self.timestamp}"

    class Meta:
        verbose_name_plural = "Analyses"
        ordering = ['-timestamp']
