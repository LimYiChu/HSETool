from UploadExcel.models import *
from .models import *
from rest_framework import serializers

class anySerializers(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ActionItems
        fields = ('id', 'StudyActionNo', 'StudyName')

class actionitemsserialiser (serializers.ModelSerializer):

    class Meta :
        pass