from django.urls import path

from . import views

urlpatterns = [
	path('', views.EventsAPIView.as_view()),
]