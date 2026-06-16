# portal/models.py
from django.db import models
from django.contrib.auth.models import User

# ADDING CLASSGRADE TO SATISFY THE IMPORTER
class ClassGrade(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    class Meta:
        db_table = 'class_grades'

    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    TRACK_CHOICES = [
        ('fullstack', 'Fullstack Development'),
        ('frontend', 'Frontend Development'),
        ('backend', 'Backend Node.js / Python'),
        ('data_science_ai', 'Data Science & AI'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    program_track = models.CharField(max_length=20, choices=TRACK_CHOICES)
    face_vector_initialized = models.BooleanField(default=False)
    face_embedding_data = models.TextField(blank=True, null=True) 
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'student_profiles'

    def __str__(self):
        return f"{self.user.username} - {self.get_program_track_display()}"

class StaffProfile(models.Model):
    ROLE_CHOICES = [
        ('teacher', 'Academic Instructor'),
        ('accounts', 'Accounts Personnel'),
        ('admin', 'System Administrator'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    department = models.CharField(max_length=100)

    class Meta:
        db_table = 'staff_profiles'

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_role_display()}"

# portal/models.py
# Find the SubscriptionPayment class model and replace it with this version:

class SubscriptionPayment(models.Model):
    STATUS_CHOICES = [('PAID', 'Paid'), ('PENDING', 'Pending'), ('FAILED', 'Failed')]
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='payments')
    item_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    # Unique database parameter column to store Paystack reference ID string blocks
    payment_reference = models.CharField(max_length=100, blank=True, null=True, unique=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subscription_payments'
