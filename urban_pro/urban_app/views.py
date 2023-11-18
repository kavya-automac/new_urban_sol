from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from . models import *
from .serializers import *
@api_view(["GET"])
def list_manufactures(request):
    manufacture_query=Manufacture.objects.all()
    manufature_serializer = manufactureSerializer(manufacture_query,many=True)
    manufature_serializer_data =manufature_serializer.data
    print('manufature_serializer_data',manufature_serializer_data)
    result_data=[]
    for data in manufature_serializer_data:
        print('data',data['manufacture_No'])
        result_data.append(data['manufacture_No'])
    return JsonResponse({"manufacture_data":result_data})


@api_view(["GET"])
def list_of_processes(request):
    get_manufacture_id = request.query_params.get('manufacture_id')
    get_model=Manufacture.objects.filter(manufacture_No=get_manufacture_id).values("id","model_id__model_name")

    print("get_model",get_model)
    # for modeldata in get_model:
    #     print('modeldata',modeldata['model_id__model_name'])
    #     no_processes=Product_Model.objects.filter(model_name=modeldata['model_id__model_name']).values("process_id__process_name")
    #     print('no_processes',no_processes)

    entire_data= process_update.objects.filter(manufacture_id__manufacture_No = get_manufacture_id).order_by("-id")
    entire_data_serializer = process_updateSerializer(entire_data, many=True)
    entire_data_serializer_data= entire_data_serializer.data

    # only_process= process_update.objects.filter(manufacture_id__manufacture_No = get_manufacture_id).order_by("-id")
    # only_process_serializer=only_processSerializer(only_process,many=True)
    # only_process_serializer_data=only_process_serializer.data
    # print("only_process_serializer_data",only_process_serializer_data)
    print('entire_data_serializer_data',entire_data_serializer_data)
    result = []

    for modeldata in get_model:
        print('modeldata',modeldata['model_id__model_name'])
        print('get_model',get_model)

        no_processes=Product_Model.objects.filter(model_name=modeldata['model_id__model_name']).values("id","process_id__process_name")
        # no_processes_serializer=only_processSerializer(no_processes,many=True)
        # no_processes_serializer_data=no_processes_serializer.data
        print('no_processes',no_processes)
        list_no_processes=list(no_processes)


        for process in list_no_processes :
            print('process',process)


            name=process['process_id__process_name']
            p_id = process["id"]
            process_id = Process_Details.objects.filter(process_name=name).values('id')
            print('process_id',list(process_id))
            p_list=list(process_id)

            # global process_data
            for process_data in entire_data_serializer_data:

                print('proces',process['process_id__process_name'])
                if process['process_id__process_name'] == process_data['process_name']:
                    if process_data["status"] == "Completed":
                        result_data_1 = {
                            "m_id": process_data["manufacture_id"],
                            "p_id": process_data["process_id"],
                            "process_status": process_data["status"],
                            "process_name": process_data["process_name"],
                            "start_date": process_data["start_date"],
                            "completed_date": process_data["end_date"],
                            "time": process_data["time"]
                        }
                        result.append(result_data_1)
                        break
                    if process_data["status"] == "On Going":
                        result_data_2 = {
                            "m_id":process_data["manufacture_id"],
                            "p_id" :process_data["process_id"],
                            "process_status": process_data["status"],
                            "process_name": process_data["process_name"],
                            "start_date": process_data["start_date"],
                            "time": process_data["time"]
                        }
                        result.append(result_data_2)
                        break
                    if process_data["status"] == "Issue Raised":
                        result_data_3 = {
                            "m_id": process_data["manufacture_id"],
                            "p_id": process_data["process_id"],
                            "process_status": process_data["status"],
                            "process_name": process_data["process_name"],
                            "Issue": process_data["Issue Raised"],

                        }
                        result.append(result_data_3)
                        break
            else:
                for data in p_list:
                    print('data',data)


                    result_data_4 = {
                        "m_id": modeldata["id"],
                        "p_id": data['id'],
                        "process_status": "Not Started",
                        "process_name": process['process_id__process_name'],
                        # "Issue": process_data["Issue Raised"],

                    }
                result.append(result_data_4)
                print('resultttt', result)


        return JsonResponse({"data":result})













@api_view(['GET'])
def about_process(request):
    if "process_id" in request.GET and "module" in request.GET:
        module = request.GET["module"]
        process_id = request.query_params.get('process_id')
        process_data=Process_Details.objects.get(process_name=process_id)
        process_data_serilaizer=all_Process_DetailsSerializer(process_data)
        process_data_serilaizer_data=process_data_serilaizer.data
        print('process_data_serilaizer_data',process_data_serilaizer_data)

        updated_data=process_update.objects.get(process_id__process_name=process_id)
        print('start_date',updated_data.start_date)
        print('end_date',updated_data.end_date)
        print('status',updated_data.status)

        if module == "Details":
            result_data_1 = {}
            result_data_1["process_name"] = process_data_serilaizer_data['process_name']
            result_data_1["Status"] = updated_data.status
            result_data_1["start_date"] = updated_data.start_date
            result_data_1["end_date"] = updated_data.end_date
            result_data_1["Type"] = process_data_serilaizer_data['process_type']
            result_data_1["issues"] = updated_data.issues

            data= {'data': result_data_1}

        if module == "Image":
            result_data_2 = {}
            result_data_2["process_name"] = process_data_serilaizer_data['process_name']
            result_data_2["Image"] = process_data_serilaizer_data['image']


            data= {'data': result_data_2}
        if module == "Description":
            result_data_3={}
            result_data_3["process_name"]=process_data_serilaizer_data['process_name']
            result_data_3["description"]=process_data_serilaizer_data['description']

            data= {'data': result_data_3}

    return JsonResponse(data)