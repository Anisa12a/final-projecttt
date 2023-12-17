from rest_framework import serializers
from investment.models import Cash_flows, Trades

class TradesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trades
        fields = ['loan_id', 'investment_date', 'maturity_date', 'interest_rate']

class CashFlowsSerializer(serializers.ModelSerializer):
    # Using PrimaryKeyRelatedField for foreign key relationship
    loan_id = serializers.PrimaryKeyRelatedField(queryset=Trades.objects.all())

    class Meta:
        model = Cash_flows
        fields = ['cashflow_id', 'loan_id', 'cashflow_date', 'cashflow_currency', 'cashflow_type', 'amount']