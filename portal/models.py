from django.db import models
from django.contrib.auth.models import User

# 1. CORE CLASS GRADE LEDGER TABLE
class ClassGrade(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    class Meta:
        db_table = 'class_grades'

    def __str__(self):
        return self.name


# 2. STUDENT USER MASTER BIOMETRIC PROFILE TABLE
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    program_track = models.CharField(max_length=100, blank=True, null=True)
    
    # 📷 CRITICAL EXPLICIT IMAGE FIELD FOR PORTRAIT PASSPORT UPLOADS
    face_id_image = models.ImageField(upload_to='face_profiles/', blank=True, null=True)
    
    # Mathematical data metrics text string tracking block
    face_vector_initialized = models.BooleanField(default=False)
    face_embedding_data = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Student Profile"


# 3. STAFF PROFILE TABLE (FIXED: Added to support your views.py queries)
class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Staff Profile"


# 4. FINANCIAL TUITION GATEWAY SUBSCRIPTION MANAGEMENT TABLE
class SubscriptionPayment(models.Model):
    STATUS_CHOICES = [('PAID', 'Paid'), ('PENDING', 'Pending'), ('FAILED', 'Failed')]
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='payments')
    item_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    payment_reference = models.CharField(max_length=100, blank=True, null=True) # Supported pipeline tracking
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subscription_payments'


# 5. BIOMETRIC LOGGING SYSTEM ATTENDANCE TRACKER TABLE
class AttendanceLog(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='attendance_logs')
    timestamp = models.DateTimeField(auto_now_add=True)
    verified_via_face_id = models.BooleanField(default=False)

    class Meta:
        db_table = 'attendance_logs'
