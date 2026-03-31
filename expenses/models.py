from django.db import models
from django.contrib.auth.models import User


class Expense(models.Model):
    title = models.TextField()
    description = models.TextField()
    amount = models.FloatField()
    category = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='expenses'
    )

