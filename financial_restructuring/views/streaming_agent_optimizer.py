from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from financial_restructuring.serializer import AgentOptimizerSerializer
from financial_restructuring.application.financial_user_service import FinancialUserService
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class AgentStreamingOptimizer(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    def post(self, request):
        serializer = AgentOptimizerSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        question = serializer.validated_data["question"]

        def stream():
            try:
                for chunk in FinancialUserService().execute_stream_agent(question):
                    yield chunk
            except Exception as e:
                yield f"[Error]: {str(e)}"

        return StreamingHttpResponse(stream(), content_type="text/event-stream")
