from django.urls import path

from . import views

app_name = 'clustering'
urlpatterns = [
    path('', views.ClusteringList.as_view(), name='clustering_list'),
    path('<int:pk>', views.ClusteringView.as_view(), name='clustering_view'),
    path('status', views.ClusteringStatus.as_view(), name='clustering_status'),
    path('download/<int:pk>', views.ClusteringDownload.as_view(), name='download'),
]
