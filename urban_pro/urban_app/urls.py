from django.urls import path
from. import views

urlpatterns = [
    path('manufacture/',views.list_manufactures),
    path('processes/',views.list_of_processes),
    path('about_process/',views.about_process),
    path('start_stop_process/',views.start_stop_process),
]



# any issue raised stop
# {"manufacture_id":1,"process_id":2,"start_date":"2222-12-22","status":"On Going"}

# after completion stop
# {"manufacture_id":1,"process_id":2,"end_date":"1111-11-11","time":"00:00:00","issues":"example issue","status":"Completed"}