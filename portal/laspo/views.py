import secrets
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages  # Added missing import
from django.views import View
from .models import StudentProfile, StaffProfile, SubscriptionPayment, AttendanceLog

def dashboard_view(request):
    if request.method == "POST":
        action = request.POST.get('action')
        
        # 💳 SUB-ROUTINE C: INITIALIZE DIRECT TRANSACTION ENGINE REFERENCE
        if action == "initialize_paystack_payment":
            invoice_id = request.POST.get('invoice_id')
            try:
                invoice = SubscriptionPayment.objects.get(id=invoice_id, status='PENDING')
                
                # Generate unique tracking code string parameters block natively
                reference_token = f"LASOP_REF_{secrets.token_hex(8).upper()}"
                
                invoice.payment_reference = reference_token
                invoice.save()
                
                return JsonResponse({
                    'success': True,
                    'reference': reference_token,
                    'amount_kobo': int(invoice.amount * 100), # Paystack calculates pricing strings in Kobo/Cents
                    'email': invoice.student.user.email,
                    'public_key': settings.PAYSTACK_PUBLIC_KEY
                })
            except SubscriptionPayment.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Invoice already cleared or not localized.'})

        # 💳 SUB-ROUTINE D: CONFIRM TRANSACTION AND UPDATE MYSQL STATUS
        elif action == "verify_payment_success":
            reference = request.POST.get('reference')
            try:
                # In production, make a backend curl call to https://paystack.co{reference}
                invoice = SubscriptionPayment.objects.get(payment_reference=reference)
                invoice.status = 'PAID'
                invoice.save()
                
                messages.success(request, f"Transaction Cleared! Invoice for '{invoice.item_name}' updated to PAID.")
                return JsonResponse({'success': True})
            except SubscriptionPayment.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Payment logging parameter record conflict.'})

        # ... keep all existing register_student and register_staff action codes here ...

    # DEFAULT DATA CONTEXT READ PIPELINE
    context = {
        'students': StudentProfile.objects.all().select_related('user'),
        'staff_members': StaffProfile.objects.all().select_related('user'),
        'payments': SubscriptionPayment.objects.all().select_related('student__user'),
        'attendance_logs': AttendanceLog.objects.all().select_related('student__user').order_by('-timestamp')[:5]
    }
    return render(request, 'portal/dashboard.html', context)


# BIOMETRIC FACE ID VERIFICATION ENDPOINT
class FaceIDVerificationView(View):
    def post(self, request, *args, **kwargs):  # Fixed syntax error here
        # Placeholder logic for handling face biometrics
        return JsonResponse({'status': 'success', 'message': 'Endpoint reached!'})
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('portal_dashboard')
    else:
        form = AuthenticationForm()
        
    return render(request, 'portal/login.html', {'form': form})
