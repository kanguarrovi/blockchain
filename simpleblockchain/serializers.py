from rest_framework import serializers

class TransactionSerializer(serializers.Serializer):
    sender = serializers.CharField(required=True, allow_blank=False)
    recipient = serializers.CharField(required=True, allow_blank=False)
    amount = serializers.IntegerField(required=True)
    
    class Meta:
        fields = ('sender','recipient','amount')

class NodesSerializer(serializers.Serializer):
    node = serializers.CharField(required=True, allow_blank=False)
    
    class Meta:
        fields = ('node',)