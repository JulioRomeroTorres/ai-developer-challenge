from django.urls import path
from .views.financial_optimizer import FinancialOptimizer
from .views.financial_user_information import FinancialUserInformation
from .views.agent_optimizer import AgentOptimizer
from .views.streaming_agent_optimizer import AgentStreamingOptimizer
from .views.users_information import UsersInformation

urlpatterns = [
    path('user/<str:id>/', FinancialUserInformation.as_view(), name='Financial User Information'),
    path('users/', UsersInformation.as_view(), name='Financial User Information'),
    path('optimizer/', FinancialOptimizer.as_view(), name='Obtain Financial Plan'),
    path('agent/', AgentOptimizer.as_view(), name='Agent Financial Plan'),
    path('streaming/agent/', AgentStreamingOptimizer.as_view(), name='Agent Streaming Financial Plan'),
]