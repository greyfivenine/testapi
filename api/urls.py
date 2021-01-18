from django.urls import path

from .views import CustomerInfoView, FileUploadView

urlpatterns = [
    path('check/', CustomerInfoView.as_view()),
    path('upload/', FileUploadView.as_view()),
]
