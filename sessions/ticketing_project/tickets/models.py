from django.db import models
from django.contrib.auth.models import User, AbstractUser

# class User(AbstractUser):
#     ROLES = [('customer', 'Customer'), ('agent','Agent'), ('admin','Admin')]
#     role = models.CharField(max_length=20, choices=ROLES, default='customer')

class Ticket(models.Model):
    STATUS_CHOICES = [('Open', 'Open'), ('Closed', 'Closed'), ('In Progress', 'In Progress')]
    PRIORITY_CHOICES = [('Low', '1'), ('Medium', '2'), ('High', '3')] 
    
    subject = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)