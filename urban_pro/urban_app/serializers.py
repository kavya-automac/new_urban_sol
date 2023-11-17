from rest_framework import serializers
from . models import *

class manufactureSerializer(serializers.ModelSerializer): #list_manufactures
    class Meta:
        model = Manufacture
        fields =['manufacture_No']





class all_Process_DetailsSerializer(serializers.ModelSerializer):#about_process
    class Meta:
        model = Process_Details
        fields ="__all__"



class process_updateSerializer(serializers.ModelSerializer):
    manufacture_model_name = serializers.CharField(source='manufacture_id.model_id.model_name', read_only=True)

    # Include fields from the related process_id model
    process_name = serializers.CharField(source='process_id.process_name', read_only=True)

    class Meta:
        model = process_update
        # fields ="__all__"
        fields =["manufacture_model_name","process_name","start_date","end_date","time","issues","status"]



class only_processSerializer(serializers.ModelSerializer):

    # Include fields from the related process_id model
    process_name = serializers.CharField(source='process_id.process_name', read_only=True)

    class Meta:
        model = process_update

        fields =["process_name"]