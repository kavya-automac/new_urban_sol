from django.db import models
from datetime import time, date


# Create your models here.



class Process_Details(models.Model):
    objects = models.Manager()
    # process_id = models.ForeignKey(process_update,on_delete=models.CASCADE)
    description=models.TextField()
    image=models.ImageField(upload_to='images',blank=True)
    process_type=models.CharField(max_length=200)
    process_name=models.CharField(max_length=200)

    def __str__(self):
        return "%s %s"%(self.process_name,self.process_type)


class  Product_Model(models.Model):
    objects = models.Manager()
    model_name=models.CharField(max_length=200)
    process_id=models.ManyToManyField(Process_Details)


    def __str__(self):
        return self.model_name



class Manufacture(models.Model):
    objects = models.Manager()
    model_id=models.ForeignKey(Product_Model,on_delete=models.CASCADE)
    manufacture_No=models.CharField(max_length=200)

    def __str__(self):
        return "%s %s" % (self.model_id.model_name, self.manufacture_No)





class process_update(models.Model):
    objects = models.Manager()
    manufacture_id=models.ForeignKey(Manufacture,on_delete=models.CASCADE)
    process_id=models.ForeignKey(Process_Details,on_delete=models.CASCADE)
    start_date=models.DateField(default=date.today)
    end_date=models.DateField(default=date.today)
    time=models.TimeField(default=time(0,0,0))
    issues=models.TextField(null=True,blank=True)
    status_choices=(("Completed","Completed"),("On Going","On Going"),("Not Started","Not Started"),("Issue Raised","Issue Raised"))
    status=models.CharField(max_length=200,choices=status_choices,default="Not Started")

    def __str__(self):
        return "%s %s"%(self.process_id.process_name,self.manufacture_id)






