from django.urls import path

from . import views

app_name = 'clustering'
urlpatterns = [
    path('<int:seq_length>/<int:decrement_range>/<int:increment_range>', views.run, name='run'),
]
