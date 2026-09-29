from django.urls import path

from . import views

app_name = "advertisements"

urlpatterns = [
    path("", views.AdvertisementListView.as_view(), name="list"),
    path("new/", views.AdvertisementCreateView.as_view(), name="create"),
    path("statistic/", views.AdvertisementStatisticView.as_view(), name="statistic"),
    path("<int:pk>/", views.AdvertisementDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.AdvertisementUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.AdvertisementDeleteView.as_view(), name="delete"),
]
