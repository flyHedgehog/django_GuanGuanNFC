from django.http import HttpResponse
from .Serializer import UserInfoModelSerializer,ActivityTypeModelSerializer,ActivityModelSerializer,ActStaModelSerializer,BoxModelSerializer,BoxContentModelSerializer,FriendModelSerializer,ApplicationModelSerializer,PushNoteModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserInfo,ActivityType,Activity,ActSta,Application,BoxContent,Box,Friend,PushNote
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

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