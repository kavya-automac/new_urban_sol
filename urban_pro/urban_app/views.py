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
                            "timer": process_data["timer"],
                            'issue_raised':process_data["issues"]
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
                            "time": process_data["timer"]
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




@api_view(['PUT'])
def start_stop_process(request):


    if request.method=="PUT" :
        # return JsonResponse({"status": "stop scenario yes"})
        f_manufacture_id = request.data.get('m_id')
        f_process_id = request.data.get('p_id')
        f_process_status = request.data.get('status')
        f_end_date = request.data.get('end_date')
        f_start_date = request.data.get('start_date')
        f_issue= request.data.get('issues')
        f_time= request.data.get('timer')
        f_start_time=request.data.get('start_time')

        r = request.data
        print('rrrrrrrrrrr', len(r), r)
        try:
            update_table_query = process_update.objects.get(manufacture_id=f_manufacture_id,process_id=f_process_id)
        except process_update.DoesNotExist:
            update_table_query = None
            print('no data in db')

        # print(update_table_query)
        frontend_stop_data = {"manufacture_id": request.data.get('m_id'),
                               "process_id": request.data.get('p_id'),"start_date": request.data.get('start_date'),
                               "end_date": request.data.get('end_date'),"timer":request.data.get('timer'),"start_time":request.data.get('start_time'),"issues":request.data.get('issues'), "status": request.data.get('status')}

        serializer_data = stop_processSerializer(data=frontend_stop_data)
        # f_serializer_data = start_processSerializer(d)
        # print('sdata', serializer_data)
        if serializer_data.is_valid():
            print('validated_dataaaaaaaaaa',serializer_data.validated_data)

            if update_table_query is None:
                manufacture_instance = Manufacture.objects.get(id=f_manufacture_id)
                process_instance = Process_Details.objects.get(id=f_process_id)
                print('/////', manufacture_instance, process_instance)
                start_new_record = process_update(manufacture_id=manufacture_instance, process_id=process_instance,
                                                  start_date=f_start_date, end_date="1111-11-11", timer=time(0, 0, 0),
                                                  start_time=f_start_time,issues="", status=f_process_status)
                start_new_record.save()

                print("00000000")

                return JsonResponse({"status": "record_created"})

            elif update_table_query is not None:

                # print(serializer_data,serializer_data.data)
                print('validated', serializer_data.validated_data)
                print(serializer_data.validated_data['manufacture_id'])
                print(serializer_data.validated_data['process_id'])
                print(serializer_data.validated_data['status'])
                print(serializer_data.validated_data['end_date'])
                print(serializer_data.validated_data['issues'])
                print(serializer_data.validated_data['timer'])
                update_table_query.manufacture_id = serializer_data.validated_data['manufacture_id']
                update_table_query.process_id = serializer_data.validated_data['process_id']
                update_table_query.status = serializer_data.validated_data['status']
                update_table_query.end_date = serializer_data.validated_data['end_date']
                update_table_query.issues = serializer_data.validated_data['issues']
                update_table_query.time = serializer_data.validated_data['timer']
                update_table_query.start_time = serializer_data.validated_data['start_time']
                update_table_query.save()

                return JsonResponse({"status": "data_updated"})

            else:
                print("else")
                pass
        else:
            print(serializer_data.errors)

            return JsonResponse({"status": "invalid_manufacture_id_or_process_id"})


    else:
        return JsonResponse({"status":"not_stop_not_start_might_be_some_other_scenario"})








@api_view(['GET'])
def about_process(request):
    if "p_id" in request.GET and "module" in request.GET and "m_id" in request.GET:
        module = request.GET["module"]
        process_id = request.query_params.get('p_id')
        manufacture_id = request.query_params.get('m_id')

        process_data=Process_Details.objects.get(pk=process_id)
        process_data_serilaizer=all_Process_DetailsSerializer(process_data)
        process_data_serilaizer_data=process_data_serilaizer.data
        print('process_data_serilaizer_data',process_data_serilaizer_data)
        try:
            updated_data=process_update.objects.get(manufacture_id=manufacture_id,process_id=process_id)
            print('updated_data',updated_data)
        except :
            updated_data= None

        # print('start_date',updated_data.start_date)
        # print('end_date',updated_data.end_date)
        # print('status',updated_data.status)

        if module == "Details":
            result_data_1 = {}
            result_data_1["process_name"] = process_data_serilaizer_data['process_name']
            result_data_1["Status"] = updated_data.status if updated_data else " "
            result_data_1["start_date"] = updated_data.start_date if updated_data else " "
            result_data_1["end_date"] = updated_data.end_date if updated_data else " "
            result_data_1["Type"] = process_data_serilaizer_data['process_type']
            result_data_1["issues"] = updated_data.issues if updated_data else " "

            data= {'data': result_data_1}

        if module == "Image":
            result_data_2 = {}
            result_data_2["process_name"] = process_data_serilaizer_data['process_name']
            result_data_2["Image"] = process_data_serilaizer_data['image'] if process_data_serilaizer_data['image'] else ""


            data= {'data': result_data_2}
        if module == "Description":
            result_data_3={}
            result_data_3["process_name"]=process_data_serilaizer_data['process_name']
            result_data_3["description"]=process_data_serilaizer_data['description']

            data= {'data': result_data_3}
        if module =="Live":
            status =updated_data.status if updated_data else ""
            d_start_time =updated_data.start_time if updated_data else ""
            d_start_date =updated_data.start_date if updated_data else ""
            print('status',status)
            issue=updated_data.issues if updated_data else ""
            if status == "On Going":
                result ="Stop"
            elif  status == "Completed" or issue :
                result = "restart"
            else:
                result="Start"
            data={"status":result,"start_time":d_start_time,"start_date":d_start_date}

    return JsonResponse(data)