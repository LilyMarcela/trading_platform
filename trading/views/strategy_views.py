# views/strategy_views.py

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Strategy
from ..serializers import StrategySerializer

from django.views.generic import ListView, DetailView, FormView
from django.shortcuts import render, get_object_or_404
from ..models import Strategy
from ..forms import RunStrategyForm
from ..services.market_day import fetch_market_data  # Assuming this is where your market data logic resides
from ..services.strategy_loader import load_strategy  # Assuming this is where your strategy logic resides
import pandas as pd
from ..serializers import StrategySerializer

# ViewSet for handling all CRUD operations for the Strategy model
class StrategyViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling all CRUD operations for the Strategy model.
    """
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer

    def get_queryset(self):
        # Return only the strategies belonging to the logged-in user
        return Strategy.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Custom create logic, ensuring the user is set
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        # Custom update logic
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        # Handles partial updates (PATCH)
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Custom delete logic
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['get'], url_path='run')
    def run_strategy(self, request, pk=None):
        """
        Custom action to run a strategy based on the strategy ID and return market data.
        """
        # Fetch the strategy based on the strategy_id (pk) and the user
        strategy = get_object_or_404(Strategy, id=pk, user=self.request.user)

        # Fetch market data (for example, using yfinance)
        market_data = fetch_market_data('AAPL', '2024-10-01', '2024-10-05')

        # Convert DataFrame to a list of dictionaries for JSON compatibility
        market_data_list = market_data.reset_index().to_dict(orient='records')

        # Convert Pandas Timestamps to strings for JSON serialization
        for row in market_data_list:
            if isinstance(row['Date'], pd.Timestamp):
                row['Date'] = row['Date'].strftime('%Y-%m-%d')  # Convert to string format

        # Return the strategy and market data as a JSON response
        return Response({
            'strategy': strategy.name,
            'market_data': market_data_list
        }, status=status.HTTP_200_OK)

