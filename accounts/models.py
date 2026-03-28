from django.db import models
from django.contrib.auth.models import User


# Room Model
class Room(models.Model):
    room_number = models.IntegerField()
    capacity = models.IntegerField()
    available_beds = models.IntegerField()

    def __str__(self):
        return f"Room {self.room_number}"


# Student Model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 🔥 IMPORTANT
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Complaint Model
class Complaint(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    issue = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.issue
    
class Fee(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.student.name} - {self.status}"