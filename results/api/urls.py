from django.urls import path

from .views import ResultListView

urlpatterns = [
    path('<tagName>', ResultListView.as_view()),
]