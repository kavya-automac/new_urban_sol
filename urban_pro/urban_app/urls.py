from django.urls import path
from. import views

urlpatterns = [
    path('manufacture/',views.list_manufactures),
    path('processes/',views.list_of_processes),
    path('about_process/',views.about_process),
    path('start_stop_process/',views.start_stop_process),
    path('reports/',views.reports_data),

    path('pre_defined_issues/',views.pre_defined_issues),
    path('Issues_details_update/',views.Issues_details_update),
    path('Issues_details_create/',views.Issues_details_create),
    path('list_of_groups/',views.list_of_groups),
    path('list_of_group_process/',views.list_of_group_process),
]



# any issue raised stop
# {"manufacture_id":1,"process_id":2,"start_date":"2222-12-22","status":"On Going"}

# after completion stop
# {"manufacture_id":1,"process_id":2,"end_date":"1111-11-11","time":"00:00:00","issues":"example issue","status":"Completed"}