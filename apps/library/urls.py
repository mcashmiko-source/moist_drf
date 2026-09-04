from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('import-csv/', views.import_csv, name='import_csv'),
    # path('download-sample-csv/', views, name='download_sample_csv'),
    # ... other URLs
]