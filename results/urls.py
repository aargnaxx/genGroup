from django.urls import path

from . import views

app_name = 'results'
urlpatterns = [
    path('', views.show_results, name='show_results'),
]
