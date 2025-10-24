from rest_framework import serializers

class FinancialOptimizerSerializer(serializers.Serializer):
    customer_id = serializers.CharField(
        min_length=4,
        allow_blank=False
    )
    monthly_income_avg = serializers.FloatField(
        
    )
    
    income_variability_pct = serializers.FloatField(
        
    )

    essential_expenses_avg = serializers.FloatField(
        
    )

    loans = serializers.ListField(
        child=serializers.DictField(required=False, default=None)
    )
    
    cards = serializers.ListField(
        child=serializers.DictField(required=False, default=None)
    )

    payment_histories = serializers.ListField(
        child=serializers.DictField(required=False, default=None)
    )

class AgentOptimizerSerializer(serializers.Serializer):
    question = serializers.CharField(
        min_length=4,
        allow_blank=False
    )