from django.urls import path

from . import views

app_name = 'clustering'
urlpatterns = [
    path('<int:seq_length>', views.run, name='run'),
]
