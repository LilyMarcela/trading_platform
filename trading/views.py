# trading/views.py

from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormView
from .forms import UserRegisterForm, StrategyForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Strategy
from .services.strategy_loader import load_strategy
from .services.market_day import fetch_market_data
import pandas as pd
import ipdb




class UserRegisterView(SuccessMessageMixin, FormView):
    template_name = 'trading/register.html'  
    form_class = UserRegisterForm 
    success_url = reverse_lazy('login') 
    success_message = "Your account has been created successfully!" 

    def form_valid(self, form):
        form.save()  # Save the user
        return super().form_valid(form)  

@login_required
def dashboard(request):
    # Retrieve the latest market data from the session
    latest_market_data = request.session.get('latest_market_data', [])
    ipdb.set_trace()  # Execution will pause here, and you'll enter the debugger
    request.session.modified = True

    print("Retrieved market data from session:", latest_market_data)


    return render(request, 'trading/dashboard.html', {
        'latest_market_data': latest_market_data
    })


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



#@login_required
#def run_strategy(request, strategy_id):
#    strategy = get_object_or_404(Strategy, id=strategy_id, user=request.user)
    
    # Fetch market data (replace with actual market data fetching logic)
#    market_data = fetch_market_data('AAPL', pd.Timestamp('2023-01-01'), pd.Timestamp('2023-12-31'))
    
    # Load and apply the strategy dynamically
#    strategy_logic = load_strategy(strategy.name, {'short_window': strategy.short_window, 'long_window': strategy.long_window})
#    signals = strategy_logic.generate_signals(market_data)
    
#    return render(request, 'trading/run_strategy.html', {'strategy': strategy, 'signals': signals})
@login_required
def run_strategy(request, strategy_id):
    strategy = get_object_or_404(Strategy, id=strategy_id, user=request.user)

    # Fetch market data (e.g., using yfinance)
    market_data = fetch_market_data('AAPL', '2024-10-01', '2024-10-05')
    ipdb.set_trace()


    # Convert DataFrame to a list of dictionaries
    market_data_list = market_data.reset_index().to_dict(orient='records')

    # Convert Pandas Timestamps to strings (or you can convert to datetime if needed)
    for row in market_data_list:
        if isinstance(row['Date'], pd.Timestamp):
            row['Date'] = row['Date'].strftime('%Y-%m-%d')  # Convert to string format

    # Store the market data in the session
    request.session['latest_market_data'] = market_data_list
    request.session.modified = True
    print("Market Data Before Storing in Session:", market_data_list)

    return render(request, 'trading/run_strategy.html', {
        'strategy': strategy,
        'market_data': market_data_list,
    })

@login_required
def strategy_detail(request, strategy_id):
    # Fetch the specific strategy
    strategy = get_object_or_404(Strategy, id=strategy_id, user=request.user)
    
    # Render the strategy details to the template
    return render(request, 'trading/strategy_detail.html', {
        'strategy': strategy
    })