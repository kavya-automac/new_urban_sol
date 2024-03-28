from datetime import timedelta
import datetime
from django.conf import settings
from django.db.models import Min, Count
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from . models import *
from .serializers import *
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from openpyxl import Workbook


@api_view(["GET"])
def list_manufactures(request):


    user_role=request.query_params.get('Role')
    if user_role =="Operator":
        result=Operator_response()
    if user_role =="Supervisor":
        result=Supervisor_response()

    return JsonResponse({"manufacture_data":result})




@api_view(["GET"])
def list_of_processes(request):
    get_manufacture_id = request.query_params.get('manufacture_id')
    get_model=mysqlview.objects.filter(manufacturing_id=get_manufacture_id)
    dept = request.query_params.get('department')


    # get_model=[]
    # model_get=mysqlview.objects.all()
    #
    # for rec in model_get:
    #     get_m={}
    #     get_m["model_id"]=rec.model_id
    #     get_m["manufacturing_id"]=rec.manufacturing_id
    #     get_model.append(get_m)
    # print('get_m_res',get_model)
    #
    #

    # print('get_model1',get_model)
    # get_model=Manufacture.objects.filter(manufacture_No=get_manufacture_id).values("id","model_id__model_name","manufacture_No")
    # # get_model=Manufacture.objects.filter(manufacture_No=get_manufacture_id).values("id","model_id__model_name")
    #
    # print("get_model",get_model)

    entire_data= process_update.objects.filter(manufacture_id = get_manufacture_id).order_by("-id")
    entire_data_serializer = process_updateSerializer(entire_data, many=True)
    entire_data_serializer_data= entire_data_serializer.data


    # print('entire_data_serializer_data',entire_data_serializer_data)
    result = []

    for modeldata in get_model:
        # print('modeldata',modeldata.model_id)
        # print('get_model',get_model)
        #changes product_model to Groups table
        # no_processes=Groups.objects.filter(model_id__model_name=modeldata['model_id__model_name']).values("id","process_id__process_name")
        # try:
        #     dept = request.query_params.get('department')
        #
        #     no_processes=Product_Model.objects.filter(wordpress_id=modeldata.model_id,process_id__process_type=dept).\
        #         values("id","process_id__process_name")
        # except:
        #     no_processes = Product_Model.objects.filter(wordpress_id=modeldata.model_id).values("id",
        #                                                                                         "process_id__process_name")
        # try:
        #     if dept:
        #         no_processes = Product_Model.objects.filter(
        #             wordpress_id=modeldata.model_id,
        #             process_id__process_type=dept
        #         ).values("id", "process_id__process_name")
        #     # if dept == "ADMIN":
        #     #     no_processes = Product_Model.objects.filter(
        #     #         wordpress_id=modeldata.model_id
        #     #     ).values("id", "process_id__process_name")
        #
        #     else:
        #         raise ValueError("Department parameter is missing")
        # except ValueError as e:
        #     # Handle the case where the department parameter is missing
        #     no_processes = Product_Model.objects.filter(
        #         wordpress_id=modeldata.model_id
        #     ).values("id", "process_id__process_name")

        try:
            if dept:
                # Filter processes based on department
                no_processes = Product_Model.objects.filter(
                    wordpress_id=modeldata.model_id,
                    process_id__process_type=dept
                ).values("id", "process_id__process_name")
            else:
                # If department is not provided, raise a custom exception
                raise ValueError("Department parameter is missing")

            if dept == "ADMIN":
                # If the department is "ADMIN", execute additional query
                no_processes = Product_Model.objects.filter(
                    wordpress_id=modeldata.model_id
                ).values("id", "process_id__process_name")



        except ValueError as e:
            # Handle the case where the department parameter is missing
            no_processes = Product_Model.objects.filter(
                wordpress_id=modeldata.model_id
            ).values("id", "process_id__process_name")




        # no_processes_serializer=only_processSerializer(no_processes,many=True)
        # no_processes_serializer_data=no_processes_serializer.data
        print('no_processes',len(no_processes))
        list_no_processes=list(no_processes)

        for process in list_no_processes:
            # print('process', process)

            name = process['process_id__process_name']
            p_id = process["id"]
            process_id = Process_Details.objects.filter(process_name=name).values('id')
            # print('process_id', list(process_id))
            p_list = list(process_id)

            # global process_data
            for process_data in entire_data_serializer_data:
                # print('process_data',process_data)

                # print('proces', process['process_id__process_name'])
                if process['process_id__process_name'] == process_data['process_name']:
                    m_no=mysqlview.objects.get(manufacturing_id=get_manufacture_id)
                    # print('m_no',m_no.manufacturing_id)
                    if process_data["status"] == "Completed":
                        result_data_1 = {
                            "m_id": m_no.manufacturing_id,
                            "p_id": process_data["process_id"],
                            "process_status": process_data["status"],
                            "process_name": process_data["process_name"],
                            "start_date": process_data["start_date"],
                            "completed_date": process_data["end_date"],
                            "timer": process_data["timer"],
                            'issue_raised': process_data["issues"]
                        }
                        result.append(result_data_1)
                        break
                    if process_data["status"] == "On Going":
                        result_data_2 = {
                            "m_id": m_no.manufacturing_id,
                            "p_id": process_data["process_id"],
                            "process_status": process_data["status"],
                            "process_name": process_data["process_name"],
                            "start_date": process_data["start_date"],
                            "timer": process_data["timer"]
                        }
                        result.append(result_data_2)
                        break
                    if process_data["status"] == "Issue Raised":
                        result_data_3 = {
                            "m_id":m_no.manufacturing_id,
                            "p_id": process_data["process_id"],
                            "process_status": process_data["status"],
                            "process_name": process_data["process_name"],
                            "Issue": process_data["Issue Raised"],

                        }
                        result.append(result_data_3)
                        break
            else:
                for data in p_list:
                    # print('data', data)

                    result_data_4 = {
                        "m_id": modeldata.manufacturing_id,
                        "p_id": data['id'],
                        "process_status": "Not Started",
                        "process_name": process['process_id__process_name'],
                        # "Issue": process_data["Issue Raised"],

                    }
                result.append(result_data_4)
        print('resultttt', len(result))

        return JsonResponse({"data": result})


def get_process_status(m_id):
    m_model = Manufacture.objects.get(manufacture_No=m_id)
    grp_data = Groups.objects.filter(model_id__wordpress_id=m_model.model_id.wordpress_id)
    # manytimanyfield_test=urban_app_Groups_Process_Details.objects.all()
    # print('manytimanyfield_test',manytimanyfield_test)


    # grp_data = Groups.objects.filter(model_id__model_name=m_model.model_id)
    grp_data_serializer = groupSerializer22(grp_data, many=True)
    grp_data_serializer_data = grp_data_serializer.data

    for data in grp_data_serializer_data:
        try:
            get_proces_count = process_update.objects.filter(manufacture_id=m_id, process_id=data["group_id"])
        except process_update.DoesNotExist:
            get_proces_count = None

        if get_proces_count:
            # If there are multiple records, consider only the first one
            first_record = get_proces_count.first()
            if first_record.status == "Completed":
                data["group_status"] = "Completed"
                data["Progress"] = 100
            else:
                data["group_status"] = "On Going"
                data["Progress"] = 0
        else:
            data["group_status"] = "Not Started"
            data["Progress"] = 0

        # Update the corresponding Groups instance
        group_instance = Groups.objects.get(id=data["group_id"])
        group_instance.group_status = data["group_status"]
        group_instance.Progress = data["Progress"]
        group_instance.save()

    print('Data saved successfully.')




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


        # hours, minutes, seconds = map(int, f_time.split(':'))

        # Create a timedelta object
        # timer = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        # total_seconds = hours * 3600 + minutes * 60 + seconds
        # timer = timedelta(seconds=total_seconds)

        # Create a timedelta object
        # d_timer = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
        # timer = f"{hours}:{minutes}:{seconds}"

        print('timer',f_time)
        print('timer type',type(f_time))

        r = request.data
        print('rrrrrrrrrrr', len(r), r)
        # grp_p=Groups.objects.get(process_id__id=f_process_id)
        # print("grp_p",grp_p)
        try:
            update_table_query = process_update.objects.get(manufacture_id=f_manufacture_id,process_id=f_process_id)#group_id and process_id should be same
        except process_update.DoesNotExist:
            update_table_query = None
            print('no data in db')
        # tt = parse_duration(timer)
        # print('ttttttttt', tt)
        # dd = f"{tt.seconds // 3600:02d}:{tt.seconds % 3600 // 60:02d}:{tt.seconds % 60:02d}"
        # print('dddd', dd)
        # print('dddd type', type(dd))

        # print(update_table_query)
        # frontend_stop_data = {"manufacture_id__manufacture_No": request.data.get('m_id'),
        #                        "process_id": request.data.get('p_id'),"start_date": request.data.get('start_date'),
        #                        "end_date": request.data.get('end_date'),"timer":request.data.get('timer'),"start_time":request.data.get('start_time'),"issues":request.data.get('issues'), "status": request.data.get('status')}
        #
        # serializer_data = stop_processSerializer(data=frontend_stop_data)
        # # f_serializer_data = start_processSerializer(d)
        # # print('sdata', serializer_data)
        # if serializer_data.is_valid():
        #     print('validated_dataaaaaaaaaa',serializer_data.validated_data)

        if update_table_query is None:
            # manufacture_instance = Manufacture.objects.get(manufacture_No=f_manufacture_id)
            process_instance = Process_Details.objects.get(pk=f_process_id)#Process_Details to Groups
            # print('/////', manufacture_instance, process_instance)
            # timer=timedelta(90)


            start_new_record = process_update(manufacture_id=f_manufacture_id, process_id=process_instance,
                                              start_date=f_start_date, end_date="1111-11-11", timer=f_time,
                                              start_time=f_start_time,issues="", status=f_process_status)
            start_new_record.save()

            print("00000000 start_new_record",start_new_record)

            return JsonResponse({"status": "record_created"})

        elif update_table_query is not None:

            # # print(serializer_data,serializer_data.data)
            # print('validated', serializer_data.validated_data)
            # # print(serializer_data.validated_data['manufacture_id'])
            # print(serializer_data.validated_data['process_id'])
            # print(serializer_data.validated_data['status'])
            # print(serializer_data.validated_data['end_date'])
            # print(serializer_data.validated_data['issues'])
            # print(serializer_data.validated_data['timer'])
            update_table_query.manufacture_id = f_manufacture_id
            # print('update_table_query.manufacture_id',update_table_query.manufacture_id)
            update_table_query.process_id__id = f_process_id
            update_table_query.status = f_process_status
            update_table_query.end_date = f_end_date
            update_table_query.issues = f_issue
            update_table_query.timer = f_time
            update_table_query.start_time = f_start_time
            update_table_query.save()

            return JsonResponse({"status": "data_updated"})

        else:
            print("else")
            pass
    else:
        # print(serializer_data.errors)

        return JsonResponse({"status": "invalid_manufacture_id_or_process_id"})


    # else:
    #     return JsonResponse({"status":"not_stop_not_start_might_be_some_other_scenario"})








@api_view(['GET'])
def about_process(request):
    if "p_id" in request.GET and "module" in request.GET and "m_id" in request.GET:
        module = request.GET["module"]
        process_id = request.query_params.get('p_id')
        manufacture_id = request.query_params.get('m_id')

        process_data=Process_Details.objects.get(pk=process_id)
        process_data_serilaizer=all_Process_DetailsSerializer(process_data)
        process_data_serilaizer_data=process_data_serilaizer.data
        # print('process_data_serilaizer_data',process_data_serilaizer_data)
        try:
            updated_data=process_update.objects.get(manufacture_id=manufacture_id,process_id=process_id)
            # print('updated_data',updated_data)
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

        if module == "Live":
            manf_id = mysqlview.objects.get(manufacturing_id=manufacture_id)
            # manf_id = Manufacture.objects.get(manufacture_No=manufacture_id)
            m_id_models = Product_Model.objects.filter(wordpress_id=manf_id.model_id).values("process_id")
            # print('m_id_models',m_id_models)
            min_process_id = min(item['process_id'] for item in m_id_models)
            # print('min_process_id',min_process_id)
            process_update_entry = None
            # print('Data types:', type(process_id), type(min_process_id))

            # print('process_id',process_id)
            process_update_entry = process_update.objects.filter(manufacture_id=manufacture_id,
                                                                 process_id=process_id).first()
            print('process_update_entry 1...',process_update_entry)

            if int(process_id) == min_process_id:
                # If process_id is the minimum process_id
                # print('process=====y', process_update_entry)

                if process_update_entry:
                    # print('process_update_entry',process_update_entry)
                    status = process_update_entry.status
                    print('statussssssssssssssssss',status)
                    if status == "On Going":
                        result = "Stop"
                        lock_status = "unlocked"
                    elif status == "Completed" or process_update_entry.issues:
                        result = "start"
                        lock_status = "unlocked"
                    else:
                        status = "Not Started"
                        result = "Start"
                        lock_status = "unlocked"
                else:
                    status = "Not Started"
                    result = "Start"
                    lock_status = "unlocked"
            else:

                prev_process_update_entry = process_update.objects.filter(manufacture_id=manufacture_id,process_id__lt=process_id).order_by("process_id").first()

                print('prev_process_update_entry 2...',prev_process_update_entry)
                if prev_process_update_entry:
                    prev_status = prev_process_update_entry.status
                    # print('prev_status',prev_status)

                    if prev_status != "Completed":
                        result = "start"
                        lock_status = "unlocked"
                        status="Not Started"
                    else:
                        # result = "start"
                        lock_status = "unlocked"
                        # status = "Not Started"

                        current_process_update_entry= process_update.objects.get(manufacture_id=manufacture_id,process_id=process_id)
                        print('current_process_update_entry 3...',current_process_update_entry)
                        if current_process_update_entry:
                            if current_process_update_entry.status=="On Going":
                                result = "stop"
                                # lock_status = "unlocked"
                                status="On Going"
                            elif current_process_update_entry.status=="Completed":
                                result = "start"
                                # lock_status = "unlocked"
                                status = "Completed"
                            else:
                                result = "start"
                                # lock_status = "unlocked"
                                status = "Not Started"
                        else:
                            result = "start"
                            lock_status = "unlocked"
                            status = "Not Started"

                else:
                    result = "start"
                    lock_status = "unlocked"
                    status = "Not Started"

            data = {
                "status": result,
                "start_time": process_update_entry.start_time if process_update_entry else "",
                "start_date": process_update_entry.start_date if process_update_entry else "",
                "p_status": status,

                "lock_status": lock_status,
            }


    return JsonResponse(data)

# def prev_min_process():
#     Product_Model.objects.get()
#

@api_view(['GET'])
def pre_defined_issues(request):
    issues_query=Issues.objects.all()
    print('issues_query',issues_query)
    issues_query_serializer=predefined_issuesSerializer(issues_query,many=True)
    print(issues_query_serializer.data)

    return JsonResponse({"status":issues_query_serializer.data})

@api_view(['POST'])

def Issues_details_create(request):
    f_m_id = request.data.get('m_id')
    f_p_id = request.data.get('p_id')
    f_issue_id = request.data.get('issue_id')
    f_issue_raised_date=request.data.get('issue_raised_date')
    f_issue_raised_by=request.data.get('issue_raised_by')
    f_resolved_date=request.data.get('resolved_date')
    f_resolved_by=request.data.get('resolved_by')
    if request.method == 'POST':
        # try:
        #     get_issue= Issues_details.objects.get(issues_id=f_issue_id,manufacture_id=f_m_id,process_id=f_p_id)
        # except:
        #     get_issue=None


        # print('get_issue',get_issue)

        frontend_data = {"issues_id": f_issue_id,
                              "manufacture_id":f_m_id ,
                            "process_id":f_p_id ,
                              "issue_raised_date":f_issue_raised_date ,
                            "issue_raised_by":f_issue_raised_by,
                              "resolved_by": f_resolved_by,
        "resolved_date": f_resolved_date,
                             }
        print('frontend_data',frontend_data)

        serializer_data = issues_detail_Serializer(data=frontend_data)

        print('.......',serializer_data.is_valid())

        if serializer_data.is_valid():
            print('validated_dataaaaaaaaaa', serializer_data.validated_data)
            serializer_data.save()
            return JsonResponse({"status": "record_created"})
        else:
            return JsonResponse({"status": serializer_data.errors})




@api_view(['PUT'])

def Issues_details_update(request):
    f_m_id = request.data.get('m_id')
    f_p_id = request.data.get('p_id')
    f_issue_id = request.data.get('issue_id')
    f_ir_id = request.data.get('ir_id')
    # f_issue_raised_date=request.data.get('issue_raised_date')
    # f_issue_raised_by=request.data.get('issue_raised_by')
    f_resolved_date=request.data.get('resolved_date')
    f_resolved_by=request.data.get('resolved_by')
    f_issue_status=request.data.get('issue_status')
    if request.method == 'PUT':

        frontend_data = { "ir_id":f_ir_id,
                          "issues_id": f_issue_id,
                          "manufacture_id":f_m_id ,
                        "process_id":f_p_id ,
                        "resolved_by": f_resolved_by,
                        "resolved_date": f_resolved_date,
                         'issue_status':f_issue_status
                             }
        print('frontend_data',frontend_data)
        issue_detail_id = Issues_details.objects.get(id=f_ir_id)
        serializer_data_2 = issues_detail_Serializer_22(instance=issue_detail_id,data=frontend_data)

        print('.......',serializer_data_2.is_valid())

        if serializer_data_2.is_valid():
            print('validated_dataaaaaaaaaa', serializer_data_2.validated_data)
            serializer_data_2.save()
            return JsonResponse({"status": "record_updated"})
        else:
            return JsonResponse({"status": serializer_data_2.errors})

#supervisor screen here
@api_view(['GET'])
def list_of_groups(request):
    data=[{
            "m_id":1,
            "group_id": 2,
            "model_id": 8918,

            "group_name": "group_2",
            "Progress": 0,
            "start_date": "1111-11-11",
            "end_date": "2023-11-11",
            "group_status": "On Going"
        },
        {
            "m_id": 1,
            "group_id": 1,
            "model_id": 8918,
            "group_name": "group1",
            "Progress": 0,
            "start_date": "2023-12-06",
            "end_date": "2023-11-11",
            "group_status": "On Going"
        }
    ]


    f_m_id =request.query_params.get('m_id')
    test=get_process_status(f_m_id)
    print('test',test)
    getting_model = Manufacture.objects.get(manufacture_No=f_m_id)


    print('getting_model',getting_model)
    group_lst=Groups.objects.filter(model_id__wordpress_id=getting_model.model_id.wordpress_id).order_by('-sequence_no')
    # group_lst=Groups.objects.filter(model_id=getting_model.model_id).order_by('-sequence_no')
    print('group_lst',group_lst)
    group_lst_serializer=groupSerializer(group_lst,many=True)
    group_lst_serializer_data=group_lst_serializer.data
    print('group_lst_serializer_data',group_lst_serializer_data)
    return JsonResponse({"result":group_lst_serializer_data})

@api_view(['GET'])
def list_of_group_process(request):
    f_model_id = request.query_params.get('model_id')
    f_group_id = request.query_params.get('group_id')
    f_m_id = request.query_params.get('m_id')
    grp_status=interlocked(f_m_id,f_group_id,f_model_id)
    if grp_status=="process_locked":
        return JsonResponse({"data":"process_locked"})
    else:

    # print('testtttttt', grp_status)

        m_id=Manufacture.objects.get(manufacture_No=f_m_id,model_id__wordpress_id=f_model_id)
        print('mid',m_id.pk)
        group_lst=Groups.objects.filter(id=f_group_id,model_id__wordpress_id=f_model_id)
        print('group_lst',group_lst)
        group_lst_serilizer=group_process_Serializer(group_lst,many=True)
        group_lst_serilizer_data=group_lst_serilizer.data
        print('group_lst_serilizer_data',group_lst_serilizer_data)# [OrderedDict([('process_id', [1, 2])])]
        result = []
        for p_d in group_lst_serilizer_data:
            print('p_d',p_d['process_id'])# [1, 2]
            for p_d_details in p_d['process_id']:#[1,2]
                print('p_d_details', p_d_details)#1

                p_details=process_update.objects.filter(process_id=p_d_details)
                entire_data_serializer = process_updateSerializer(p_details, many=True)
                entire_data_serializer_data = entire_data_serializer.data

                print('entire_data_serializer_data',entire_data_serializer_data)
                print('get_model', p_d['process_id'])

                no_processes = Process_Details.objects.filter(pk=p_d_details).values("id", "process_name")
                # no_processes_serializer=only_processSerializer(no_processes,many=True)
                # no_processes_serializer_data=no_processes_serializer.data
                print('no_processes', no_processes)#<QuerySet [{'id': 1, 'process_name': 'process_1'}]>
                list_no_processes = list(no_processes)
                for process in list_no_processes:
                    print('process', process)#{'id': 1, 'process_name': 'process_1'}


                    name = process['process_name']
                    p_id = process["id"]
                    process_id = Process_Details.objects.filter(process_name=name).values('id')
                    print('process_id', list(process_id))
                    p_list = list(process_id)

                    for process_data in entire_data_serializer_data:
                        process_id_in_grp = dict(process_data)['process_id']  # grp_id
                        print('process_id_in_grp', process_id_in_grp)
                        grp_d = Groups.objects.filter(id=process_id_in_grp).values("process_id__process_name")[0]
                        print('grp_d', grp_d['process_id__process_name'])

                        # print('proces', process['process_id__process_name'])
                        if process['process_name'] == grp_d['process_id__process_name']:
                            if process_data["status"] == "Completed":
                                result_data_1 = {
                                    "m_id": process_data["manufacture_id"],
                                    "p_id": process_data["process_id"],
                                    "process_status": process_data["status"],
                                    "process_name": grp_d['process_id__process_name'],
                                    "start_date": process_data["start_date"],
                                    "completed_date": process_data["end_date"],
                                    "timer": process_data["timer"],
                                    'issue_raised': process_data["issues"]
                                }
                                result.append(result_data_1)
                                break
                            if process_data["status"] == "On Going":
                                result_data_2 = {
                                    "m_id": process_data["manufacture_id"],
                                    "p_id": process_data["process_id"],
                                    "process_status": process_data["status"],
                                    "process_name": grp_d['process_id__process_name'],
                                    "start_date": process_data["start_date"],
                                    "timer": process_data["timer"]
                                }
                                result.append(result_data_2)
                                break
                            if process_data["status"] == "Issue Raised":
                                result_data_3 = {
                                    "m_id": process_data["manufacture_id"],
                                    "p_id": process_data["process_id"],
                                    "process_status": process_data["status"],
                                    "process_name": grp_d['process_id__process_name'],
                                    "Issue": process_data["Issue Raised"],

                                }
                                result.append(result_data_3)
                                break
                    else:
                        for data in p_list:
                            print('data', data)

                            result_data_4 = {
                                "m_id": m_id.pk,
                                "p_id": data['id'],
                                "process_status": "Not Started",
                                "process_name": process['process_name'],
                                # "Issue": process_data["Issue Raised"],

                            }
                        result.append(result_data_4)
                        print('resultttt', result)

            return JsonResponse({"data": result})


# def interlocked(f_m_id,f_group_id,f_model_id):







    # m_id_model = Manufacture.objects.get(manufacture_No=f_m_id)
    # print('m_id_model', m_id_model.model_id.id)
    #
    # group_data = Groups.objects.filter(id=f_group_id, model_id=f_model_id).values('process_id', 'sequence_no')
    # print('group_data', group_data)
    #
    # interlock_status = "unlocked"  # Default status
    #
    # max_sequence_no = max(item['sequence_no'] for item in group_data)
    #
    # for ps_ids_data in group_data:
    #     p_details = process_update.objects.filter(process_id=ps_ids_data['process_id'])
    #
    #     if not p_details.exists() or not p_details.filter(status='completed').exists():
    #         interlock_status = "locked"
    #
    # # Check if the current sequence_no is the maximum among all sequence numbers in the group
    # if ps_ids_data['sequence_no'] == max_sequence_no:
    #     # Check if all processes in the group have 'completed' status
    #     if not process_update.objects.filter(process_id__in=[item['process_id'] for item in group_data],
    #                                          status='completed').exists():
    #         interlock_status = "locked"
    #     else:
    #         interlock_status = "unlocked"
    #
    # return interlock_status

#
#
#
def interlocked(m_id,f_group_id,f_model_id):
    mid=m_id
    g_id=f_group_id
    model_id=f_model_id

    sequence_queryset=Groups.objects.filter(pk=f_group_id).values('sequence_no','group_status')
    print('sequence_queryset',sequence_queryset)


    min_seq_id=Groups.objects.filter(model_id__wordpress_id=f_model_id).aggregate(Min('sequence_no'))['sequence_no__min']
    print('min_seq_id',min_seq_id)



    for sequence in sequence_queryset:
        if sequence['sequence_no'] == min_seq_id:
            return "process_unlocked"
        else:
            prev_seq=(sequence['sequence_no'])-1
            grp_no=(sequence['sequence_no'])-1
            print('prev_seq',prev_seq)
            prev_seq_status=Groups.objects.get(model_id__wordpress_id=f_model_id,sequence_no=prev_seq)
            print('prev_seq_status',prev_seq_status.group_status)


            if prev_seq_status.group_status != "Completed":
                print('...........................',prev_seq_status.group_status != "Completed")
                return "process_locked"


            else:

                return "process_unlocked"


    # return JsonResponse({"status":"hhh"})
#
# def supervisor_manufacture_data(user_role):
#     # result = [{
#     #     "m_id": "9456_8918_1",
#     #     "model_id": "8918",
#     #     "start_date":"2023-12-06",
#     #     "end_date":"1111-11-11",
#     #     "status":"On Going",
#     #     "progress":"20",
#     # },{
#     #     "m_id": "9456_8918_2",
#     #     "model_id": "8918",
#     #     "start_date":"1111-11-11",
#     #     "end_date":"1111-11-11",
#     #     "status":"Not Started",
#     #     "progress":"0",
#     # },{
#     #     "m_id": "9456_8918_3",
#     #     "model_id": "8918",
#     #     "start_date":"2023-12-06",
#     #     "end_date":"2023-12-07",
#     #     "status":"Completed",
#     #     "progress":"100",
#     # }]
#
#
#
#
#     manufactures=mysqlview.objects.all()
#     print('manufactures',manufactures)
#     data=[]
#     # for record in manufactures:
#     #     print('record',record)
#     if user_role=="Operator":
#         result = {
#             "m_id": record.manufacturing_id,
#             "model_id": record.model_id
#         }
#
#     if user_role=="Supervisor":
#         result=status()
#         # result={
#         # "m_id":record.manufacturing_id,
#         # "model_id":record.model_id,
#         # "start_date":"",
#         # "end_date":"",
#         # "status":"",
#         # "progress":"",
#         # }
#         # st_date = process_update.objects.
#     # data.append(result)
#     return result


# def manufacture_progress(model_id):
#     model=Product_Model.objects.get(wordpress_id=model_id)
#
#
#     return data


def Operator_response():
    manufactures = mysqlview.objects.all()
    print('manufactures', manufactures)
    data = []
    for record in manufactures:
        print('record',record)
        result = {
            "m_id": record.manufacturing_id,
            "model_id": str(record.model_id)
        }
        data.append(result)
    return data


def Supervisor_response():

    data = mysqlview.objects.all()
    print('data',data)

    # Create a dictionary to group entries by model_id
    # model_data = defaultdict(list)

    result_data = []

    for i in data:
        result = {
            "m_id": i.manufacturing_id,
            # Adjust some_unique_field to the appropriate field
            # "model_id": str(i.model_id),
            # "model_id": "",
            # "start_date": "",
            # "end_date": "",
            # "status": "",
            # "progress": ""
        }

        model_details = Product_Model.objects.filter(wordpress_id=i.model_id).values('process_id','model_name')
        model_details1 = Product_Model.objects.get(wordpress_id=i.model_id)
        # model_details1 = Product_Model.objects.get(wordpress_id=i.model_id)
        # print('model_details111',model_details1)
        result['model_id']=model_details1.model_name

        # print('model_details',model_details)
        # print('manufacturing_id',i.manufacturing_id)
        # print('model_details........',model_details1)
        # print('model_details........',model_details1.process_id)
        process_ids = [item['process_id'] for item in model_details]
        if process_ids:
            min_process_id = min(process_ids)
            max_process_id = max(process_ids)
            total_count=len(process_ids)
            print('min_process_id',min_process_id)
            print('max_process_id',max_process_id)
            print('total_count',total_count)

            try:
                min_updated_data = process_update.objects.get(manufacture_id=i.manufacturing_id,
                                                         process_id=min_process_id)
                # global records
                records= True
                min_start_date=min_updated_data.start_date
                print('min_start_date',min_start_date)
                result["start_date"]=min_start_date
                result["status"]="On Going"


            except:
                records= False

            try:
                max_updated_data = process_update.objects.get(manufacture_id=i.manufacturing_id,
                                                          process_id=max_process_id,status="Completed")
                max_end_date=max_updated_data.end_date
                print('max_end_date',max_end_date)
                result["end_date"]=max_end_date

            except:
                pass
            try:
                completed_processes=process_update.objects.filter(manufacture_id=i.manufacturing_id,status="Completed").count()

                print('completed_count',completed_processes)
                progress= int((completed_processes/total_count)*100)
                result["progress"] = str(progress)
                if progress == 0 and records == False:
                    result["status"]="Not Started"
                    result["start_date"]="1111-11-11"
                    result["end_date"]="1111-11-11"
                elif progress == 0 and records == True:
                    result["status"] = "On Going"
                    result["start_date"] = min_start_date
                    result["end_date"] = "1111-11-11"




                elif progress == 100:
                    result["status"] = "Completed"
                else:
                    result["status"] = "On Going"
                    result["end_date"] = "1111-11-11"





            except:
                pass


        result_data.append(result)

    # Convert the dictionary to the desired list format

    print('result_data',result_data)

    return result_data

@api_view(["GET"])

def reports_data(request):

    res=excel_download()
    return res


def excel_download():
    entire_data = process_update.objects.all()
    entire_data_serializer = reports_process_update_Serializer(entire_data, many=True)
    entire_data_serializer_data = entire_data_serializer.data

    # Create an Excel workbook
    wb = Workbook()
    ws = wb.active

    # Write headers
    headers = list(entire_data_serializer_data[0].keys())
    ws.append(headers)

    # Write data
    for item in entire_data_serializer_data:
        ws.append(list(item.values()))

    # Save the workbook to a response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reports.xlsx"'
    wb.save(response)


    return response




def sending_email(m_id,p_id,status):

    # print('sendinggggggg email')
    email_body=f'''<p>{m_id} machine {p_id} {status}</p>'''
    send_mail("Machine Manufacturing update",'',from_email=settings.EMAIL_HOST_USER,
              recipient_list=["kavya.automac@gmail.com","veldisriharsha@gmail.com"],html_message=email_body)
    # print('sentttt')
