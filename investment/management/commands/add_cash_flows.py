from sqlalchemy import create_engine
import pandas as pd
from django.core.management.base import BaseCommand
from investment.models import Cash_flows, Trades
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
import decimal

class Command(BaseCommand):
    help = "A command to add data from an Excel file to the Cash_flows table"

    def handle(self, *args, **options):
        excel_file = 'data/cash_flows.xlsx'
        df = pd.read_excel(excel_file)

        for index, row in df.iterrows():
            try:
                amount = decimal.Decimal(row['amount'].replace(',', '').strip())
            except decimal.InvalidOperation:
                print(f"Invalid amount value in row {index + 1}: {row['amount']}")
                continue

            try:
                trade = Trades.objects.get(loan_id=row['loan_id'])
            except ObjectDoesNotExist:
                print(f"Trade with loan_id {row['loan_id']} does not exist.")
                # To handle the case where the trade does not exist, for example log the error or skip the row
                continue

            # To convert date string to the Django expected format (YYYY-MM-DD), because in Excel files date was formatted differently
            cashflow_date = datetime.strptime(row['cashflow_date'], '%d/%m/%Y').strftime('%Y-%m-%d')

            Cash_flows.objects.create(
                cashflow_id=row['cashflow_id'],
                loan_id=trade,
                cashflow_date=cashflow_date,
                cashflow_currency=row['cashflow_currency'],
                cashflow_type=row['cashflow_type'],
                amount=amount  # We use the above formatted amount here
            )