from rest_framework import serializers


class ResponseSerializer(serializers.Serializer):
    status = serializers.IntegerField(min_value=100, max_value=599, required=True)
    message = serializers.CharField(max_length=1000)
    code = serializers.IntegerField(min_value=1000, max_value=9999)
    result = serializers.DictField(allow_null=True, allow_empty=True)
