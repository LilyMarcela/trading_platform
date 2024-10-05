# trading/urls.py (app-level)

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UserRegisterView
from . import views
urlpatterns = [
    path('strategies/<int:strategy_id>/', views.strategy_detail, name='strategy_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard URL
    path('register/', UserRegisterView.as_view(), name='register'),  # Registration URL
    path('login/', auth_views.LoginView.as_view(template_name='trading/login.html'), name='login'),  # Login URL
    path('logout/', auth_views.LogoutView.as_view(template_name='trading/logout.html'), name='logout'),  # Logout URL
    path('strategies/', views.strategy_list, name='strategy_list'),  # List strategies
    path('strategies/create/', views.create_strategy, name='create_strategy'),
    path('strategies/run/<int:strategy_id>/', views.run_strategy, name='run_strategy'),

]
