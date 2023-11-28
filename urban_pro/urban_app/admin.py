from django.contrib import admin
from  .models import *
# Register your models here.

admin.site.register([process_update,Process_Details,Product_Model,Manufacture,Issues])


@admin.register(Issues_details)
class Issues_detailsAdmin(admin.ModelAdmin):
    list_display = ['issues_id','manufacture_id','process_id','issue_raised_by']



#
# @admin.register(process_update)
# class process_update_ListAdmin(admin.ModelAdmin):
#     # list_display = ['id','kpi_name','kpi_data','kpi_unit']
#     list_display = ['id','manufacture_id','process_id','start_date','end_date','time','issues','status']
#
# @admin.register(Process_Details)
# class Process_Details_ListAdmin(admin.ModelAdmin):
#     list_display = ['id','process_name','description','image','process_type']
#
# @admin.register(Product_Model)
# class Product_Model_ListAdmin(admin.ModelAdmin):
#     list_display = ['id','model_name','process_id']
#
#
# @admin.register(Manufacture)
# class Manufacturemodel_id_ListAdmin(admin.ModelAdmin):
#     list_display = ['id','model_id','manufacture_No']

