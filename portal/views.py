import base64
import json
import secrets
import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
import cv2
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import AttendanceLog, StudentProfile, StaffProfile, SubscriptionPayment
import numpy as np
import face_recognition
import traceback
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import traceback
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
# -------------------------------------------------------------------------
# 🤖 FACE RECOGNITION ENGINES INITIALIZATION
# -------------------------------------------------------------------------


# -------------------------------------------------------------
# GLOBAL FACE DATABASE SETUP (Inside views.py)
# -------------------------------------------------------------
# -------------------------------------------------------------
# GLOBAL FACE DATABASE SETUP (Inside views.py)
# -------------------------------------------------------------
import os
import face_recognition
from django.conf import settings

known_face_encodings = []
known_face_names = []

try:
    image_name = 'my_profile.jpg'
    image_path = os.path.join(settings.BASE_DIR, 'static', 'images', image_name)
    
    if os.path.exists(image_path):
        # Load raw file
        reference_image = face_recognition.load_image_file(image_path)
        encodings_list = face_recognition.face_encodings(reference_image)
        
        if len(encodings_list) > 0:
            # 🛠️ KEEP AS NATIVE NUMPY ARRAY (Do not use .tolist() here)
            known_face_encodings = [encodings_list[0]]
            
            # ⚠️ Change this to your exact name to show on your phone screen
            known_face_names = ["Your Full Name"] 
            print("--> Success: Biometric database loaded natively!")
        else:
            print(f"--> Error: No face could be extracted from image file: '{image_name}'")
    else:
        print(f"--> Warning: Missing base reference image layer at: {image_path}")
        
except Exception as e:
    print(f"--> Error loading biometric profile: {e}")

# 🏠 LANDING & INDEX ROUTINES
def landing_page(request):
    return render(request, 'portal/landing.html')

def index_view(request):
    return render(request, 'portal/index.html')


# 📂 STUDENT PROFILE MIGRATION HANDLER
def create_profile_view(request):
    if not request.user.is_authenticated:
        return redirect('portal_login')
    return render(request, 'portal/create_profile.html')


# 🔓 AUTHENTICATION SYSTEM MANAGEMENT (LOGIN & LOGOUT)
def login_view(request):
    if request.user.is_authenticated:
        return redirect('portal_dashboard')
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('portal_dashboard')
        else:
            messages.error(request, "Invalid username handle or secret key configuration.")
    else:
        form = AuthenticationForm()
        
    return render(request, 'portal/login.html', {'form': form})


def logout_action(request):
    """
    Safely terminates the active user session and returns back to the gateway landing view.
    """
    auth_logout(request)
    messages.info(request, "Session successfully closed. Secure terminal signed out.")
    return redirect('portal_login')


# 💳 MAIN SYSTEM DASHBOARD CONTROL NODE
def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('portal_login')
    if request.method == "POST":
        action = request.POST.get('action')
        if action == "initialize_paystack_payment":
            invoice_id = request.POST.get('invoice_id')
            try:
                invoice = SubscriptionPayment.objects.get(id=invoice_id, status='PENDING')
                reference_token = f"LASOP_REF_{secrets.token_hex(8).upper()}"
                invoice.payment_reference = reference_token
                invoice.save()
                return JsonResponse({
                    'success': True,
                    'reference': reference_token,
                    'amount_kobo': int(invoice.amount * 100),
                    'email': invoice.student.user.email,
                    'public_key': settings.PAYSTACK_PUBLIC_KEY
                })
            except SubscriptionPayment.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Invoice not localized.'})
        elif action == "verify_payment_success":
            reference = request.POST.get('reference')
            try:
                invoice = SubscriptionPayment.objects.get(payment_reference=reference)
                invoice.status = 'PAID'
                invoice.save()
                messages.success(request, f"Transaction Cleared!")
                return JsonResponse({'success': True})
            except SubscriptionPayment.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Record conflict.'})
    try:
        current_profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        current_profile = None
    context = {
        'profile': current_profile,
        'students': StudentProfile.objects.all().select_related('user'),
        'staff_members': StaffProfile.objects.all().select_related('user'),
        'payments': SubscriptionPayment.objects.all().select_related('student__user'),
        'attendance_logs': AttendanceLog.objects.all().select_related('student__user').order_by('-timestamp')[:5]
    }
    return render(request, 'portal/dashboard.html', context)


# 📝 AUTOMATED ACCOUNT REGISTRATION WITH PASSPORT ENROLLMENT
def register_view(request):
    from django.contrib.auth.models import User
    if request.user.is_authenticated:
        return redirect('portal_dashboard')
    if request.method == "POST":
        first_name_input = request.POST.get('first_name')
        last_name_input = request.POST.get('last_name')
        username_handle = request.POST.get('username')
        email_address = request.POST.get('email')
        password_secret = request.POST.get('password')
        uploaded_photo = request.FILES.get('biometric_photo')
        if User.objects.filter(username=username_handle).exists():
            messages.error(request, "Username already registered.")
            return render(request, 'portal/register.html')
        new_user = User.objects.create_user(
            username=username_handle, email=email_address, password=password_secret,
            first_name=first_name_input, last_name=last_name_input
        )
        auth_login(request, new_user)
        return redirect('portal_dashboard')
    return render(request, 'portal/register.html')


# 📊 ATTENDANCE HISTORY LIST VIEW
class AttendanceDashboardView(LoginRequiredMixin, ListView):
    model = AttendanceLog
    template_name = 'attendance_dashboard.html'
    context_object_name = 'logs'
    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.username == 'admin':
            return AttendanceLog.objects.all().order_by('-id')
        return AttendanceLog.objects.filter(student__user=self.request.user).order_by('-id')

# -------------------------------------------------------------
# GLOBAL FACE DATABASE SETUP
# Populate these lists with your reference face signatures.
# -------------------------------------------------------------
# --- SIMULATED MEMORY BANK DATABASE ---
# Ensure these variables are populated, or detection will always return "Unknown Face"
known_face_encodings = []  
known_face_names = []      

@method_decorator(csrf_exempt, name='dispatch')
class FaceIDVerificationView(View):
    def post(self, request, *args, **kwargs):
        try:
            body_data = json.loads(request.body)
            img_b64_string = body_data.get('image')
            
            if not img_b64_string:
                return JsonResponse({'status': 'error', 'message': 'Missing image context frame.'}, status=400)
            
            if "," in img_b64_string:
                _, encoded = img_b64_string.split(",", 1)
            else:
                encoded = img_b64_string
            
            img_bytes = base64.b64decode(encoded)
            np_array = np.frombuffer(img_bytes, dtype=np.uint8)
            frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
            
            if frame is None:
                return JsonResponse({'status': 'error', 'message': 'Failed to decode frame arrays.'}, status=400)
            
            # Standardize RGB color mapping layout
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Execute primary scanning pass
            face_locations = face_recognition.face_locations(rgb_frame)
            
            # 🔄 PHONE AUTO-ROTATION WORKAROUND: Force check frame shifts if initial pass is 0
            if not face_locations:
                for angle in [cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_180, cv2.ROTATE_90_COUNTERCLOCKWISE]:
                    rotated_bgr = cv2.rotate(frame, angle)
                    rotated_rgb = cv2.cvtColor(rotated_bgr, cv2.COLOR_BGR2RGB)
                    face_locations = face_recognition.face_locations(rotated_rgb)
                    if face_locations:
                        rgb_frame = rotated_rgb
                        break
            
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            detected_faces = []
            
            for face_loc, face_encoding in zip(face_locations, face_encodings):
                name = "Unknown Face"
                
                if len(known_face_encodings) > 0:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.75)
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    if len(face_distances) > 0:
                        best_match = np.argmin(face_distances)
                        if matches[best_match]:
                            name = known_face_names[best_match]
                
                top, right, bottom, left = face_loc
                detected_faces.append({
                    "name": name,
                    "coordinates": {"top": int(top), "right": int(right), "bottom": int(bottom), "left": int(left)}
                })
                
            return JsonResponse({'status': 'success', 'faces': detected_faces}, status=200)
            
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
