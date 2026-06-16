from django.urls import path
from .views import (
    login_view, logout_action, dashboard_view, 
    register_view, AttendanceDashboardView, FaceIDVerificationView,
    landing_page  # 🌟 Added the landing page view import here
)

urlpatterns = [
    # 🌟 CLEAN EXPLICIT ROUTING: Maps path paths directly to view functions
    path("", dashboard_view, name="portal_dashboard"), 
    path("landingpage/", landing_page, name="landing_page"), # 🌟 Added this line
    path("login/", login_view, name="portal_login"),
    path("logout/", logout_action, name="portal_logout"),
    path("register/", register_view, name="portal_register"),
    path("verify-face/", FaceIDVerificationView.as_view(), name="face_id_verify"),
    path("attendance/history/", AttendanceDashboardView.as_view(), name="attendance_dashboard"),
]
