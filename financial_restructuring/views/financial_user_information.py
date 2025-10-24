from django.shortcuts import render

from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

@method_decorator(csrf_exempt, name='dispatch')
class FinancialUserInformation(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    def get(self, request):
        serializer = ConsolidateInformationSerializer(data=request.data)

        custom_logger = get_logger(ConsolidateInformationView.__name__, LOGGING_TYPE)
        trace_id = custom_logger.generate_trace()

        print(f'trace_id {trace_id}')
        if serializer.is_valid():
            initial_budget = serializer.validated_data['initial_budget']
            descriptor = serializer.validated_data['descriptor']
            metadata = serializer.validated_data['metadata']
            process_id = serializer.validated_data.get('process_id', None)
            enable_summary = serializer.validated_data.get('enable_summary')

            custom_logger.log_text(f"Payload {request.data}")

            try:    
                agent_workflow_service = AgentWorkFlowService(trace_id)
                consolidated_information, cleaned_response = agent_workflow_service.consolidate_information(initial_budget, descriptor, metadata)
                summary_information = agent_workflow_service.summary_information(cleaned_response) if enable_summary else DEFAULT_STRING_VALUE

                response_process = {
                    "entities": consolidated_information,
                    "summary": summary_information,
                    "process_id": process_id,
                    "metadata": metadata
                }
                custom_logger.log_struct(response_process)
                return Response(
                    response_process,
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                custom_logger.log_text(f"Error Document Processor {e}")
                return Response(
                    {"error": "Failed to publish message", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
