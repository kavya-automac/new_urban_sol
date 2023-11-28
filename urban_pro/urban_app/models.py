from django.db import models
from datetime import time,date


# Create your models here.



class Process_Details(models.Model):
    objects = models.Manager()
    # process_id = models.ForeignKey(process_update,on_delete=models.CASCADE)
    description=models.TextField()
    image=models.ImageField(upload_to='media',blank=True)
    process_type=models.CharField(max_length=200)
    process_name=models.CharField(max_length=200)

    def __str__(self):
        return "%s %s"%(self.process_name,self.process_type)


class  Product_Model(models.Model):
    objects = models.Manager()
    # model_id=models.AutoField(primary_key=True)
    model_name=models.CharField(max_length=200)
    process_id=models.ManyToManyField(Process_Details)


    def __str__(self):
        return self.model_name



class Manufacture(models.Model):

    objects = models.Manager()
    # m_id = models.AutoField(primary_key=True)
    model_id=models.ForeignKey(Product_Model,on_delete=models.CASCADE)
    manufacture_No=models.CharField(max_length=200)
    order_id=models.IntegerField()

    def __str__(self):
        return "%s %s" % (self.model_id.model_name, self.manufacture_No)





class process_update(models.Model):
    objects = models.Manager()
    manufacture_id=models.ForeignKey(Manufacture,on_delete=models.CASCADE)
    process_id=models.ForeignKey(Process_Details,on_delete=models.CASCADE)
    start_date=models.DateField(default=date.today)
    end_date=models.DateField(default=date.today)
    timer=models.TimeField(default=time(0,0,0))
    start_time=models.TimeField(default=time(0,0,0))
    issues=models.TextField(null=True,blank=True)
    status_choices=(("Completed","Completed"),("On Going","On Going"),("Not Started","Not Started"),("Issue Raised","Issue Raised"))
    status=models.CharField(max_length=200,choices=status_choices,default="Not Started")

    def __str__(self):
        return "%s %s"%(self.process_id.process_name,self.manufacture_id)


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





