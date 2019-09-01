from django.urls import path
from django.contrib.auth.views import (
LoginView,LogoutView, PasswordResetView, PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
)
from . import views
from django.urls import reverse_lazy


app_name ="results"

urlpatterns = [
    path('view_results/',views.view_results, name='view_results'),
    path('display_results/',views.display_results, name='display_results'),
    path('login/', LoginView.as_view(template_name='results/login.html'),name='login'),
    path('logout/', LogoutView.as_view(template_name='results/logout.html'),name='logout'),
    path('register/',views.register, name='register'),
    path('admin-register/', views.admin_register, name = 'admin_register'),
    path('profile/',views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),

    path('profile/reset-password/', PasswordResetView.as_view(template_name='results/reset_password.html',
    success_url = reverse_lazy('results:password_reset_done'),
    email_template_name='results/reset_password_email.html'),
    name='password_reset'),

    path('profile/reset-password/done/', PasswordResetDoneView.as_view(
    template_name='results/reset_password_done.html'),
    name='password_reset_done'),

    path('profile/reset-password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
    template_name='results/reset_password_confirm.html',
    success_url = reverse_lazy('results:password_reset_complete')),
    name='password_reset_confirm'),

    path('profile/reset-password/complete/', PasswordResetCompleteView.as_view(
    template_name='results/reset_password_complete.html'),
    name='password_reset_complete'),

    path('upload-results/',views.upload_results, name='upload_results'),
    path('save-results/',views.save_results, name='save_results'),
    path('permission-required/',views.permission_required, name='permission_required' ),
    path('invalid-register-number/',views.invalid_register_number, name= 'invalid_register_number'),

]
