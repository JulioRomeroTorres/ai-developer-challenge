from django.shortcuts import render

from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from financial_restructuring.serializer import FinancialOptimizerSerializer
from financial_restructuring.application.financial_user_service import FinancialUserService

@method_decorator(csrf_exempt, name='dispatch')
class FinancialOptimizer(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    def post(self, request):
        serializer = FinancialOptimizerSerializer(data=request.data)

        if serializer.is_valid():
            customer_id = serializer.validated_data.get('customer_id')
            monthly_income_avg = serializer.validated_data.get('monthly_income_avg')
            income_variability_pct = serializer.validated_data.get('income_variability_pct')
            essential_expenses_avg = serializer.validated_data.get('essential_expenses_avg', None)
            loans = serializer.validated_data.get('loans')
            cards = serializer.validated_data.get('cards')
            payment_histories = serializer.validated_data.get('payment_histories')

            try:    
                minimum_payment, optimized_payment, consolidated = FinancialUserService().optimize_financial_plan(
                    monthly_income_avg, income_variability_pct, essential_expenses_avg, loans, cards, payment_histories )

                response_process = {
                    "customer_id": customer_id,
                    "financial_plan": {
                        "minimum": {
                            "value": minimum_payment,
                            "thrift": 0.0
                        },
                        "optimized": {
                            "value": optimized_payment,
                            "thrift": 0.0
                        },
                        "consolidated": {
                            "value": consolidated,
                            "thrift": 0.0
                        }
                    }
                }
                return Response(
                    response_process,
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                return Response(
                    {"error": "Failed to publish message", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
