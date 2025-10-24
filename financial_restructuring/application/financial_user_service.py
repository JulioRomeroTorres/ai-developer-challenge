from financial_restructuring.models import CustomerCashflow
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from .constants.app_constants import FINANCIAL_USER_INFORMATION_COLUMNS
from .agent.work_flow import agent_graph, State
from .agent.streaming_work_flow import streaming_agent_graph

class FinancialUserService:
    def get_user_information(self, user_id: str) -> CustomerCashflow:
        try:

            customer = CustomerCashflow.objects.prefetch_related(
                'credit_score_history',
                'payment_histories', 
                'loans',
                'cards'
            ).get(customer_id='CU-001')

            customer_loans = list(customer.loans.values(*FINANCIAL_USER_INFORMATION_COLUMNS["LOANS"]))
            customer_cards = list(customer.cards.values(*FINANCIAL_USER_INFORMATION_COLUMNS["CARDS"]))
            customer_payment_histories = list(customer.payment_histories.values(*FINANCIAL_USER_INFORMATION_COLUMNS["PAYMENT_HISTORIES"]))

            return {**model_to_dict(customer), "loans": customer_loans, "cards": customer_cards, "payment_histories": customer_payment_histories   }
        except Exception as error:
            raise error

    def optimize_financial_plan(
            self, 
            monthly_income_avg, income_variability_pct, essential_expenses_avg, loans, cards, payment_histories):
        
        return 0.0, 0.0, 0.0

    def execute_agent(self, question: str):
        print(f"User Question {question}")
        state = {"user_input": question}
        result = agent_graph.invoke(state)
        return {"response": result["llm_output"]}

    def execute_stream_agent(self, question: str):
        print(f"User Question {question}")
        state = {"user_input": question}
        result = streaming_agent_graph.invoke(state)

        for token in result["stream_output"]:
            yield token + "\n"