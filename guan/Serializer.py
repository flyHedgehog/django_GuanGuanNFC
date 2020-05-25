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
        fields = ('nid','act_id','start_time','end_time','moment_text','is_shared')

class BoxModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ('nid','user_id','nfc','box_name','box_pos')

class BoxContentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxContent
        fields = ('nid','box_id','thing_name','thing_num')

class FriendModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ('nid','user_id','friend_id')

class ApplicationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('nid','from_id','to_id','content','is_processed')

class PushNoteModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushNote
        fields = ('nid','author_id','title','summary','contents')