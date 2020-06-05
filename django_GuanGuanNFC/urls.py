"""django_GuanGuanNFC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from guan import views as GuanViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('DaoUserInfo/insert/',GuanViews.DaoUserInfoInsert),
    path('DaoUserInfo/loadQuery/',GuanViews.DaoUserInfoLoadQuery),
    path('DaoUserInfo/delete/',GuanViews.DaoUserInfoDelete),
    path('DaoUserInfo/update/',GuanViews.DaoUserInfoUpdate),
    path('DaoUserInfo/registrationQuery/',GuanViews.DaoUserInfoRegistrationQuery),
    path('DaoUserInfo/updateLastAct/',GuanViews.DaoUserInfoUpdateLastAct),
    path('DaoUserInfo/queryLastActDate/',GuanViews.DaoUserInfoQueryLastActDate),
    path('DaoUserInfo/updateActiveDay/',GuanViews.DaoUserInfoUpdateActiveDay),
    path('DaoUserInfo/personMessage/',GuanViews.UserInfoAPIView.as_view(),name="UserInfo"),
    path('DaoActivityType/insert/',GuanViews.DaoActivityTypeInsert),
    path('DaoActivityType/delete/',GuanViews.DaoActivityTypeDelete),
    path('DaoActivityType/update/',GuanViews.DaoActivityTypeUpdate),
    path('DaoActivityType/query/',GuanViews.ActivityTypeAPIView.as_view(),name="ActivityType"),
    path('DaoActivityType/queryAllType/',GuanViews.ActivityTypeAllAPIView.as_view(),name="AllActivityType"),
    path('DaoActivityType/queryTypeAndActivity/',GuanViews.ActivityAPIView.as_view(),name="Activity"),
    path('DaoActivity/insert1/',GuanViews.DaoActivityInsert1),
    path('DaoActivity/insert2/',GuanViews.DaoActivityInsert2),
    path('DaoActivity/delete/',GuanViews.DaoActivityDelete),
    path('DaoActivity/update/',GuanViews.DaoActivityUpdate),
    path('DaoActivity/query1/',GuanViews.DaoActivityQuery1),
    path('DaoActivity/query2/',GuanViews.DaoActivityQuery2),
    path('DaoActivity/queryActivityByNFC/',GuanViews.Activity2APIView.as_view(),name="Activity2"),
    path('DaoActSta/update2/',GuanViews.DaoActStaUpdate2),
    path('DaoActSta/queryActType/',GuanViews.DaoActStaQueryActType),
    path('DaoActSta/queryByTimeDesc/',GuanViews.DaoActStaQueryByTimeDesc),
    path('DaoBoxContent/insert2/',GuanViews.DaoBoxContentInsert2),

]
