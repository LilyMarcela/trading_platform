from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # Logic to display the dashboard, fetch relevant data for the user
    return render(request, 'trading/dashboard.html')
