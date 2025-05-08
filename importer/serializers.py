from rest_framework import serializers
from .models import ImportSummary, ImportLog, Product

class ImportSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportSummary
        fields = '__all__'

class ImportLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportLog
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'