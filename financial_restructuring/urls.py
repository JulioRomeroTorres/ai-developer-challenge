from django.urls import path
from .views.financial_optimizer import FinancialOptimizer
from .views.financial_user_information import FinancialUserInformation
from .views.agent_optimizer import AgentOptimizer

urlpatterns = [
    path('user/<str:id>/', FinancialUserInformation.as_view(), name='Financial User Information'),
    path('optimizer/', FinancialOptimizer.as_view(), name='Obtain Financial Plan'),
    path('agent/', AgentOptimizer.as_view(), name='Agent Financial Plan'),
]