from django.contrib import admin
from .models import Strategy, Backtest, HistoricalPriceData, Trade, TradeResults, Signal, Notification

# Register your models here.


@admin.register(Strategy)
class StrategyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'status', 'created_at')
    search_fields = ('name', 'user__username')
    list_filter = ('status', 'created_at')

@admin.register(Backtest)
class BacktestAdmin(admin.ModelAdmin):
    list_display = ('strategy', 'start_date', 'end_date', 'initial_capital', 'final_capital')
    list_filter = ('strategy', 'start_date', 'end_date')

@admin.register(HistoricalPriceData)
class HistoricalPriceDataAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'date', 'open_price', 'close_price', 'high_price', 'low_price', 'volume')
    search_fields = ('symbol',)
    list_filter = ('symbol', 'date')

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('strategy', 'symbol', 'order_type', 'price', 'quantity', 'executed_at', 'trade_type')
    list_filter = ('strategy', 'symbol', 'order_type', 'trade_type')


@admin.register(TradeResults)
class TradeResultsAdmin(admin.ModelAdmin):
    list_display = ('trade', 'current_price', 'profit_loss', 'updated_at')

@admin.register(Signal)
class SignalAdmin(admin.ModelAdmin):
    list_display = ('strategy', 'symbol', 'signal_type', 'signal_date', 'signal_price', 'executed')
    list_filter = ('strategy', 'signal_type', 'signal_date', 'executed')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'signal', 'notification_type', 'sent_at')