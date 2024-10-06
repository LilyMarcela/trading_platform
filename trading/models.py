from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    risk_profile = models.CharField(
        max_length=20,
        choices=[('conservative', 'Conservative'), ('moderate', 'Moderate'), ('aggressive', 'Aggressive'), ('expert', 'Expert')],
        default='moderate'
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class Strategy(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who owns the strategy
    status = models.CharField(
        max_length=20,
        choices=[('active', 'Active'), ('paused', 'Paused'), ('completed', 'Completed')],
        default='active'
    )
    is_prebuilt = models.BooleanField(default=False)  # True if this is a pre-built strategy
    is_customizable = models.BooleanField(default=True)  # True if users can customize it
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class StrategyConfiguration(models.Model):
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE, related_name='configurations')
    parameter_name = models.CharField(max_length=255)  # Name of the parameter
    parameter_value = models.CharField(max_length=255)  # Value of the parameter

    def __str__(self):
        return f'{self.parameter_name}: {self.parameter_value} (Strategy: {self.strategy.name})'


class Backtest(models.Model):
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    initial_capital = models.DecimalField(max_digits=20, decimal_places=4)
    final_capital = models.DecimalField(max_digits=20, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)

class HistoricalPriceData(models.Model):
    symbol = models.CharField(max_length=10)
    date = models.DateField()
    open_price = models.DecimalField(max_digits=30, decimal_places=10)
    close_price = models.DecimalField(max_digits=30, decimal_places=10)
    high_price = models.DecimalField(max_digits=30, decimal_places=10)
    low_price = models.DecimalField(max_digits=30, decimal_places=10)
    volume = models.DecimalField(max_digits=30, decimal_places=10)


class Trade(models.Model):
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    order_type = models.CharField(max_length=4, choices=(('BUY', 'buy'), ('SELL', 'sell')))
    price = models.DecimalField(max_digits=30, decimal_places=10)
    quantity = models.DecimalField(max_digits=30, decimal_places=10)
    executed_at = models.DateTimeField()
    trade_type = models.CharField(max_length=10, choices=(('backtest', 'Backtest'), ('real-time', 'Real-time')))

class TradeResults(models.Model):
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE)
    current_price = models.DecimalField(max_digits=30, decimal_places=10)
    profit_loss = models.DecimalField(max_digits=30, decimal_places=10)
    updated_at = models.DateTimeField(auto_now=True)

class Signal(models.Model):
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    signal_type = models.CharField(max_length=4, choices=(('BUY', 'Buy'), ('SELL', 'Sell')))
    signal_date = models.DateTimeField()
    signal_price =models.DecimalField(max_digits=30, decimal_places=10)
    executed = models.BooleanField(default=False)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    signal = models.ForeignKey(Signal, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=10, choices=(('email', 'Email'), ('sms', 'SMS')))
    sent_at = models.DateTimeField(auto_now_add=True)
 
