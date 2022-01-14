from django.urls import path

from . import views

app_name = 'preprocess'
urlpatterns = [
    path('', views.select_file, name='select_file'),
    path('results', views.preprocess_results, name='preprocess_results'),
]
