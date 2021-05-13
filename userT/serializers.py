from UploadExcel.models import *
from rest_framework import serializers

class anySerializers(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ActionItems
        fields = ('id', 'StudyActionNo', 'StudyName')