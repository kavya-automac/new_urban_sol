import datetime

from django.db import models
from datetime import time,date
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.



class Process_Details(models.Model):
    objects = models.Manager()
    description=models.TextField()
    image=models.ImageField(upload_to='media',blank=True)
    process_type=models.CharField(max_length=200)
    process_name=models.CharField(max_length=200)

    def __str__(self):
        return "%s %s"%(self.process_name,self.process_type)


class  Product_Model(models.Model):
    objects = models.Manager()
    model_name=models.CharField(max_length=200)
    wordpress_id=models.IntegerField(default=0)

    process_id=models.ManyToManyField(Process_Details)



    def __str__(self):
        return self.model_name

class Groups(models.Model):
    model_id=models.ForeignKey(Product_Model,on_delete=models.CASCADE)
    group_name=models.CharField(max_length=200)
    # process_id=models.ManyToManyField(Process_Details)
    process_id=models.ManyToManyField(Process_Details)
    Progress=models.IntegerField(default=0)
    start_date=models.DateField(default=date(1111,11,11))
    end_date=models.DateField(default=date(1111,11,11))
    sequence_no = models.PositiveIntegerField()
    group_status=models.CharField(max_length=200,default='Not Started')

    def __str__(self):
        return "%s %s"%(self.model_id,self.group_name)

class grp_process(models.Model):
    group_id=models.ForeignKey(Groups,on_delete=models.CASCADE)
    process_id=models.ManyToManyField(Process_Details)

    def __str__(self):
        return "%s %s" % (self.group_id, self.process_id)


class Manufacture(models.Model):

    objects = models.Manager()
    model_id=models.ForeignKey(Product_Model,on_delete=models.CASCADE)
    manufacture_No=models.CharField(max_length=200)
    order_id=models.IntegerField(default=0)

    def __str__(self):
        return "%s %s" % (self.model_id.model_name, self.manufacture_No)





class process_update(models.Model):
    objects = models.Manager()
    manufacture_id=models.CharField(max_length=500)
    process_id=models.ForeignKey(Process_Details,on_delete=models.CASCADE)
    # group_id=models.
    # process_id=models.ForeignKey(Groups,on_delete=models.CASCADE)
    start_date=models.DateField(default=date.today)
    end_date=models.DateField(default=date.today)
    timer=models.TimeField(default=time(0,0,0))
    start_time=models.TimeField(default=time(0,0,0))
    issues=models.TextField(null=True,blank=True)
    status_choices=(("Completed","Completed"),("On Going","On Going"),("Not Started","Not Started"),("Issue Raised","Issue Raised"))
    status=models.CharField(max_length=200,choices=status_choices,default="Not Started")

    def __str__(self):
        return "%s %s"%(self.process_id,self.manufacture_id)


class Issues(models.Model):
    objects = models.Manager()
    issue_name=models.TextField()

    def __str__(self):
        return self.issue_name


class Issues_details(models.Model):
    issues_id=models.ForeignKey(Issues,on_delete=models.CASCADE)
    manufacture_id = models.ForeignKey(Manufacture, on_delete=models.CASCADE)
    process_id = models.ForeignKey(Process_Details, on_delete=models.CASCADE)
    issue_raised_date=models.DateField(default=date(1111,11,11))
    issue_status=models.CharField(max_length=200,default="")
    issue_raised_by=models.CharField(max_length=200)
    resolved_by = models.CharField(max_length=500,blank=True,null=True)
    resolved_date=models.DateField(default=date(1111,11,11))

    def __str__(self):
        return "%s %s %s %s" %(self.issues_id,self.manufacture_id,self.process_id,self.issues_id.issue_name)



class mysqlview(models.Model):
    order_id = models.IntegerField()
    model_id = models.IntegerField()
    manufacturing_id=models.CharField(max_length=30,primary_key=True)
    # start_date=models.DateField(default=date(1111,11,11))
    # end_date=models.DateField(default=date(1111,11,11))
    # status=models.CharField(max_length=200,default="Not Started")
    # progress=models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'manufacture_list'



class manufacture_list_update(models.Model):
    # order_id = models.IntegerField()
    model_id = models.IntegerField()
    manufacturing_id=models.IntegerField(primary_key=True)
    start_date=models.DateField(default=date(1111,11,11))
    end_date=models.DateField(default=date(1111,11,11))
    status=models.CharField(max_length=200,default="Not Started")
    progress=models.IntegerField(default=1)

    def __str__(self):
        return "%s %s %s" % (self.manufacturing_id,  self.model_id, self.status)

# @receiver(post_save,sender=process_update)
# def signal(sender,instance,created,**kwargs):
#     m_id = instance.manufacture_id
#     p_id = instance.process_id
#     manufactures = mysqlview.objects.all()
#     print('manufactures', manufactures)
#     for record in manufactures:
#         print('record', record.manufacturing_id)
#         print('record', record.model_id)
#         model=Product_Model.objects.filter(wordpress_id=record.model_id).values('process_id')
#         print('............',model)
#         total_count=len(list(model))
#         print('total_count',total_count)

# def func(9456_8918_1,1):











#
# @receiver(post_save,sender=process_update)
# def signal(sender,instance,created,**kwargs):
#     m_id = instance.manufacture_id
#     p_id = instance.process_id
#     status=instance.status
#     print('m_id',"....................", m_id.manufacture_No)
#     print('p_id',"....................", p_id.id)
#
#     if created:
#
#         # views_table_updation=mysqlview.objects.get(pk= m_id.manufacture_No)
#         # print('views_table_updation',views_table_updation)
#         # views_table_updation.start_date=instance.start_date
#         # views_table_updation.status=instance.status
#         #
#         # views_table_updation.save()
#         update_start_date = Groups.objects.get(id=p_id.id)
#         update_start_date.start_date = instance.start_date
#         update_start_date.status=instance.status
#         update_start_date.save()
#     else:
#         update_end_date = Groups.objects.get(id=p_id.id)
#         update_end_date.end_date = instance.end_date
#         update_end_date.status = instance.status
#         update_end_date.save()
#
#
#         # manufactures = mysqlview.objects.all()
#         # print('manufactures', manufactures)
#         # for record in manufactures:
#         #     print('record', record.manufacturing_id)
#         #     # views_table_updation_1 = record.manufacturing_id
#         #     print(record.manufacturing_id ==m_id.manufacture_No)
#         #     if record.manufacturing_id ==m_id.manufacture_No:
#         #         print('views_table_updation elseee',record.manufacturing_id)
#         #         print('mmmmm',instance.end_date)
#         #         print('llllll',record.end_date)
#         #         if instance.end_date is not None and isinstance(instance.end_date, date):
#         #             print('llllll', record.end_date)
#         #             record.end_date = instance.end_date
#         #             record.status = instance.status
#         #             record.save()
#         #
#         #         # record.end_date = instance.end_date
#         #         # record.status = instance.status
#         #         # record.save()
#
#
#     # if created:#already startstop api will update the end date and status
#     #     update_start_date=Groups.objects.get(id=p_id.id)
#     #     print('update_start_date',update_start_date)
#     #     todays_date = date.today()
#     #     date_string = todays_date.strftime('%Y-%m-%d')
#     #     parsed_date = datetime.date.fromisoformat(date_string)
#     #
#     #     update_start_date.start_date=parsed_date
#     #     update_start_date.save()
#     #
#     #     # process_instance = process_update.objects.get(manufacture_id__manufacture_No=m_id,
#     #     #                                               process_id=p_id.id)
#     #
#     #     # Update the start_date field
#     #     instance.start_date = parsed_date
#     #     instance.save()
#     #     print("added in 2 tables")
#     #
#     #
#     #     print("new data arrived")
#     #
#     #
#     #     print('m_id','p_id',".............................",m_id,p_id,status)
#     #
#     # else:
#     #     print('elseeeee')
#     #     if instance.status=="Completed":
#     #         endtodays_date = date.today()
#     #         date_string1 = endtodays_date.strftime('%Y-%m-%d')
#     #         end_parsed_date = datetime.date.fromisoformat(date_string1)
#     #
#     #         instance.end_date=end_parsed_date
#     #         instance.save()
#     #         update_end_date = Groups.objects.get(id=p_id.id)
#     #         update_end_date.end_date = end_parsed_date
#     #         update_end_date.status = "Completed"
#     #
#     #         update_end_date.save()
#     #         print('updates status and end date in process_uodate and group tables')
#     #     else:
#     #         update_end_date = Groups.objects.get(id=p_id.id)
#     #         update_end_date.status = "On Going"
#
#
#
#
#
#

