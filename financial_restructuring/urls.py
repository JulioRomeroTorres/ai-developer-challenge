from django.urls import path
from .views.financial_optimizer import FinancialOptimizer
from .views.financial_user_information import FinancialUserInformation

urlpatterns = [
    path('user/:id', FinancialUserInformation.as_view(), name='Financial User Information'),
    path('optimizer', FinancialOptimizer.as_view(), name='Obtain Financial Plan'),
]