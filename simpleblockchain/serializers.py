from rest_framework import serializers

class TransactionSerializer(serializers.Serializer):
    sender = serializers.CharField(required=True, allow_blank=False)
    recipient = serializers.CharField(required=True, allow_blank=False)
    amount = serializers.IntegerField(required=True)
    
    class Meta:
        fields = ('sender','recipient','amount')

class NodesSerializer(serializers.Serializer):
    #This Regex must be aproved to accept valid IP address with a valid port. 
    node = serializers.RegexField(regex="^(?:[0-2]?[0-9]?[0-9]\.){3}(?:[0-2]?[0-9]?[0-9])(?:\:\d{1,4})?$", required=True, allow_blank=False)

    class Meta:
        fields = ('node',)