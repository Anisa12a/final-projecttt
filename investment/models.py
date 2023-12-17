from django.db import models

# Create your models here.

class Trades (models.Model):
    loan_id = models.CharField(primary_key=True, max_length=50, db_column="loan_id")
    investment_date = models.DateField()
    maturity_date = models.DateField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)

class Cash_flows(models.Model):
    cashflow_id = models.CharField(primary_key=True, max_length=50, db_column="cashflow_id")
    loan_id = models.ForeignKey(Trades, db_column="loan_id", on_delete=models.CASCADE)
    cashflow_date = models.DateField()
    cashflow_currency = models.CharField(max_length=15)
    cashflow_type = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)