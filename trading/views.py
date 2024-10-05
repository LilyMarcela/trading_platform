# trading/views.py

from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormView
from .forms import UserRegisterForm, StrategyForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Strategy



class UserRegisterView(SuccessMessageMixin, FormView):
    template_name = 'trading/register.html'  
    form_class = UserRegisterForm 
    success_url = reverse_lazy('login') 
    success_message = "Your account has been created successfully!" 

    def form_valid(self, form):
        form.save()  # Save the user
        return super().form_valid(form)  

@login_required  # Ensure the user is logged in to access this page
def dashboard(request):
    return render(request, 'trading/dashboard.html')


@login_required
def create_strategy(request):
    if request.method == 'POST':
        form = StrategyForm(request.POST)
        if form.is_valid():
            strategy = form.save(commit=False)
            strategy.user = request.user  # Assign the current user to the strategy
            strategy.save()
            return redirect('strategy_list')  # Redirect to the strategy list after saving
    else:
        form = StrategyForm()
    
    return render(request, 'trading/create_strategy.html', {'form': form})

@login_required
def strategy_list(request):
    strategies = Strategy.objects.filter(user=request.user)
    return render(request, 'trading/strategy_list.html', {'strategies': strategies})