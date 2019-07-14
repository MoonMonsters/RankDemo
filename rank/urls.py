from django.urls import path, re_path

from rank import views

urlpatterns = [
    path('rank/', views.RankView.as_view()),
    path('search/', views.SearchView.as_view())
]
