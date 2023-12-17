from django.urls import path, include
from investment.api.views import trades_list, cash_flows_list
from .views import trades_list, cash_flows_list, gross_expected_amount, realized_amount, remaining_invested_amount, closing_date, trade_details, total_invested_amount

urlpatterns = [
    path('list1/', trades_list, name='trades-list'), 
    path('list2/', cash_flows_list, name='cash-flows-list'),
    path('gross_expected_amount/<str:loan_id>/<str:reference_date>/', gross_expected_amount, name='gross-expected-amount'),
    path('realized_amount/<str:loan_id>/<str:reference_date>/', realized_amount, name='realized-amount'),
    path('remaining_invested_amount/<str:loan_id>/<str:reference_date>/', remaining_invested_amount, name='remaining-invested-amount'),
    path('closing_date/<str:loan_id>/', closing_date, name='closing-date'),
    path('trades/details/<str:loan_id>/', trade_details, name='trade-details'),
    path('trades/total_invested_amount/', total_invested_amount, name='total-invested-amount'),
    path('trades/total_invested_amount/<str:loan_id>/', total_invested_amount, name='total-invested-amount-by-trade'),
]