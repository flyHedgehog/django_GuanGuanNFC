from django.http import HttpResponse,JsonResponse
from .Serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import time
from django.db import connection
from django.core import serializers


from django.forms.models import model_to_dict
# Create your views here.
import json

def dictfetchall(cursor):
    "从cursor获取所有行数据转换成一个字典"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

@method_decorator(csrf_exempt)
def DaoUserInfoInsert(request):
    if request.method == "POST":
        username = request.POST.get('username',None)
        password = request.POST.get('password',None)
        try:
            UserInfo.objects.get(user_name=username)
        except ObjectDoesNotExist:
            UserInfo.objects.create(user_nameuser=username, password=password)
            return HttpResponse("注册成功")
        else:
            return HttpResponse("注册失败")

@method_decorator(csrf_exempt)
def DaoUserInfoLoadQuery(request):
    if request.method == "GET":
        username = request.GET.get('username')
        password = request.GET.get('password')
        try:
            user = UserInfo.objects.get(user_name=username)
        except ObjectDoesNotExist:
            return HttpResponse("用户不存在")
        else:
            if user.password == password:
                return HttpResponse("登录成功")
            else:
                return HttpResponse("登录失败")

@method_decorator(csrf_exempt)
def DaoUserInfoDelete(request):
    if request.method == "POST":
        username = request.POST.get('username')
        cursor = connection.cursor()
        cursor.execute("delete from guan_userinfo where user_name=%s",[username])
        return HttpResponse("删除成功")

@method_decorator(csrf_exempt)
def DaoUserInfoUpdate(request):
    if request.method == "POST":
        username = request.POST.get('username')
        newPassword = request.POST.get('newPassword')
        UserInfo.objects.filter(user_name=username).update(password=newPassword,updated_time=int(time.time()))
        return HttpResponse("修改成功")

@method_decorator(csrf_exempt)
def DaoUserInfoRegistrationQuery(request):
    if request.method == "GET":
        username = request.GET.get('username')
        if UserInfo.objects.filter(user_name=username).count() != 0:
            return HttpResponse(True)
        else:
            return HttpResponse(False)

@method_decorator(csrf_exempt)
def DaoUserInfoUpdateLastAct(request):
    if request.method == "POST":
        username = request.POST.get('username')
        last_act = request.POST.get('last_act')
        UserInfo.objects.filter(user_name=username).update(last_act=last_act)
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoUserInfoQueryLastActDate(request):
    if request.method == "GET":
        username = request.GET.get('username')
        last_act_date = request.GET.get('last_act_date')
        if last_act_date in UserInfo.objects.filter(user_name=username).values_list('last_act')[0]:
            return HttpResponse(True)
        else:
            return HttpResponse(False)

@method_decorator(csrf_exempt)
def DaoUserInfoUpdateActiveDay(request):
    if request.method == "POST":
        username = request.POST.get('username')
        ret = UserInfo.objects.get(user_name=username).active_day + 1
        UserInfo.objects.filter(user_name=username).update(active_day = ret)
        return HttpResponse(True)

class UserInfoAPIView(APIView):
    def get(self,request,format=None):
        username = self.request.query_params.get("username",0)
        user = UserInfo.objects.filter(user_name=username)
        if user:
            userInfo = UserInfoModelSerializer(user,many=True)
            return Response(userInfo.data)
        else:
            return Response(False)

@method_decorator(csrf_exempt)
def DaoActivityTypeInsert(request):
    if request.method == "POST":
        act_type = request.POST.get('act_type')
        ActivityType.objects.create(act_type=act_type)
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoActivityTypeDelete(request):
    if request.method == "POST":
        act_type = request.POST.get('act_type')
        ActivityType.objects.filter(act_type=act_type).delete()
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoActivityTypeUpdate(request):
    if request.method == "POST":
        act_oldType = request.POST.get('act_oldType')
        act_newType = request.POST.get('act_newType')
        ActivityType.objects.filter(act_type=act_oldType).update(act_type=act_newType,updated_time=int(time.time()))
        return HttpResponse(True)

class ActivityTypeAPIView(APIView):
    def get(self,request,format=None):
        act_type = self.request.query_params.get("act_type",0)
        activityType = ActivityType.objects.filter(act_type=act_type);
        if activityType:
            typeInfo = ActivityTypeModelSerializer(activityType,many=True)
            return Response(typeInfo.data)
        else:
            return Response(False)

class ActivityTypeAllAPIView(APIView):
    def get(self,request,format=None):
        activityType = ActivityType.objects.all();
        if activityType:
            typeInfo = ActivityTypeModelSerializer(activityType,many=True)
            return Response(typeInfo.data)
        else:
            return Response(False)

class ActivityAPIView(APIView):
    def get(self,request,format=None):
        user_name = self.request.query_params.get("user_name",0)
        type_name = self.request.query_params.get("type_name",0)
        user_id = UserInfo.objects.get(user_name=user_name).nid
        type_id = ActivityType.objects.get(act_type=type_name).nid
        AllActivity = Activity.objects.filter(user_id=user_id,type_id=type_id)
        if AllActivity:
            activityInfo = ActivityModelSerializer(AllActivity,many=True)
            return Response(activityInfo.data)
        else:
            return Response(False)

@method_decorator(csrf_exempt)
def DaoActivityInsert1(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        nfc = request.POST.get('nfc')
        act_type = request.POST.get('act_type')
        act_name = request.POST.get('act_name')
        user_ID = UserInfo.objects.get(user_name=user_name).nid
        type_ID = ActivityType.objects.get(act_type=act_type)
        Activity.objects.create(user_id=user_ID,nfc=nfc,type_id=type_ID,act_name=act_name)
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoActivityInsert2(request):
    if request.method == "POST":
        user_ID = request.POST.get('user_ID')
        nfc = request.POST.get('nfc')
        type_ID = request.POST.get('type_ID')
        act_name = request.POST.get('act_name')
        Activity.objects.create(user_id=user_ID,nfc=nfc,type_id=type_ID,act_name=act_name)
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoActivityDelete(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        act_name = request.POST.get('act_name')
        user_ID = UserInfo.objects.get(user_name=user_name).nid
        Activity.objects.filter(user_id=user_ID,act_name=act_name).delete()
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoActivityUpdate(request):
    if request.method == "POST":
        username = request.POST.get('username')
        act_oldName = request.POST.get('act_oldName')
        act_newName = request.POST.get('act_newName')
        user_ID = UserInfo.objects.get(user_name=username).nid
        Activity.objects.filter(user_id=user_ID,act_name=act_oldName).update(act_name=act_newName,updated_time=int(time.time()))
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoActivityQuery1(request):
    if request.method == "GET":
        user_name = request.GET.get('user_name')
        act_name = request.GET.get('act_name')
        user_ID = UserInfo.objects.get(user_name=user_name).nid
        if Activity.objects.filter(user_id=user_ID,act_name=act_name).count() != 0:
            return HttpResponse(True)
        else:
            return HttpResponse(False)

@method_decorator(csrf_exempt)
def DaoActivityQuery2(request):
    if request.method == "GET":
        nfc = request.GET.get('nfc')
        if Activity.objects.filter(nfc=nfc).count() != 0:
            return HttpResponse(True)
        else:
            return HttpResponse(False)

class Activity2APIView(APIView):
    def get(self,request,format=None):
        nfc = self.request.query_params.get("nfc", 0)
        activity = Activity.objects.filter(nfc=nfc)
        if activity:
            activityInfo = ActivityModelSerializer(activity, many=True)
            return Response(activityInfo.data)
        else:
            return Response(False)

@method_decorator(csrf_exempt)
def DaoActStaInsert(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        act_name = request.POST.get('act_name')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        user_id = UserInfo.objects.get(user_name=user_name).nid
        act_id = Activity.objects.get(act_name=act_name).nid
        ActSta.objects.create(act_id=act_id,user_id=user_id,start_time=start_time,end_time=end_time)
        return HttpResponse(True)

def DaoActStaInsert2(request):
    if request.method == "POST":
        act_ID = request.POST.get('act_ID')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        ActSta.objects.create(act_id=act_ID, start_time=start_time, end_time=end_time)
        return HttpResponse(True)

def DaoActStaInsert3(request):
    if request.method == "POST":
        act_ID = request.POST.get('act_ID')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        moment_text = request.POST.get('moment_text')
        is_shared = request.POST.get('is_shared')
        ActSta.objects.create(act_id=act_ID, start_time=start_time, end_time=end_time,moment_text=moment_text,is_shared=is_shared)
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoActStaUpdate(request):
    if request.method == "POST":
        username = request.POST.get('username')
        start_time = request.POST.get('start_time')
        moment_text = request.POST.get('moment_text')
        user_id = UserInfo.objects.get(user_name=username).nid
        ActSta.objects.filter(user_id=user_id,start_time=start_time).update(moment_text=moment_text,is_shared=1,shared_time=int(time.time()),updated_time=int(time.time()))
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoActStaUpdate2(request):
    if request.method == "POST":
        username = request.POST.get('username')
        moment_text = request.POST.get('moment_text')
        currentTime = int(time.time())
        cursor = connection.cursor()
        cursor.execute("update guan_actsta set moment_text=%s,is_shared=1,updated_time=%s ,shared_time=%s where end_time=(select max(end_time) from guan_actsta where act_id in (select nid from guan_activity where user_id=(select nid from guan_userinfo where user_name=%s)) group by end_time)",[moment_text,currentTime,currentTime,username])
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoActStaDelete(request):
    if request.method == "POST":
        act_ID = request.POST.get('act_ID')
        ActSta.objects.filter(act_id=act_ID).delete()
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoActStaQueryActType(request):
    if request.method == "GET":
        username = request.GET.get('user_name')
        begin = str(request.GET.get('begin'))
        end = str(request.GET.get('end'))
        cursor = connection.cursor()
        cursor.execute("select act_type,sum(end_time-start_time) from guan_activitytype,guan_actsta inner join guan_activity" +
                " on guan_activity.nid=guan_actsta.act_id " +
                " where guan_activitytype.nid=guan_activity.type_id and guan_activity.user_id=(select nid from guan_userinfo where user_name=%s) and start_time>%s and end_time<%s " +
                " group by act_type",[username,begin,end])
        raw = dictfetchall(cursor)
        return JsonResponse(list(raw), safe=False, json_dumps_params={'ensure_ascii': False})

@method_decorator(csrf_exempt)
def DaoActStaQueryActType2(request):
    if request.method == "GET":
        username = request.GET.get('user_name')
        begin = str(request.GET.get('begin'))
        end = str(request.GET.get('end'))
        act_type = request.GET.get('act_type')
        cursor = connection.cursor()
        cursor.execute("select act_type,sum(end_time-start_time) from guan_activitytype,guan_actsta inner join guan_activity" +
                " on guan_activity.nid=guan_actsta.act_id " +
                " where guan_ctivitytype.nid=guan_activity.type_id and guan_activity.user_id=(select nid from guan_userinfo where user_name=%s) and start_time>%s and end_time<%s and guan_activitytype.act_type=%s" +
                " group by act_type",[username,begin,end,act_type])
        raw = dictfetchall(cursor)
        return JsonResponse(list(raw), safe=False, json_dumps_params={'ensure_ascii': False})

@method_decorator(csrf_exempt)
def DaoActStaQueryByLengthDesc(request):
    if request.method == "GET":
        user_name = request.GET.get('user_name')
        cursor = connection.cursor()
        cursor.execute("select act_type,act_name,start_time,end_time,end_time-start_time from guan_actsta inner join guan_activity on guan_activity.nid=guan_actsta.nid inner join guan_activitytype on guan_activitytype.nid=guan_acticity.type_id where user_id=(select nid from guan_userinfo where user_name=%s) order by end_time-start_time desc",[user_name]
               )
        raw = dictfetchall(cursor)
        return JsonResponse(list(raw), safe=False, json_dumps_params={'ensure_ascii': False})

@method_decorator(csrf_exempt)
def DaoActStaQueryByLengthAsc(request):
    if request.method == "GET":
        user_name = request.GET.get('user_name')
        cursor = connection.cursor()
        cursor.execute("select act_type,act_name,start_time,end_time,end_time-start_time from guan_actsta inner join guan_activity on guan_activity.nid=guan_actsta.nid inner join guan_activitytype on guan_activitytype.nid=guan_activity.type_id where user_id=(select nid from guan_userinfo where user_name=%s) order by end_time-start_time asc",[user_name]
               )
        raw = dictfetchall(cursor)
        return JsonResponse(list(raw), safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt)
def DaoActStaQueryByTimeDesc(request):
    if request.method == "GET":
        user_name = request.GET.get('user_name')
        cursor = connection.cursor()
        cursor.execute(
            "select act_type,act_name,start_time,end_time,end_time-start_time from guan_actsta inner join guan_activity on guan_activity.nid=guan_actsta.nid inner join guan_activitytype on guan_activitytype.nid=guan_activity.type_id where guan_actsta.user_id=(select nid from guan_userinfo where user_name=%s) order by end_time desc",
            [user_name]
            )
        raw = dictfetchall(cursor)
        return JsonResponse(list(raw),safe=False,json_dumps_params={'ensure_ascii':False})

@method_decorator(csrf_exempt)
def DaoActStaQueryByTimeAsc(request):
    if request.method == "GET":
        user_name = request.GET.get('user_name')
        cursor = connection.cursor()
        cursor.execute(
            "select act_type,act_name,start_time,end_time,end_time-start_time from guan_actsta inner join guan_activity on guan_activity.nid=guan_actsta.nid inner join guan_activitytype on guan_activitytype.nid=guan_activity.type_id where guan_actsta.user_id=(select nid from guan_userinfo where user_name=%s) order by end_time asc",
            [user_name]
            )
        raw = dictfetchall(cursor)
        return JsonResponse(list(raw),safe=False,json_dumps_params={'ensure_ascii':False})

@method_decorator(csrf_exempt)
def DaoActStaQueryByLengthDesc2(request):
    if request.method == "GET":
        user_name = request.GET.get('user_name')
        act_type = request.GET.get('act_type')
        cursor = connection.cursor()
        cursor.execute("select act_type,act_name,start_time,end_time,end_time-start_time from guan_actsta inner join guan_activity on guan_activity.nid=guan_actsta.nid inner join guan_activitytype on guan_activitytype.nid=guan_acticity.type_id where user_id=(select nid from guan_userinfo where user_name=%s) and act_type=%s order by end_time-start_time desc",[user_name,act_type]
               )
        raw = dictfetchall(cursor)
        return JsonResponse(list(raw), safe=False, json_dumps_params={'ensure_ascii': False})

@method_decorator(csrf_exempt)
def DaoActStaQueryByLengthAsc2(request):
    if request.method == "GET":
        user_name = request.GET.get('user_name')
        act_type = request.GET.get('act_type')
        cursor = connection.cursor()
        cursor.execute("select act_type,act_name,start_time,end_time,end_time-start_time from guan_actsta inner join guan_activity on guan_activity.nid=guan_actsta.nid inner join guan_activitytype on guan_activitytype.nid=guan_acticity.type_id where user_id=(select nid from guan_userinfo where user_name=%s) and act_type=%s order by end_time-start_time asc",[user_name,act_type]
               )
        raw = dictfetchall(cursor)
        return JsonResponse(list(raw), safe=False, json_dumps_params={'ensure_ascii': False})

@method_decorator(csrf_exempt)
def DaoActStaQueryByTimeDesc2(request):
    if request.method == "GET":
        user_name = request.GET.get('user_name')
        act_type = request.GET.get('act_type')
        cursor = connection.cursor()
        cursor.execute(
            "select act_type,act_name,start_time,end_time,end_time-start_time from guan_actsta inner join guan_activity on guan_activity.nid=guan_actsta.nid inner join guan_activitytype on guan_activitytype.nid=guan_activity.type_id where guan_actsta.user_id=(select nid from guan_userinfo where user_name=%s) and act_type=%s order by end_time desc",
            [user_name,act_type]
            )
        raw = dictfetchall(cursor)
        return JsonResponse(list(raw),safe=False,json_dumps_params={'ensure_ascii':False})

@method_decorator(csrf_exempt)
def DaoActStaQueryByTimeAsc2(request):
    if request.method == "GET":
        user_name = request.GET.get('user_name')
        act_type = request.GET.get('act_type')
        cursor = connection.cursor()
        cursor.execute(
            "select act_type,act_name,start_time,end_time,end_time-start_time from guan_actsta inner join guan_activity on guan_activity.nid=guan_actsta.nid inner join guan_activitytype on guan_activitytype.nid=guan_activity.type_id where guan_actsta.user_id=(select nid from guan_userinfo where user_name=%s) and act_type=%s order by end_time asc",
            [user_name,act_type]
            )
        raw = dictfetchall(cursor)
        return JsonResponse(list(raw),safe=False,json_dumps_params={'ensure_ascii':False})











@method_decorator(csrf_exempt)
def DaoBoxInsert(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        nfc = request.POST.get('nfc')
        box_name = request.POST.get('box_name')
        box_pos = request.POST.get('box_pos')
        user_id = UserInfo.objects.get(user_name=user_name).nid
        Box.objects.create(user_id=user_id, nfc=nfc, box_name=box_name, box_pos=box_pos)
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoBoxInsert2(request):
    if request.method == "POST":
        nfc = request.POST.get('nfc')
        box_name = request.POST.get('box_name')
        box_pos = request.POST.get('box_pos')
        user_id = request.POST.get('user_ID')
        Box.objects.create(user_id=user_id, nfc=nfc, box_name=box_name, box_pos=box_pos)
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoBoxDelete(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        box_name = request.POST.get('box_name')
        user_id = UserInfo.objects.get(user_name=user_name).nid
        Box.objects.filter(user_id=user_id,box_name=box_name).delete()
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoBoxUpdateName(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        box_oldName = request.POST.get('box_oldName')
        box_newName = request.POST.get('box_newName')
        user_id = UserInfo.objects.get(user_name=user_name).nid
        Box.objects.filter(box_name=box_oldName,user_id=user_id).update(box_name=box_newName,updated_time=int(time.time()))
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoBoxUpdatePos(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        box_oldPos = request.POST.get('box_oldPos')
        box_newPos = request.POST.get('box_newPos')
        user_id = UserInfo.objects.get(user_name=user_name).nid
        Box.objects.filter(box_pos=box_oldPos,user_id=user_id).update(box_pos=box_newPos,updated_time=int(time.time()))
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoBoxQuery(request):
    if request.method == "GET":
        user_name = request.GET.get('username')
        box_name = request.GET.get('box_name')
        user_id = UserInfo.objects.get(user_name=user_name).nid
        if Box.objects.filter(user_id=user_id,box_name=box_name).count() != 0:
            return HttpResponse(True)
        else:
            return HttpResponse(False)

@method_decorator(csrf_exempt)
def DaoBoxQueryNFC(request):
    if request.method == "GET":
        nfc = request.GET.get('nfc')
        if Box.objects.filter(nfc=nfc).count() != 0:
            return HttpResponse(True)
        else:
            return HttpResponse(False)

@method_decorator(csrf_exempt)
def DaoBoxQueryBoxByNFC(request):
    if request.method == "GET":
        nfc = request.GET.get('nfc')
        box_name = Box.objects.get(nfc=nfc).box_name
        data={'box_name':box_name}
        return JsonResponse(data)

class DaoBoxQueryAllBoxAPIView(APIView):
    def get(self,request,format=None):
        user_name = self.request.query_params.get("user_name", 0)
        user_id = UserInfo.objects.get(user_name=user_name)
        box = Box.objects.filter(user_id=user_id)
        if box:
            AllBox = BoxModelSerializer(box,many=True)
            return Response(AllBox.data)
        else:
            return Response("查无此人")

def DaoBoxQueryBoxAndContent(request):
    if request.method == "GET":
        user_name = request.GET.get('user_name')
        box_name = request.GET.get('box_name')
        cursor = connection.cursor()
        cursor.execute(
            " select thing_name,thing_num from guan_boxcontent" +
            " inner join guan_box on guan_box.nid=guan_boxcontent.box_id_id " +
            " where guan_box.user_id=(select nid from guan_userinfo where user_name=%s) and guan_box.box_name=%s",
            [user_name,box_name]
        )
        raw = dictfetchall(cursor)
        return JsonResponse(list(raw), safe=False, json_dumps_params={'ensure_ascii': False})

def DaoBoxQueryBox(request):
    if request.method == "GET":
        user_name = request.GET.get('user_name')
        thing_name = request.GET.get('thing_name')
        cursor = connection.cursor()
        cursor.execute(
            "select box_name from guan_box where user_id=(select nid from guan_userinfo where user_name=%s) and nid in (select box_id_id from guan_boxcontent where thing_name=%s)",
            [user_name,thing_name]
        )
        raw = dictfetchall(cursor)
        return JsonResponse(list(raw), safe=False, json_dumps_params={'ensure_ascii': False})

@method_decorator(csrf_exempt)
def DaoBoxContentInsert(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        box_name = request.POST.get('box_name')
        thing_name = request.POST.get('thing_name')
        thing_num = request.POST.get('thing_num')
        user_id = UserInfo.objects.get(user_name=user_name).nid
        box_id = Box.objects.filter(user_id=user_id,box_name=box_name).first().nid
        BoxContent.objects.create(box_id_id=box_id,thing_name=thing_name,thing_num=thing_num)
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoBoxContentInsert2(request):
    if request.method == "POST":
        box_ID = request.POST.get('box_ID')
        thing_name = request.POST.get('thing_name')
        thing_num = request.POST.get('thing_num')
        BoxContent.objects.create(box_id_id=box_ID,thing_name=thing_name,thing_num=thing_num)
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoBoxContentDelete(request):
    if request.method == "POST":
        box_ID = request.POST.get('box_ID')
        BoxContent.objects.filter(box_id=box_ID).delete()
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoBoxContentDelete2(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        box_name = request.POST.get('box_name')
        thing_name = request.POST.get('thing_name')
        user_id = UserInfo.objects.get(user_name=user_name).nid
        box = Box.objects.filter(user_id=user_id,box_name=box_name).first().nid
        BoxContent.objects.filter(box_id=box,thing_name=thing_name).delete()
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoBoxContentUpdate(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        box_name = request.POST.get('box_name')
        thing_name = request.POST.get('thing_name')
        thing_num = request.POST.get('thing_num')
        user_id = UserInfo.objects.get(user_name=user_name).nid
        box = Box.objects.filter(user_id=user_id, box_name=box_name).first().nid
        BoxContent.objects.filter(box_id=box, thing_name=thing_name).update(thing_num=thing_num,updated_time=int(time.time()))
        return HttpResponse(True)

def DaoBoxContentLoadQuery(request):
    if request.method == "GET":
        user_name = request.GET.get('user_name')
        box_name = request.GET.get('box_name')
        thing_name = request.GET.get('thing_name')
        user_id = UserInfo.objects.get(user_name=user_name).nid
        box = Box.objects.filter(user_id=user_id, box_name=box_name).first().nid
        if BoxContent.objects.filter(box_id=box,thing_name=thing_name).count() != 0:
            return HttpResponse(True)
        else:
            return HttpResponse(False)

@method_decorator(csrf_exempt)
def DaoPushInsert(request):
    if request.method == "POST":
        author_id = request.POST.get('author_id')
        title = request.POST.get('title')
        summary = request.POST.get('summary')
        contents = request.POST.get('contents')
        PushNote.objects.create(author_id=author_id,title=title,summary=summary,contents=contents)
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoPushDelete(request):
    if request.method == "POST":
        id = request.POST.get('id')
        PushNote.objects.filter(nid=id).delete()
        return HttpResponse(True)

class DaoPushAPIView(APIView):
    def get(self,request,format=None):
        push = PushNote.objects.all()
        if push:
            pushNote = PushNoteModelSerializer(push,many=True)
            return Response(pushNote.data)
        else:
            return Response("无推送")

@method_decorator(csrf_exempt)
def DaoMomentInsert(request):
    if request.method == "POST":
        from_id = request.POST.get('from_id')
        to_id = request.POST.get('to_id')
        content = request.POST.get('content')
        is_processed = request.POST.get('is_processed')
        Application.objects.create(from_id=from_id,to_id=to_id,content=content,is_processed=is_processed)
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoMomentInsert2(request):
    if request.method == "POST":
        from_name = request.POST.get('from_name')
        to_name = request.POST.get('to_name')
        content = request.POST.get('content')
        from_id = UserInfo.objects.get(user_name=from_name).nid
        to_id = UserInfo.objects.get(user_name=to_name).nid
        Application.objects.create(from_id=from_id,to_id=to_id,content=content)
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoMomentDelete(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        friend_name = request.POST.get('friend_name')
        from_id = UserInfo.objects.get(user_name=user_name).nid
        to_id = UserInfo.objects.get(user_name=friend_name).nid
        Application.objects.filter(from_id=from_id,to_id=to_id).delete()
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoMomentUpdate(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        friend_name = request.POST.get('friend_name')
        from_id = UserInfo.objects.get(user_name=user_name).nid
        to_id = UserInfo.objects.get(user_name=friend_name).nid
        Application.objects.filter(from_id=from_id, to_id=to_id).update(is_processed=1,updated_time=int(time.time()))
        return HttpResponse(True)

class DaoMomentQueryAPIView(APIView):
    def get(self,request,format=None):
        user_name = self.request.query_params.get("user_name", 0)
        user_id = UserInfo.objects.get(user_name=user_name)
        applist = Application.objects.filter(to_id=user_id,is_processed=0)
        if applist:
            appList = ApplicationModelSerializer(applist,many=True)
            return Response(appList.data)
        else:
            return Response("空")


@method_decorator(csrf_exempt)
def DaoFriendInsert(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        friend_id = request.POST.get('friend_id')
        Friend.objects.create(user_id=user_id,friend_id=friend_id)
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoFriendInsert2(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        friend_name = request.POST.get('friend_name')
        user_id = UserInfo.objects.get(user_name=user_name).nid
        friend_id = UserInfo.objects.get(user_name=friend_name).nid
        Friend.objects.create(user_id=user_id, friend_id=friend_id)
        Friend.objects.create(user_id=friend_id, friend_id=user_id)
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoFriendDelete(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        friend_name = request.POST.get('friend_name')
        user_id = UserInfo.objects.get(user_name=user_name).nid
        friend_id = UserInfo.objects.get(user_name=friend_name).nid
        Friend.objects.filter(user_id=user_id, friend_id=friend_id).delete()
        Friend.objects.filter(user_id=friend_id, friend_id=user_id).delete()
        return HttpResponse(True)

@method_decorator(csrf_exempt)
def DaoFriendQuery(request):
    if request.method == "GET":
        user_name = request.GET.get('user_name')
        cursor = connection.cursor()
        cursor.execute(
            "select user_name,active_day from guan_userinfo where guan_userinfo.nid in (select friend_id from guan_friend where user_id=(select nid from guan_userinfo where user_name=%s))",
            [user_name]
        )
        raw = dictfetchall(cursor)
        return JsonResponse(list(raw), safe=False, json_dumps_params={'ensure_ascii': False})

@method_decorator(csrf_exempt)
def DaoFriendQueryFriendAct(request):
    if request.method == "GET":
        user_name = request.GET.get('user_name')
        cursor = connection.cursor()
        cursor.execute(
            "select user_name,active_day,act_type,start_time,end_time,(end_time-start_time),moment_text,shared_time from guan_actsta inner join guan_activity on guan_actsta.act_id=guan_activity.nid " +
                " inner join guan_userinfo on guan_userinfo.nid=guan_activity.user_id " +
                " inner join guan_activitytype on guan_activity.type_id=guan_activitytype.nid " +
                " where guan_userinfo.nid in (select friend_id from guan_friend where user_id=(select nid from guan_userinfo where user_name=%s))" +
                " and guan_actsta.is_shared=1",
            [user_name]
        )
        raw = dictfetchall(cursor)
        return JsonResponse(list(raw), safe=False, json_dumps_params={'ensure_ascii': False})





































