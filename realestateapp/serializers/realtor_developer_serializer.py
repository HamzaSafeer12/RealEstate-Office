from rest_framework import serializers
from realestateapp.models import UserConnection

class RealtorDeveloperConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConnection
        fields = '__all__'
        read_only_fields = ['realtor', 'receiver', 'status', 'created_at']