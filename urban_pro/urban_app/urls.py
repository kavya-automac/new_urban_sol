from django.urls import path
from. import views

urlpatterns = [
    path('manufacture/',views.list_manufactures),
    path('processes/',views.list_of_processes),
    path('about_process/',views.about_process)
]
