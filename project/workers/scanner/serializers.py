from rest_framework import serializers


class BaseScannerSerializer(serializers.Serializer):
    target = serializers.CharField()


class PortScannerSerializer(BaseScannerSerializer):
    ports = serializers.CharField(required=False, default=None, allow_null=True, allow_blank=True)
    top_ports = serializers.IntegerField(required=False, default=10, allow_null=True)


class NseScannerSerializer(BaseScannerSerializer):
    script = serializers.CharField(required=False, default="*vuln*")




