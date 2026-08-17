from django.urls import path
from django.contrib.auth import views as auth_views #alising
from .views import *
urlpatterns = [
    path('',index,name='index'),
    path('about/',about,name='about'),
    path('contact/',contact,name='contact'),
    path('menu/',menu,name='menu'),
    path('services/',services,name='services'),
    path('testemonial/',testemonial,name='testemonial'),
    path('help/',help,name='help'),
    path('terms/',terms,name='terms'),
    path('privacy/',privacy,name='privacy'),
    # auth part
    path('register/',register,name='register'),
    path('log_in/',log_in,name='log_in'),
    path('log_out/',log_out,name='log_out'),
    path('password_change/',password_change,name='password_chnage'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html',html_email_template_name='auth/mail.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
]

