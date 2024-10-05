# trading/urls.py

from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .views import strategy_views, dashboard_views, user_views


# Create DRF Router
router = DefaultRouter()

# Register ViewSets
router.register(r'users', user_views.UserViewSet)
router.register(r'strategies', strategy_views.StrategyViewSet)

# Define URL patterns
urlpatterns = [
    # Standard paths for user authentication and dashboard
    path('dashboard/', dashboard_views.dashboard, name='dashboard'),  # Dashboard URL
    path('login/', auth_views.LoginView.as_view(template_name='trading/login.html'), name='login'),  # Login URL
    path('logout/', auth_views.LogoutView.as_view(template_name='trading/logout.html'), name='logout'),  # Logout URL

    # Custom route for running strategies

    # Include router-generated routes (e.g., for strategies and accounts)
    path('', include(router.urls)),

]
