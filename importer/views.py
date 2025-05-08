
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .utils import import_excel_file
from .models import ImportLog, ImportSummary, Product
from rest_framework import status
from .serializers import ImportLogSerializer,ProductSerializer
from django.db import transaction
from rest_framework import generics, filters


# # Create your views here

class ImportExcelView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file was uploaded."}, status=400)

        os.makedirs('media', exist_ok=True)
        file_path = os.path.join('media', file.name)

        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        try:
            summary = import_excel_file(file_path)
        except Exception as e:
            return Response({
                "error": "Failed to import data",
                "details": str(e)
            }, status=400)

        return Response({"message": "Import completed", "summary_id": summary.id})

    
class ImportSummaryView(APIView):
    def get(self, request):
        latest_summary = ImportSummary.objects.latest('created_at') 
        return Response({
            'file_name': latest_summary.file_name,
            'total': latest_summary.total,
            'success': latest_summary.success,
            'warnings': latest_summary.warnings,
            'errors': latest_summary.errors,
            'duration': str(latest_summary.duration)
        })
    

class ImportLogListView(generics.ListAPIView):
    serializer_class = ImportLogSerializer
    queryset = ImportLog.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter] 
    search_fields = ['message'] 
    ordering_fields = ['row_number', 'status']

    def get_queryset(self):
        queryset = super().get_queryset()
        summary_id = self.request.query_params.get('summary')
        status = self.request.query_params.get('status')

        if summary_id:
            queryset = queryset.filter(summary_id=summary_id)
        if status:
            queryset = queryset.filter(status=status)
        return queryset
    

class ProductListView(APIView):
    
    def get(self, request):
        products = Product.objects.all()
        print("Products:", products)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    