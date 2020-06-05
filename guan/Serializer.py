from rest_framework import serializers
from .models import UserInfo,ActivityType,Activity,ActSta,Box,BoxContent,Friend,Application,PushNote

class UserInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('nid','user_name','password','active_day','last_act')

class ActivityTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityType
        fields = ('nid','act_type')

class ActivityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('nid','user_id','nfc','type_id','act_name')

class ActStaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActSta
        fields = ('nid','act_id','start_time','end_time','moment_text','is_shared','shared_time')

class BoxModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ('nid','user_id','nfc','box_name','box_pos')

class BoxContentModelSerializer(serializers.ModelSerializer):
    box_name = serializers.CharField(source='box_id.box_name')
    class Meta:
        model = BoxContent
        fields = ('box_name','thing_name','thing_num')

class FriendModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ('nid','user_id','friend_id')

class ApplicationModelSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='from_id.user_name')
    class Meta:
        model = Application
        fields = ('from_id','content','created_time')

class PushNoteModelSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author_id.user_name')
    class Meta:
        model = PushNote
        fields = ('nid','author_name','title','summary','contents')