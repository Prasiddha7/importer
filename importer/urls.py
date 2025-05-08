from django.urls import path
from .views import ImportExcelView, ImportSummaryView, ImportLogListView, ProductListView

urlpatterns = [
    path('upload/', ImportExcelView.as_view()),
    path('summary/<int:summary_id>/', ImportSummaryView.as_view()),
    path('import-logs/', ImportLogListView.as_view(), name='import-logs'),
    path('products/', ProductListView.as_view(), name='product-list'),
]