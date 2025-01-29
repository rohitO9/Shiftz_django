from django.urls import path
from .views import generate_job_description  # Import your API function

urlpatterns = [
    path('generate-jd/', generate_job_description),  # ✅ This is your API route
]
