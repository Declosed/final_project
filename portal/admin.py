from django.contrib import admin
from .models import ClassGrade, StudentProfile, StaffProfile, SubscriptionPayment, AttendanceLog

@admin.register(ClassGrade)
class ClassGradeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    # FIXED: Replaced 'registration_date' with valid model attributes from your models.py
    list_display = ['user', 'program_track', 'face_vector_initialized']
    search_fields = ['user__username', 'program_track']

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    # FIXED: Cleared out the missing 'role' field reference to prevent system check crashes
    list_display = ['user', 'department']
    search_fields = ['user__username', 'department']

@admin.register(SubscriptionPayment)
class SubscriptionPaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'item_name', 'amount', 'status', 'updated_at']
    list_filter = ['status']
    search_fields = ['student__user__username', 'item_name']

@admin.register(AttendanceLog)
class AttendanceLogAdmin(admin.ModelAdmin):
    list_display = ['student', 'timestamp', 'verified_via_face_id']
    list_filter = ['verified_via_face_id']
