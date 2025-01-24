from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('RegisterHere/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset-confirm/<str:uidb64>/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('password-change/', views.password_change, name='password_change'),
    
    # path('2FA/', views.TwoFactors, name='two_factor_setup'),
    path('profile/', views.profile_view, name='profile'),
    path('account/', views.account_view, name='account'),
    path('performance/', views.performance_view, name='performance'),
]