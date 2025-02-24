from rest_framework import serializers
from .models import GeneralList, CompletedList, CancelledList, NotComeList
class GeneralListSerializers(serializers.ModelSerializer):
    class Meta:
        model = GeneralList
        fields = ['id', 'service', 'firstname', 'lastname', 'phone','user_telegram_id', 'created_at','updated_at']
class GeneralListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralList
        fields = ['service', 'firstname', 'lastname', 'phone','user_telegram_id']
class HomeSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralList
        fields = ['service', 'firstname', 'lastname', 'phone']
class CompletedListSerializers(serializers.ModelSerializer):
    class Meta:
        model = CompletedList
        fields = ['id', 'service', 'firstname', 'lastname', 'phone','user_telegram_id', 'created_at','updated_at']

class CancelledListSerializers(serializers.ModelSerializer):
    class Meta:
        model = CancelledList
        fields = ['id', 'service', 'firstname', 'lastname', 'phone','user_telegram_id', 'created_at','updated_at']

class NotComeListSerializers(serializers.ModelSerializer):
    class Meta:
        model = NotComeList
        fields = ['id', 'service', 'firstname', 'lastname', 'phone','user_telegram_id', 'created_at','updated_at']