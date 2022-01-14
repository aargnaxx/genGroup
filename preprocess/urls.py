from django.urls import path

from . import views

app_name = 'preprocess'
urlpatterns = [
    path('', views.Preprocessing.as_view(), name='run_preprocessing'),
]
