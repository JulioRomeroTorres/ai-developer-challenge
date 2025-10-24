from django.shortcuts import render

from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from financial_restructuring.application.financial_user_service import FinancialUserService

@method_decorator(csrf_exempt, name='dispatch')
class FinancialUserInformation(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    def get(self, request, id):
    
        try:    
            financial_user_service = FinancialUserService()
            response = financial_user_service.get_user_information(id)

            print(f"Financial User information {response}")
            
            return Response(
                response,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"Error Document Processor {e}")
            return Response(
                {"error": "Failed to get financial user information", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
