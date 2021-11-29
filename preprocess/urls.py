from django.urls import path

from . import views

app_name = 'preprocess'
urlpatterns = [
    path('', views.list_files, name='list'),
    path('results', views.preprocess_results, name='preprocess_results')
]
