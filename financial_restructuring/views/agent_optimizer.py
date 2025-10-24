from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from financial_restructuring.serializer import AgentOptimizerSerializer
from financial_restructuring.application.financial_user_service import FinancialUserService

@method_decorator(csrf_exempt, name='dispatch')
class AgentOptimizer(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    def post(self, request):
        serializer = AgentOptimizerSerializer(data=request.data)

        if serializer.is_valid():
            question = serializer.validated_data.get('question')

            try:    
                response = FinancialUserService().execute_agent(question)
                return Response(
                    response,
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                return Response(
                    {"error": "Failed to publish message", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
