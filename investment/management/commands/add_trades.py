import pandas as pd
from django.core.management.base import BaseCommand
from investment.models import Trades
from sqlalchemy import create_engine
from datetime import datetime

class Command(BaseCommand):
    help = "A command to add data from an Excel file to the Trades table"

    def handle(self, *args, **options):
        excel_file = 'data/trades.xlsx'
        df = pd.read_excel(excel_file)

        for index, row in df.iterrows():
             # To convert date string to the Django expected format (YYYY-MM-DD), because in Excel files date was formatted differently
            investment_date = datetime.strptime(row['investment_date'], '%d/%m/%Y').strftime('%Y-%m-%d')
            maturity_date = datetime.strptime(row['maturity_date'], '%d/%m/%Y').strftime('%Y-%m-%d')

            # Convertation of percentage interest rate to decimal
            interest_rate_percent = row['interest_rate']
            # Removal of the '%' sign and convert to decimal
            interest_rate_decimal = float(interest_rate_percent.rstrip('%')) / 100.0

            Trades.objects.create(
                loan_id=row['loan_id'],
                investment_date=investment_date,
                maturity_date=maturity_date,
                interest_rate=interest_rate_decimal
                )