from django.db import models

class CustomerCashflow(models.Model):
    customer_id = models.CharField(max_length=20, primary_key=True)
    monthly_income_avg = models.DecimalField(max_digits=10, decimal_places=2)
    income_variability_pct = models.DecimalField(max_digits=5, decimal_places=1)
    essential_expenses_avg = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'customer_cashflow'

class CreditScoreHistory(models.Model):
    customer = models.ForeignKey(
        CustomerCashflow, 
        on_delete=models.CASCADE,
        related_name='credit_score_history'
    )
    date = models.DateField()
    credit_score = models.IntegerField()

    class Meta:
        db_table = 'credit_score_history'

class PaymentHistory(models.Model):
    PRODUCT_TYPES = [
        ('loan', 'Loan'),
        ('card', 'Card'),
    ]
    
    product_id = models.CharField(max_length=20)
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPES)
    customer = models.ForeignKey(
        CustomerCashflow, 
        on_delete=models.CASCADE,
        related_name='payment_histories'
    )
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'payments_history'

class Loan(models.Model):
    loan_id = models.CharField(max_length=20, primary_key=True)
    customer = models.ForeignKey(
        CustomerCashflow, 
        on_delete=models.CASCADE,
        related_name='loans'
    )
    product_type = models.CharField(max_length=20)
    principal = models.DecimalField(max_digits=12, decimal_places=2)
    annual_rate_pct = models.DecimalField(max_digits=5, decimal_places=1)
    remaining_term_months = models.IntegerField()
    collateral = models.BooleanField()
    days_past_due = models.IntegerField()

    class Meta:
        db_table = 'loans'

class Card(models.Model):
    card_id = models.CharField(max_length=20, primary_key=True)
    customer = models.ForeignKey(
        CustomerCashflow, 
        on_delete=models.CASCADE,
        related_name='cards'
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    annual_rate_pct = models.DecimalField(max_digits=5, decimal_places=1)
    min_payment_pct = models.DecimalField(max_digits=4, decimal_places=1)
    payment_due_day = models.IntegerField()
    days_past_due = models.IntegerField()

    class Meta:
        db_table = 'cards'