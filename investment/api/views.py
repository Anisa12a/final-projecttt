from rest_framework.decorators import api_view
from rest_framework.response import Response
from investment.models import Trades, Cash_flows
from investment.api.serializers import TradesSerializer, CashFlowsSerializer
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta

def calculate_gross_expected_amount(trade, reference_date):
    daily_interest_rate = trade.interest_rate / 365
    invested_amount = sum([cf.amount for cf in Cash_flows.objects.filter(loan_id=trade, cashflow_type='funding', cashflow_date__lte=reference_date)])
    passed_days = (reference_date - trade.investment_date).days
    gross_expected_interest_amount = daily_interest_rate * invested_amount * passed_days
    return invested_amount + gross_expected_interest_amount

def calculate_realized_amount(trade, reference_date):
    return sum([cf.amount for cf in Cash_flows.objects.filter(loan_id=trade, cashflow_type='repayment', cashflow_date__lte=reference_date)])

def calculate_remaining_invested_amount(trade, reference_date):
    invested_amount = calculate_gross_expected_amount(trade, reference_date)
    realized = calculate_realized_amount(trade, reference_date)
    return invested_amount - realized

def calculate_closing_date(trade):
    cash_flows = Cash_flows.objects.filter(loan_id=trade).order_by('cashflow_date')
    total_realized_amount = 0
    for cf in cash_flows:
        if cf.cashflow_type == 'repayment':
            total_realized_amount += cf.amount
            if total_realized_amount > calculate_gross_expected_amount(trade, cf.cashflow_date):
                return cf.cashflow_date
    return None

@api_view(['GET'])
def gross_expected_amount(request, loan_id, reference_date):
    trade = get_object_or_404(Trades, loan_id=loan_id)
    reference_date = datetime.strptime(reference_date, '%Y-%m-%d').date()
    amount = calculate_gross_expected_amount(trade, reference_date)
    return Response({'gross_expected_amount': amount})

@api_view(['GET'])
def realized_amount(request, loan_id, reference_date):
    trade = get_object_or_404(Trades, loan_id=loan_id)
    reference_date = datetime.strptime(reference_date, '%Y-%m-%d').date()
    amount = calculate_realized_amount(trade, reference_date)
    return Response({'realized_amount': amount})

@api_view(['GET'])
def remaining_invested_amount(request, loan_id, reference_date):
    trade = get_object_or_404(Trades, loan_id=loan_id)
    reference_date = datetime.strptime(reference_date, '%Y-%m-%d').date()
    amount = calculate_remaining_invested_amount(trade, reference_date)
    return Response({'remaining_invested_amount': amount})

@api_view(['GET'])
def closing_date(request, loan_id):
    trade = get_object_or_404(Trades, loan_id=loan_id)
    closing_date = calculate_closing_date(trade)
    if closing_date:
        return Response({'closing_date': closing_date})
    else:
        return Response({'message': 'Closing date not found or trade is not yet closed.'})
    
#An API to get detailed information about a specific trade, including its associated cash flows.
@api_view(['GET'])
def trade_details(request, loan_id):
    trade = get_object_or_404(Trades, loan_id=loan_id)
    cash_flows = Cash_flows.objects.filter(loan_id=trade)
    trade_serializer = TradesSerializer(trade)
    cash_flows_serializer = CashFlowsSerializer(cash_flows, many=True)
    return Response({
        'trade': trade_serializer.data,
        'cash_flows': cash_flows_serializer.data
    })


#An API to calculate the total amount invested in all trades or a specific trade.
@api_view(['GET'])
def total_invested_amount(request, loan_id=None):
    if loan_id:
        trades = Trades.objects.filter(loan_id=loan_id)
    else:
        trades = Trades.objects.all()
    
    total_amount = 0
    for trade in trades:
        total_amount += sum(cf.amount for cf in Cash_flows.objects.filter(loan_id=trade, cashflow_type='funding'))

    return Response({'total_invested_amount': total_amount})


@api_view()
def trades_list(request):
    trades = Trades.objects.all()
    serializer = TradesSerializer(trades, many=True)
    return Response(serializer.data)

@api_view()
def cash_flows_list(request):
    cash_flows = Cash_flows.objects.all()
    serializer = CashFlowsSerializer(cash_flows, many=True)
    return Response(serializer.data)